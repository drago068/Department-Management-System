"""
Authentication repository for user and token data access.
"""
from typing import Optional
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.user import User, RefreshToken


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username.strip())
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        stmt = (
            select(User)
            .options(
                selectinload(User.student_profile),
                selectinload(User.staff_profile),
                selectinload(User.admin_profile),
            )
            .where(User.id == user_id)
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_refresh_token(self, token_hash: str) -> Optional[RefreshToken]:
        stmt = select(RefreshToken).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.is_revoked.is_(False),
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()


__all__ = ["AuthRepository"]
