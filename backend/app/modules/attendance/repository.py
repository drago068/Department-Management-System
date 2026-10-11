"""
Attendance data repository.
"""
from typing import Optional, List
from datetime import date
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.attendance import AttendanceRecord, AttendanceSession


class AttendanceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_session_by_id(self, session_id: uuid.UUID) -> Optional[AttendanceSession]:
        stmt = select(AttendanceSession).where(AttendanceSession.id == session_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_session(
        self, timetable_entry_id: uuid.UUID, session_date: date
    ) -> Optional[AttendanceSession]:
        stmt = select(AttendanceSession).where(
            AttendanceSession.timetable_entry_id == timetable_entry_id,
            AttendanceSession.date == session_date,
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_records_by_student(self, student_id: uuid.UUID) -> List[AttendanceRecord]:
        stmt = select(AttendanceRecord).where(AttendanceRecord.student_id == student_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())


__all__ = ["AttendanceRepository"]
