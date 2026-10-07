from datetime import datetime, timedelta, timezone
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.config import settings
from app.core.exceptions import AppException, ForbiddenException, UnauthorizedException
from app.core.security import create_access_token, generate_refresh_token, verify_password
from app.models.profiles import AdminProfile, Staff, Student
from app.models.user import RefreshToken, User
from app.schemas.auth import LoginRequest, TokenResponseData, UserAuthResponse, UserProfileSummary


class AuthService:
    @staticmethod
    async def login(db: AsyncSession, request: LoginRequest, ip_address: str = None) -> TokenResponseData:
        ident = request.identifier.strip().lower()
        stmt = (
            select(User)
            .outerjoin(Student, User.id == Student.user_id)
            .outerjoin(Staff, User.id == Staff.user_id)
            .outerjoin(AdminProfile, User.id == AdminProfile.user_id)
            .options(
                selectinload(User.student_profile),
                selectinload(User.staff_profile),
                selectinload(User.admin_profile),
            )
            .where(
                or_(
                    func.lower(User.identifier) == ident,
                    func.lower(Student.register_number) == ident,
                    func.lower(Student.email) == ident,
                    func.lower(Staff.faculty_id) == ident,
                    func.lower(Staff.email) == ident,
                    func.lower(AdminProfile.email) == ident,
                )
            )
        )
        result = await db.execute(stmt)
        users = result.scalars().all()

        if not users:
            raise UnauthorizedException(
                message="Invalid identifier or password",
                details={"code": "INVALID_CREDENTIALS"},
            )

        # Match user by role if requested, otherwise take first match
        user = None
        if request.role:
            for u in users:
                if u.role.upper() == request.role.upper():
                    user = u
                    break
        if not user:
            user = users[0]

        if not verify_password(request.password, user.password_hash):
            raise UnauthorizedException(
                message="Invalid identifier or password",
                details={"code": "INVALID_CREDENTIALS"},
            )

        if request.role and user.role != request.role.upper():
            raise UnauthorizedException(
                message=f"Identifier does not have permission for the {request.role} portal",
                details={"code": "ROLE_MISMATCH"},
            )

        if not user.is_active:
            raise ForbiddenException(
                message="Your account has been deactivated. Please contact campus admin.",
                details={"code": "ACCOUNT_LOCKED"},
            )

        # Update last login timestamp
        user.last_login = datetime.now(timezone.utc)

        # Issue tokens
        access_token = create_access_token(
            subject=str(user.id),
            role=user.role,
            identifier=user.identifier,
        )

        raw_refresh_token = generate_refresh_token()
        refresh_token_record = RefreshToken(
            user_id=user.id,
            token_hash=raw_refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            revoked=False,
        )
        db.add(refresh_token_record)
        await db.commit()
        await db.refresh(user)

        # Profile summary resolution
        full_name = user.identifier
        avatar_url = None
        if user.role == "STUDENT" and user.student_profile:
            full_name = user.student_profile.full_name
            avatar_url = user.student_profile.avatar_url
        elif user.role == "STAFF" and user.staff_profile:
            full_name = user.staff_profile.full_name
            avatar_url = user.staff_profile.avatar_url
        elif user.role == "ADMIN" and user.admin_profile:
            full_name = user.admin_profile.full_name
            avatar_url = user.admin_profile.avatar_url

        return TokenResponseData(
            access_token=access_token,
            refresh_token=raw_refresh_token,
            token_type="Bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserAuthResponse(
                id=str(user.id),
                identifier=user.identifier,
                role=user.role,
                profile=UserProfileSummary(
                    full_name=full_name,
                    avatar_url=avatar_url,
                ),
            ),
        )

    @staticmethod
    async def refresh(db: AsyncSession, raw_refresh_token: str) -> TokenResponseData:
        stmt = (
            select(RefreshToken)
            .options(
                selectinload(RefreshToken.user).selectinload(User.student_profile),
                selectinload(RefreshToken.user).selectinload(User.staff_profile),
                selectinload(RefreshToken.user).selectinload(User.admin_profile),
            )
            .where(RefreshToken.token_hash == raw_refresh_token)
        )
        result = await db.execute(stmt)
        token_record = result.scalar_one_or_none()

        if not token_record or token_record.revoked:
            raise UnauthorizedException(
                message="Refresh token is invalid or has expired",
                details={"code": "INVALID_REFRESH_TOKEN"},
            )

        now = datetime.now(timezone.utc)
        exp = token_record.expires_at
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)

        if exp < now:
            raise UnauthorizedException(
                message="Refresh token is invalid or has expired",
                details={"code": "INVALID_REFRESH_TOKEN"},
            )

        user = token_record.user
        if not user or not user.is_active:
            raise UnauthorizedException("User account is inactive or not found")

        # Invalidate old refresh token (rotation)
        token_record.revoked = True

        # Generate new tokens
        access_token = create_access_token(
            subject=str(user.id),
            role=user.role,
            identifier=user.identifier,
        )
        new_refresh_token = generate_refresh_token()
        new_token_record = RefreshToken(
            user_id=user.id,
            token_hash=new_refresh_token,
            expires_at=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            revoked=False,
        )
        db.add(new_token_record)
        await db.commit()

        full_name = user.identifier
        avatar_url = None
        if user.role == "STUDENT" and user.student_profile:
            full_name = user.student_profile.full_name
            avatar_url = user.student_profile.avatar_url
        elif user.role == "STAFF" and user.staff_profile:
            full_name = user.staff_profile.full_name
            avatar_url = user.staff_profile.avatar_url
        elif user.role == "ADMIN" and user.admin_profile:
            full_name = user.admin_profile.full_name
            avatar_url = user.admin_profile.avatar_url

        return TokenResponseData(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="Bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserAuthResponse(
                id=str(user.id),
                identifier=user.identifier,
                role=user.role,
                profile=UserProfileSummary(
                    full_name=full_name,
                    avatar_url=avatar_url,
                ),
            ),
        )

    @staticmethod
    async def logout(db: AsyncSession, raw_refresh_token: str) -> None:
        stmt = select(RefreshToken).where(RefreshToken.token_hash == raw_refresh_token)
        result = await db.execute(stmt)
        token_record = result.scalar_one_or_none()
        if token_record:
            token_record.revoked = True
            await db.commit()
