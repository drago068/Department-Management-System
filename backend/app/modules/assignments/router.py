"""
Assignments router endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db, get_current_user
from app.common.responses import success_response
from app.models.user import User

router = APIRouter(prefix="/assignments", tags=["Assignments"])


@router.get("/")
async def list_assignments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return success_response(
        data=[],
        message="Assignments retrieved successfully",
    )


__all__ = ["router"]
