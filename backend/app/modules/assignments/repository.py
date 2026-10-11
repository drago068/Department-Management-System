"""
Assignment data repository.
"""
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession


class AssignmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


__all__ = ["AssignmentRepository"]
