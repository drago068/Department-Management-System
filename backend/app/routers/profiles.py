from typing import Annotated, Any, Union
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.common import StandardResponse
from app.schemas.profile import (
    AdminProfileData,
    AdminProfileUpdate,
    StaffProfileData,
    StaffProfileUpdate,
    StudentProfileData,
    StudentProfileUpdate,
)
from app.services.user_service import UserService

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get("/me", response_model=StandardResponse[Union[StudentProfileData, StaffProfileData, AdminProfileData]])
async def get_my_profile(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    profile = await UserService.get_profile(db=db, current_user=current_user)
    return StandardResponse(
        data=profile,
        message="Profile retrieved successfully",
    )


@router.put("/me", response_model=StandardResponse[Union[StudentProfileData, StaffProfileData, AdminProfileData]])
async def update_my_profile(
    payload: Union[StudentProfileUpdate, StaffProfileUpdate, AdminProfileUpdate],
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    updated = await UserService.update_profile(db=db, current_user=current_user, payload=payload)
    return StandardResponse(
        data=updated,
        message="Profile updated successfully",
    )
