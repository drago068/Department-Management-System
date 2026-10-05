from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.academic import CourseResponse, DepartmentResponse, PeriodResponse, RoomResponse
from app.schemas.common import StandardResponse
from app.services.academic_service import AcademicService

router = APIRouter(prefix="/academic", tags=["Academic Master Data"])


@router.get("/departments", response_model=StandardResponse[List[DepartmentResponse]])
async def list_departments(db: Annotated[AsyncSession, Depends(get_db)]):
    depts = await AcademicService.get_departments(db)
    items = [
        DepartmentResponse(
            id=str(d.id),
            code=d.code,
            name=d.name,
            is_active=d.is_active,
        )
        for d in depts
    ]
    return StandardResponse(data=items, message="Departments retrieved successfully")


@router.get("/courses", response_model=StandardResponse[List[CourseResponse]])
async def list_courses(
    db: Annotated[AsyncSession, Depends(get_db)],
    department_id: Optional[str] = Query(None),
):
    courses = await AcademicService.get_courses(db, department_id=department_id)
    items = [
        CourseResponse(
            id=str(c.id),
            department_id=str(c.department_id),
            code=c.code,
            name=c.name,
            short_name=c.short_name,
            credits=c.credits,
            course_type=c.course_type,
        )
        for c in courses
    ]
    return StandardResponse(data=items, message="Courses retrieved successfully")


@router.get("/rooms", response_model=StandardResponse[List[RoomResponse]])
async def list_rooms(db: Annotated[AsyncSession, Depends(get_db)]):
    rooms = await AcademicService.get_rooms(db)
    items = [
        RoomResponse(
            id=str(r.id),
            department_id=str(r.department_id) if r.department_id else None,
            room_number=r.room_number,
            building=r.building,
            capacity=r.capacity,
            room_type=r.room_type,
        )
        for r in rooms
    ]
    return StandardResponse(data=items, message="Rooms retrieved successfully")


@router.get("/periods", response_model=StandardResponse[List[PeriodResponse]])
async def list_periods(db: Annotated[AsyncSession, Depends(get_db)]):
    periods = await AcademicService.get_periods(db)
    items = [
        PeriodResponse(
            id=str(p.id),
            period_number=p.period_number,
            name=p.name,
            start_time=p.start_time.strftime("%H:%M"),
            end_time=p.end_time.strftime("%H:%M"),
            is_break=p.is_break,
        )
        for p in periods
    ]
    return StandardResponse(data=items, message="Periods retrieved successfully")
