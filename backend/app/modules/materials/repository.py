"""
Materials data repository.
"""
from typing import Optional, List
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.materials import Material


class MaterialRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, material_id: uuid.UUID) -> Optional[Material]:
        stmt = (
            select(Material)
            .options(selectinload(Material.course), selectinload(Material.uploaded_by_user))
            .where(Material.id == material_id)
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_course(self, course_id: uuid.UUID) -> List[Material]:
        stmt = (
            select(Material)
            .where(Material.course_id == course_id)
            .order_by(Material.created_at.desc())
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())


__all__ = ["MaterialRepository"]
