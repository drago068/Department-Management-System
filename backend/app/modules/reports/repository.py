"""
Reports data repository.
"""
from sqlalchemy.ext.asyncio import AsyncSession


class ReportRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


__all__ = ["ReportRepository"]
