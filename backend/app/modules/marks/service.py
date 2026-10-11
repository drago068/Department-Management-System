"""
Marks business service.
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.marks.schemas import MarkItem, StudentMarksSummary


class MarksService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_student_marks(self, student_id: str) -> StudentMarksSummary:
        return StudentMarksSummary(
            student_id=student_id,
            register_number="",
            marks=[],
            gpa=None,
        )


__all__ = ["MarksService"]
