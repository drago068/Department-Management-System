import uuid
from typing import Annotated, List, Optional
from fastapi import Depends, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.database import get_db
from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.core.security import decode_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    auto_error=False,
)


async def get_current_user(
    token: Annotated[Optional[str], Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    if not token:
        raise UnauthorizedException("Authentication token is missing")

    try:
        payload = decode_token(token)
    except Exception:
        raise UnauthorizedException("Invalid or expired authentication token")

    user_id_str: Optional[str] = payload.get("sub")
    if not user_id_str:
        raise UnauthorizedException("Malformed authentication token")

    try:
        user_uuid = uuid.UUID(user_id_str)
    except ValueError:
        raise UnauthorizedException("Invalid user identifier in token")

    stmt = (
        select(User)
        .options(
            selectinload(User.student_profile),
            selectinload(User.staff_profile),
            selectinload(User.admin_profile),
        )
        .where(User.id == user_uuid)
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise UnauthorizedException("User associated with token no longer exists")

    if not user.is_active:
        raise UnauthorizedException("User account is deactivated")

    return user


async def get_optional_user(
    token: Annotated[Optional[str], Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Optional[User]:
    if not token:
        return None
    try:
        return await get_current_user(token=token, db=db)
    except UnauthorizedException:
        return None


def require_role(allowed_roles: List[str]):
    async def role_checker(current_user: Annotated[User, Depends(get_current_user)]) -> User:
        if current_user.role not in allowed_roles:
            raise ForbiddenException(
                f"Access denied. Requires one of roles: {', '.join(allowed_roles)}. Your role is {current_user.role}."
            )
        return current_user

    return role_checker
