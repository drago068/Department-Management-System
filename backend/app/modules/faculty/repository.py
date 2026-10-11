"""
Faculty and Staff data repository.
"""
from typing import Optional, List
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.profiles import Staff


class FacultyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, staff_id: uuid.UUID) -> Optional[Staff]:
        stmt = (
            select(Staff)
            .options(selectinload(Staff.user), selectinload(Staff.department))
            .where(Staff.id == staff_id)
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_employee_id(self, employee_id: str) -> Optional[Staff]:
        stmt = (
            select(Staff)
            .options(selectinload(Staff.user))
            .where(Staff.employee_id == employee_id.strip())
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_all_mentors(self) -> List[Staff]:
        stmt = (
            select(Staff)
            .options(selectinload(Staff.user), selectinload(Staff.department))
            .order_by(Staff.full_name.asc())
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())


__all__ = ["FacultyRepository"]
