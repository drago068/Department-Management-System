"""
Department data repository.
"""
from typing import Optional, List
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organization import Department


class DepartmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, dept_id: uuid.UUID) -> Optional[Department]:
        stmt = select(Department).where(Department.id == dept_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Optional[Department]:
        stmt = select(Department).where(Department.code == code.strip().upper())
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_all_active(self) -> List[Department]:
        stmt = select(Department).where(Department.is_active.is_(True)).order_by(Department.name.asc())
        res = await self.db.execute(stmt)
        return list(res.scalars().all())


__all__ = ["DepartmentRepository"]
