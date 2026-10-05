import os
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.common import StandardResponse
from app.schemas.materials import MaterialItemResponse
from app.services.material_service import MaterialService

router = APIRouter(prefix="/materials", tags=["Study Materials"])


@router.get("", response_model=StandardResponse[List[MaterialItemResponse]])
async def list_materials(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    course_id: Optional[str] = Query(None),
    material_type: Optional[str] = Query(None),
    unit: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
):
    items = await MaterialService.list_materials(
        db=db,
        course_id=course_id,
        material_type=material_type,
        unit=unit,
        search=search,
        limit=limit,
        page=page,
    )
    return StandardResponse(data=items, message="Materials retrieved successfully")


@router.post("/upload", response_model=StandardResponse[MaterialItemResponse], status_code=status.HTTP_201_CREATED)
async def upload_material(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role(["STAFF", "ADMIN"]))],
    course_id: str = Form(...),
    title: str = Form(...),
    material_type: str = Form("LECTURE_NOTE"),
    unit: Optional[str] = Form(None),
    topic: Optional[str] = Form(None),
    file: UploadFile = File(...),
):
    material = await MaterialService.upload_material(
        db=db,
        current_user=current_user,
        course_id=course_id,
        title=title,
        unit=unit,
        topic=topic,
        material_type=material_type,
        file=file,
    )
    return StandardResponse(data=material, message="Study material uploaded successfully")


@router.get("/{material_id}/download")
async def download_material(
    material_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    file_path = await MaterialService.track_download(
        db=db,
        material_id=material_id,
        current_user=current_user,
    )
    filename = os.path.basename(file_path)
    return FileResponse(path=file_path, filename=filename)


@router.delete("/{material_id}", response_model=StandardResponse[None])
async def delete_material(
    material_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role(["STAFF", "ADMIN"]))],
):
    await MaterialService.delete_material(
        db=db,
        material_id=material_id,
        current_user=current_user,
    )
    return StandardResponse(data=None, message="Study material deleted successfully")
