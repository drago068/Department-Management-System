"""
User data repository.
"""
from typing import Optional, List
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_all_active(self) -> List[User]:
        stmt = select(User).where(User.is_active.is_(True))
        res = await self.db.execute(stmt)
        return list(res.scalars().all())


__all__ = ["UserRepository"]
