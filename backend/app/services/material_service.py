import os
from typing import List, Optional
import uuid
import aiofiles
from fastapi import UploadFile
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.config import settings
from app.core.exceptions import AppException, ForbiddenException, NotFoundException
from app.models.academics import Course
from app.models.materials import Material, MaterialDownload
from app.models.profiles import Staff
from app.models.user import User
from app.schemas.materials import MaterialItemResponse
from app.services.audit_service import AuditService


class MaterialService:
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{round(size_bytes / 1024, 1)} KB"
        else:
            return f"{round(size_bytes / (1024 * 1024), 1)} MB"

    @staticmethod
    async def list_materials(
        db: AsyncSession,
        course_id: Optional[str] = None,
        material_type: Optional[str] = None,
        unit: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 50,
        page: int = 1,
    ) -> List[MaterialItemResponse]:
        stmt = (
            select(Material)
            .options(selectinload(Material.course), selectinload(Material.staff))
            .where(Material.is_active == True)
            .order_by(Material.reads_count.desc(), Material.created_at.desc())
        )

        if course_id:
            stmt = stmt.where(Material.course_id == uuid.UUID(course_id))
        if material_type:
            stmt = stmt.where(Material.material_type == material_type.upper())
        if unit:
            stmt = stmt.where(Material.unit == unit)
        if search:
            search_pattern = f"%{search}%"
            stmt = stmt.where(Material.title.ilike(search_pattern) | Material.topic.ilike(search_pattern))

        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)

        result = await db.execute(stmt)
        materials = result.scalars().all()

        return [
            MaterialItemResponse(
                id=str(m.id),
                course_id=str(m.course_id),
                course_code=m.course.code,
                course_name=m.course.name,
                unit=m.unit,
                title=m.title,
                topic=m.topic,
                instructor=m.staff.full_name,
                material_type=m.material_type,
                file_format=m.file_format,
                file_size=MaterialService.format_file_size(m.file_size_bytes),
                page_count=m.page_count,
                reads_count=m.reads_count,
                downloads_count=m.downloads_count,
                download_url=f"/api/v1/materials/{m.id}/download",
                created_at=m.created_at,
            )
            for m in materials
        ]

    @staticmethod
    async def upload_material(
        db: AsyncSession,
        current_user: User,
        course_id: str,
        title: str,
        unit: Optional[str],
        topic: Optional[str],
        material_type: str,
        file: UploadFile,
    ) -> MaterialItemResponse:
        staff = (await db.execute(select(Staff).where(Staff.user_id == current_user.id))).scalar_one_or_none()
        if not staff and current_user.role != "ADMIN":
            raise ForbiddenException("Only staff or admin can upload materials")

        staff_id = staff.id if staff else None
        if not staff_id:
            # Fallback to first staff if admin uploads
            first_staff = (await db.execute(select(Staff).limit(1))).scalar_one_or_none()
            if first_staff:
                staff_id = first_staff.id
            else:
                raise NotFoundException("No staff member registered to attribute upload")

        course_uuid = uuid.UUID(course_id)
        course = (await db.execute(select(Course).where(Course.id == course_uuid))).scalar_one_or_none()
        if not course:
            raise NotFoundException("Course not found")

        # Save file to upload directory
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        file_ext = os.path.splitext(file.filename or "")[1].lower().replace(".", "") or "pdf"
        file_uuid = uuid.uuid4()
        dest_filename = f"{file_uuid}.{file_ext}"
        dest_path = os.path.join(settings.UPLOAD_DIR, dest_filename)

        content = await file.read()
        file_size = len(content)

        async with aiofiles.open(dest_path, "wb") as out_file:
            await out_file.write(content)

        material = Material(
            id=file_uuid,
            course_id=course_uuid,
            uploaded_by=staff_id,
            title=title,
            unit=unit,
            topic=topic,
            material_type=material_type.upper(),
            file_path=dest_path,
            file_format=file_ext.upper(),
            file_size_bytes=file_size,
            page_count=12,  # default estimate
            reads_count=1,
            downloads_count=0,
            is_active=True,
        )
        db.add(material)
        await db.commit()
        await db.refresh(material)

        # Re-query with relationships
        stmt = (
            select(Material)
            .options(selectinload(Material.course), selectinload(Material.staff))
            .where(Material.id == material.id)
        )
        m = (await db.execute(stmt)).scalar_one()

        return MaterialItemResponse(
            id=str(m.id),
            course_id=str(m.course_id),
            course_code=m.course.code,
            course_name=m.course.name,
            unit=m.unit,
            title=m.title,
            topic=m.topic,
            instructor=m.staff.full_name,
            material_type=m.material_type,
            file_format=m.file_format,
            file_size=MaterialService.format_file_size(m.file_size_bytes),
            page_count=m.page_count,
            reads_count=m.reads_count,
            downloads_count=m.downloads_count,
            download_url=f"/api/v1/materials/{m.id}/download",
            created_at=m.created_at,
        )

    @staticmethod
    async def track_download(db: AsyncSession, material_id: str, current_user: User) -> str:
        mat_uuid = uuid.UUID(material_id)
        mat = (await db.execute(select(Material).where(Material.id == mat_uuid, Material.is_active == True))).scalar_one_or_none()
        if not mat:
            raise NotFoundException("Material not found")

        mat.downloads_count += 1
        mat.reads_count += 1

        download_log = MaterialDownload(
            material_id=mat.id,
            user_id=current_user.id,
        )
        db.add(download_log)
        await db.commit()
        return mat.file_path

    @staticmethod
    async def delete_material(db: AsyncSession, material_id: str, current_user: User) -> None:
        mat_uuid = uuid.UUID(material_id)
        mat = (await db.execute(select(Material).where(Material.id == mat_uuid))).scalar_one_or_none()
        if not mat:
            raise NotFoundException("Material not found")

        if current_user.role == "STAFF":
            staff = (await db.execute(select(Staff).where(Staff.user_id == current_user.id))).scalar_one_or_none()
            if not staff or mat.uploaded_by != staff.id:
                raise ForbiddenException("You can only delete materials that you uploaded yourself")

        mat.is_active = False
        await AuditService.log_action(
            db=db,
            action="MATERIAL_DELETE",
            entity_name="materials",
            entity_id=str(mat.id),
            user_id=current_user.id,
        )
        await db.commit()
