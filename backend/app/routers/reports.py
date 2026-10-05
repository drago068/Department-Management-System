from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.user import User
from app.schemas.common import StandardResponse
from app.schemas.reports import (
    DefaulterReportResponse,
    DepartmentKpiResponse,
    FacultyWorkloadResponse,
)
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Institutional Reports & Analytics"])


@router.get("/attendance/defaulters", response_model=StandardResponse[DefaulterReportResponse])
async def get_attendance_defaulters(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role(["ADMIN"]))],
    threshold: float = Query(75.0, ge=0.0, le=100.0),
    section_id: Optional[str] = Query(None),
):
    report = await ReportService.get_defaulters_report(
        db=db,
        threshold=threshold,
        section_id=section_id,
    )
    return StandardResponse(data=report, message="Defaulters report compiled successfully")


@router.get("/faculty/workload", response_model=StandardResponse[FacultyWorkloadResponse])
async def get_faculty_workload(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role(["STAFF", "ADMIN"]))],
):
    workload = await ReportService.get_faculty_workload(db=db)
    return StandardResponse(data=workload, message="Faculty workload summary generated")


@router.get("/department/summary", response_model=StandardResponse[DepartmentKpiResponse])
async def get_department_summary(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role(["ADMIN"]))],
):
    summary = await ReportService.get_department_kpis(db=db)
    return StandardResponse(data=summary, message="Department KPIs compiled successfully")
