from datetime import date
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.attendance import (
    AttendanceHistoryItem,
    AttendanceSubmitRequest,
    AttendanceSubmitResponse,
    SessionRosterResponse,
    StudentAttendanceSummaryResponse,
)
from app.schemas.common import StandardResponse
from app.services.attendance_service import AttendanceService

router = APIRouter(prefix="/attendance", tags=["Attendance Management"])


@router.get("/session/students", response_model=StandardResponse[SessionRosterResponse])
async def get_session_roster(
    timetable_entry_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role(["STAFF", "ADMIN"]))],
    marking_date: Optional[date] = Query(None, alias="date"),
):
    target_date = marking_date or date.today()
    roster = await AttendanceService.get_session_roster(
        db=db,
        timetable_entry_id=timetable_entry_id,
        target_date=target_date,
        current_user=current_user,
    )
    return StandardResponse(data=roster, message="Attendance roster loaded")


@router.post("/submit", response_model=StandardResponse[AttendanceSubmitResponse], status_code=status.HTTP_201_CREATED)
async def submit_attendance(
    request: AttendanceSubmitRequest,
    req: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role(["STAFF", "ADMIN"]))],
):
    ip_addr = req.client.host if req.client else None
    result = await AttendanceService.submit_session_attendance(
        db=db,
        request=request,
        current_user=current_user,
        ip_address=ip_addr,
    )
    return StandardResponse(data=result, message="Attendance marked successfully")


@router.get("/student/summary", response_model=StandardResponse[StudentAttendanceSummaryResponse])
async def get_student_attendance_summary(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    student_id: Optional[str] = Query(None),
):
    summary = await AttendanceService.get_student_summary(
        db=db,
        current_user=current_user,
        target_student_id=student_id,
    )
    return StandardResponse(data=summary, message="Student attendance summary calculated")


@router.get("/history", response_model=StandardResponse[List[AttendanceHistoryItem]])
async def get_attendance_history(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role(["ADMIN"]))],
    history_date: Optional[date] = Query(None, alias="date"),
    limit: int = Query(50, ge=1, le=100),
):
    history = await AttendanceService.get_attendance_history(
        db=db,
        date_filter=history_date,
        limit=limit,
    )
    return StandardResponse(data=history, message="Attendance history retrieved")
