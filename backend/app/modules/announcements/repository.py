"""
Announcements data repository.
"""
from typing import Optional, List
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.announcements import Announcement


class AnnouncementRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, announcement_id: uuid.UUID) -> Optional[Announcement]:
        stmt = select(Announcement).where(Announcement.id == announcement_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_active(self) -> List[Announcement]:
        stmt = select(Announcement).order_by(Announcement.publish_date.desc())
        res = await self.db.execute(stmt)
        return list(res.scalars().all())


__all__ = ["AnnouncementRepository"]
