from datetime import date, datetime, timezone
from typing import List, Optional
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundException
from app.models.announcements import Announcement
from app.models.user import User
from app.schemas.announcements import AnnouncementCreateRequest, AnnouncementItemResponse
from app.services.audit_service import AuditService


class AnnouncementService:
    @staticmethod
    async def list_announcements(
        db: AsyncSession,
        category: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 50,
        page: int = 1,
    ) -> List[AnnouncementItemResponse]:
        now = datetime.now(timezone.utc)
        stmt = (
            select(Announcement)
            .where(
                Announcement.is_active == True,
                (Announcement.expires_at == None) | (Announcement.expires_at > now),
            )
            .order_by(Announcement.publish_date.desc(), Announcement.created_at.desc())
        )

        if category and category.lower() != "all":
            stmt = stmt.where(Announcement.category == category.lower())

        if search:
            pattern = f"%{search}%"
            stmt = stmt.where(
                Announcement.title.ilike(pattern)
                | Announcement.content.ilike(pattern)
                | Announcement.reference_number.ilike(pattern)
            )

        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)

        announcements = (await db.execute(stmt)).scalars().all()

        return [
            AnnouncementItemResponse(
                id=str(a.id),
                category=a.category,
                reference_number=a.reference_number,
                title=a.title,
                heading=a.heading or a.title,
                content=a.content,
                department=a.department_name,
                date=a.publish_date.strftime("%d %b %Y"),
                tag=a.tag,
                badge=a.badge,
                badge_type=a.badge_type or "blue",
                footer=a.footer,
                publish_date=a.publish_date.isoformat(),
                expires_at=a.expires_at,
            )
            for a in announcements
        ]

    @staticmethod
    async def create_announcement(
        db: AsyncSession,
        request: AnnouncementCreateRequest,
        current_user: User,
    ) -> AnnouncementItemResponse:
        pub_date = request.publish_date or date.today()

        announcement = Announcement(
            title=request.title,
            heading=request.heading or request.title,
            content=request.content,
            category=request.category.lower(),
            target_role=request.target_role.upper(),
            reference_number=request.reference_number,
            tag=request.tag,
            badge=request.badge,
            badge_type=request.badge_type,
            department_name=request.department_name,
            footer=request.footer,
            publish_date=pub_date,
            expires_at=request.expires_at,
            created_by=current_user.id,
            is_active=True,
        )
        db.add(announcement)
        await db.flush()

        await AuditService.log_action(
            db=db,
            action="ANNOUNCEMENT_CREATE",
            entity_name="announcements",
            entity_id=str(announcement.id),
            user_id=current_user.id,
            details={"title": announcement.title, "category": announcement.category},
        )
        await db.commit()
        await db.refresh(announcement)

        return AnnouncementItemResponse(
            id=str(announcement.id),
            category=announcement.category,
            reference_number=announcement.reference_number,
            title=announcement.title,
            heading=announcement.heading,
            content=announcement.content,
            department=announcement.department_name,
            date=announcement.publish_date.strftime("%d %b %Y"),
            tag=announcement.tag,
            badge=announcement.badge,
            badge_type=announcement.badge_type,
            footer=announcement.footer,
            publish_date=announcement.publish_date.isoformat(),
            expires_at=announcement.expires_at,
        )

    @staticmethod
    async def delete_announcement(db: AsyncSession, announcement_id: str, current_user: User) -> None:
        ann_uuid = uuid.UUID(announcement_id)
        ann = (await db.execute(select(Announcement).where(Announcement.id == ann_uuid))).scalar_one_or_none()
        if not ann:
            raise NotFoundException("Announcement not found")

        ann.is_active = False
        await AuditService.log_action(
            db=db,
            action="ANNOUNCEMENT_DELETE",
            entity_name="announcements",
            entity_id=str(ann.id),
            user_id=current_user.id,
        )
        await db.commit()
