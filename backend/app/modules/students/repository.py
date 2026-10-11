"""
Student data repository.
"""
from typing import Optional, List
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.profiles import Student


class StudentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, student_id: uuid.UUID) -> Optional[Student]:
        stmt = (
            select(Student)
            .options(selectinload(Student.user), selectinload(Student.mentor))
            .where(Student.id == student_id)
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_register_number(self, register_number: str) -> Optional[Student]:
        stmt = (
            select(Student)
            .options(selectinload(Student.user))
            .where(Student.register_number == register_number.strip().upper())
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_section(self, section_id: uuid.UUID) -> List[Student]:
        stmt = (
            select(Student)
            .options(selectinload(Student.user))
            .where(Student.section_id == section_id)
            .order_by(Student.roll_number.asc())
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())


__all__ = ["StudentRepository"]
