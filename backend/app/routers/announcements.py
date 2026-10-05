from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.user import User
from app.schemas.announcements import AnnouncementCreateRequest, AnnouncementItemResponse
from app.schemas.common import StandardResponse
from app.services.announcement_service import AnnouncementService

router = APIRouter(prefix="/announcements", tags=["Announcements & Campus Circulars"])


@router.get("", response_model=StandardResponse[List[AnnouncementItemResponse]])
async def list_announcements(
    db: Annotated[AsyncSession, Depends(get_db)],
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    page: int = Query(1, ge=1),
):
    items = await AnnouncementService.list_announcements(
        db=db,
        category=category,
        search=search,
        limit=limit,
        page=page,
    )
    return StandardResponse(data=items, message="Announcements retrieved successfully")


@router.post("", response_model=StandardResponse[AnnouncementItemResponse], status_code=status.HTTP_201_CREATED)
async def create_announcement(
    request: AnnouncementCreateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role(["ADMIN"]))],
):
    item = await AnnouncementService.create_announcement(
        db=db,
        request=request,
        current_user=current_user,
    )
    return StandardResponse(data=item, message="Announcement created successfully")


@router.delete("/{announcement_id}", response_model=StandardResponse[None])
async def delete_announcement(
    announcement_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role(["ADMIN"]))],
):
    await AnnouncementService.delete_announcement(
        db=db,
        announcement_id=announcement_id,
        current_user=current_user,
    )
    return StandardResponse(data=None, message="Announcement deleted successfully")
