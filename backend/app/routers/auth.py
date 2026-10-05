from typing import Annotated
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest, RefreshTokenRequest, TokenResponseData
from app.schemas.common import StandardResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=StandardResponse[TokenResponseData])
async def login(
    request: LoginRequest,
    req: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    ip_address = req.client.host if req.client else None
    token_data = await AuthService.login(db=db, request=request, ip_address=ip_address)
    return StandardResponse(
        data=token_data,
        message="Authentication successful",
    )


@router.post("/refresh", response_model=StandardResponse[TokenResponseData])
async def refresh_token(
    request: RefreshTokenRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    token_data = await AuthService.refresh(db=db, raw_refresh_token=request.refresh_token)
    return StandardResponse(
        data=token_data,
        message="Access token refreshed successfully",
    )


@router.post("/logout", response_model=StandardResponse[None])
async def logout(
    request: RefreshTokenRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    await AuthService.logout(db=db, raw_refresh_token=request.refresh_token)
    return StandardResponse(
        data=None,
        message="Logged out successfully",
    )
