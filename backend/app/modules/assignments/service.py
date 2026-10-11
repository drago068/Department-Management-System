"""
Assignments business service.
"""
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.assignments.schemas import AssignmentItem


class AssignmentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_assignments(self, course_id: str) -> List[AssignmentItem]:
        return []


__all__ = ["AssignmentService"]
