"""
Marks module router endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db, get_current_user
from app.common.responses import success_response
from app.models.user import User

router = APIRouter(prefix="/marks", tags=["Marks"])


@router.get("/student/{student_id}")
async def get_student_marks(
    student_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return success_response(
        data={"student_id": student_id, "marks": []},
        message="Marks retrieved successfully",
    )


__all__ = ["router"]
