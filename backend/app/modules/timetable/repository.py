"""
Timetable data repository.
"""
from typing import Optional, List
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.timetable import TimetableEntry


class TimetableRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, entry_id: uuid.UUID) -> Optional[TimetableEntry]:
        stmt = (
            select(TimetableEntry)
            .options(
                selectinload(TimetableEntry.course),
                selectinload(TimetableEntry.staff),
                selectinload(TimetableEntry.room),
                selectinload(TimetableEntry.period),
            )
            .where(TimetableEntry.id == entry_id)
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_section_and_day(
        self, section_id: uuid.UUID, day_of_week: int
    ) -> List[TimetableEntry]:
        stmt = (
            select(TimetableEntry)
            .options(
                selectinload(TimetableEntry.course),
                selectinload(TimetableEntry.staff),
                selectinload(TimetableEntry.room),
                selectinload(TimetableEntry.period),
            )
            .where(
                TimetableEntry.section_id == section_id,
                TimetableEntry.day_of_week == day_of_week,
            )
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())


__all__ = ["TimetableRepository"]
