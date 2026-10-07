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
    BulkStudentEnrollRequest,
    BulkStudentEnrollResponse,
    StaffProfileData,
    StaffProfileUpdate,
    StudentEnrollRequest,
    StudentEnrollResponse,
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


@router.get("/cohort-options", response_model=StandardResponse[dict])
async def get_cohort_options(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    options = await UserService.get_cohort_options(db=db)
    return StandardResponse(
        data=options,
        message="Cohort configuration options retrieved successfully",
    )


@router.get("/students/template")
async def download_student_enrollment_template():
    """Download official Excel (.xlsx) template for bulk student enrollment."""
    from fastapi.responses import StreamingResponse
    from app.services.template_service import generate_student_enrollment_template

    excel_stream = generate_student_enrollment_template()
    return StreamingResponse(
        excel_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=nexus_student_enrollment_template.xlsx",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.post("/students", response_model=StandardResponse[StudentEnrollResponse])
async def enroll_student(
    payload: StudentEnrollRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await UserService.enroll_student(db=db, payload=payload)
    return StandardResponse(
        data=result,
        message="Student enrolled successfully",
    )


@router.post("/students/bulk", response_model=StandardResponse[BulkStudentEnrollResponse])
async def bulk_enroll_students(
    payload: BulkStudentEnrollRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await UserService.bulk_enroll_students(db=db, payload=payload)
    return StandardResponse(
        data=result,
        message="Bulk student import processed successfully",
    )


