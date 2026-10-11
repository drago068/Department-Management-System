"""
Subject and Course data repository.
"""
from typing import Optional, List
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.academics import Course


class SubjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, course_id: uuid.UUID) -> Optional[Course]:
        stmt = select(Course).where(Course.id == course_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Optional[Course]:
        stmt = select(Course).where(Course.code == code.strip().upper())
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_department(self, department_id: uuid.UUID) -> List[Course]:
        stmt = select(Course).where(Course.department_id == department_id).order_by(Course.code.asc())
        res = await self.db.execute(stmt)
        return list(res.scalars().all())


__all__ = ["SubjectRepository"]
