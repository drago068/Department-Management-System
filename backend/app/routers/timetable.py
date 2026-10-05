from typing import Annotated, List, Optional
import uuid
from datetime import date
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role
from app.core.exceptions import NotFoundException
from app.models.timetable import TimetableEntry
from app.models.user import User
from app.schemas.common import StandardResponse
from app.schemas.timetable import (
    TimetableEntryCreate,
    TimetableScheduleResponse,
)
from app.services.audit_service import AuditService
from app.services.timetable_service import TimetableService

router = APIRouter(prefix="/timetable", tags=["Timetable"])


@router.get("/student", response_model=StandardResponse[TimetableScheduleResponse])
async def get_student_timetable(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role(["STUDENT", "ADMIN"]))],
    day_of_week: Optional[int] = Query(None, ge=1, le=6),
):
    schedule = await TimetableService.get_student_schedule(db=db, current_user=current_user, day_of_week=day_of_week)
    return StandardResponse(data=schedule, message="Student timetable retrieved successfully")


@router.get("/staff", response_model=StandardResponse[TimetableScheduleResponse])
async def get_staff_timetable(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role(["STAFF", "ADMIN"]))],
    day_of_week: Optional[int] = Query(None, ge=1, le=6),
):
    schedule = await TimetableService.get_staff_schedule(db=db, current_user=current_user, day_of_week=day_of_week)
    return StandardResponse(data=schedule, message="Staff schedule retrieved successfully")


@router.get("/today", response_model=StandardResponse[TimetableScheduleResponse])
async def get_today_schedule(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Role-agnostic endpoint: returns today's schedule for the logged-in user."""
    today_dow = date.today().isoweekday()  # 1=Mon … 7=Sun
    if current_user.role in ("STAFF", "ADMIN"):
        schedule = await TimetableService.get_staff_schedule(
            db=db, current_user=current_user, day_of_week=today_dow
        )
    else:
        schedule = await TimetableService.get_student_schedule(
            db=db, current_user=current_user, day_of_week=today_dow
        )
    return StandardResponse(data=schedule, message="Today's schedule retrieved")


@router.get("/weekly", response_model=StandardResponse[TimetableScheduleResponse])
async def get_weekly_schedule(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Role-agnostic endpoint: returns the full weekly timetable."""
    if current_user.role in ("STAFF", "ADMIN"):
        schedule = await TimetableService.get_staff_schedule(db=db, current_user=current_user)
    else:
        schedule = await TimetableService.get_student_schedule(db=db, current_user=current_user)
    return StandardResponse(data=schedule, message="Weekly timetable retrieved")


@router.post("/entries", response_model=StandardResponse[dict], status_code=status.HTTP_201_CREATED)
async def create_timetable_entry(
    entry_data: TimetableEntryCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role(["ADMIN"]))],
):
    new_entry = await TimetableService.create_entry_with_conflict_check(
        db=db,
        entry_data=entry_data,
        acting_user_id=current_user.id,
    )
    return StandardResponse(
        data={"id": str(new_entry.id), "message": "Timetable entry created with zero conflict."},
        message="Timetable entry scheduled successfully",
    )


@router.delete("/entries/{entry_id}", response_model=StandardResponse[None])
async def delete_timetable_entry(
    entry_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role(["ADMIN"]))],
):
    entry_uuid = uuid.UUID(entry_id)
    entry = (await db.execute(select(TimetableEntry).where(TimetableEntry.id == entry_uuid))).scalar_one_or_none()
    if not entry:
        raise NotFoundException("Timetable entry not found")

    entry.is_active = False
    await AuditService.log_action(
        db=db,
        action="TIMETABLE_DELETE",
        entity_name="timetable_entries",
        entity_id=str(entry.id),
        user_id=current_user.id,
    )
    await db.commit()
    return StandardResponse(data=None, message="Timetable slot removed successfully")
