from typing import Annotated, Any, Optional, Union
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.common import StandardResponse
from app.schemas.profile import (
    AdminProfileData,
    AdminProfileUpdate,
    AssignMentorRequest,
    AutoDistributeMentorsRequest,
    BulkStaffEnrollRequest,
    BulkStaffEnrollResponse,
    BulkStaffItem,
    BulkStudentEnrollRequest,
    BulkStudentEnrollResponse,
    BulkStudentItem,
    FacultyMentorItem,
    StaffEnrollRequest,
    StaffEnrollResponse,
    StaffProfileData,
    StaffProfileUpdate,
    StudentAllocationResponse,
    StudentEnrollRequest,
    StudentEnrollResponse,
    StudentProfileData,
    StudentProfileUpdate,
    UnassignMentorRequest,
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
@router.patch("/me", response_model=StandardResponse[Union[StudentProfileData, StaffProfileData, AdminProfileData]])
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


@router.post("/students/parse-file", response_model=StandardResponse[dict])
async def parse_student_file(
    file: UploadFile = File(...),
):
    """Parse an uploaded Excel (.xlsx, .xls) or CSV student roster and return preview with auto-calculated passwords."""
    from app.services.template_service import parse_student_upload_file

    file_bytes = await file.read()
    result = parse_student_upload_file(file_bytes=file_bytes, filename=file.filename or "roster.xlsx")
    return StandardResponse(
        data=result,
        message=f"Successfully parsed {result.get('valid_count', 0)} students from {file.filename}",
    )


@router.post("/students/upload", response_model=StandardResponse[BulkStudentEnrollResponse])
async def upload_and_bulk_enroll(
    db: Annotated[AsyncSession, Depends(get_db)],
    file: UploadFile = File(...),
    default_department_code: Optional[str] = Form(None),
    default_batch_name: Optional[str] = Form(None),
    default_section_name: Optional[str] = Form(None),
    conflict_strategy: Optional[str] = Form("skip"),
):
    """Directly upload Excel/CSV roster and bulk enroll all students in the database."""
    from app.services.template_service import parse_student_upload_file

    file_bytes = await file.read()
    parsed = parse_student_upload_file(file_bytes=file_bytes, filename=file.filename or "roster.xlsx")
    student_items = [BulkStudentItem(**st) for st in parsed.get("students", [])]

    req = BulkStudentEnrollRequest(
        students=student_items,
        default_department_code=default_department_code,
        default_batch_name=default_batch_name,
        default_section_name=default_section_name,
        conflict_strategy=conflict_strategy or "skip",
    )
    result = await UserService.bulk_enroll_students(db=db, payload=req)
    return StandardResponse(
        data=result,
        message=f"Roster uploaded & imported: {result.enrolled_count} students enrolled, {result.skipped_count} skipped",
    )


# ─────────────────────────────────────────────────────────────
# Staff Onboarding Endpoints
# ─────────────────────────────────────────────────────────────
@router.get("/staff/template")
async def download_staff_enrollment_template():
    """Download official Excel (.xlsx) template for bulk staff onboarding."""
    from fastapi.responses import StreamingResponse
    from app.services.template_service import generate_staff_enrollment_template

    excel_stream = generate_staff_enrollment_template()
    return StreamingResponse(
        excel_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=nexus_staff_onboarding_template.xlsx",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.post("/staff", response_model=StandardResponse[StaffEnrollResponse])
async def enroll_staff(
    payload: StaffEnrollRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Enroll single faculty member and provision STAFF identity."""
    result = await UserService.enroll_staff(db=db, payload=payload)
    return StandardResponse(
        data=result,
        message="Faculty registered successfully",
    )


@router.post("/staff/bulk", response_model=StandardResponse[BulkStaffEnrollResponse])
async def bulk_enroll_staff(
    payload: BulkStaffEnrollRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Bulk import faculty members from structured list."""
    result = await UserService.bulk_enroll_staff(db=db, payload=payload)
    return StandardResponse(
        data=result,
        message="Bulk faculty import completed successfully",
    )


@router.post("/staff/upload", response_model=StandardResponse[BulkStaffEnrollResponse])
async def upload_and_bulk_enroll_staff(
    db: Annotated[AsyncSession, Depends(get_db)],
    file: UploadFile = File(...),
    default_department_code: Optional[str] = Form(None),
    conflict_strategy: Optional[str] = Form("skip"),
):
    """Directly upload Excel/CSV roster and bulk enroll all faculty in the database."""
    from app.services.template_service import parse_staff_upload_file

    file_bytes = await file.read()
    parsed = parse_staff_upload_file(file_bytes=file_bytes, filename=file.filename or "faculty_roster.xlsx")
    staff_items = [BulkStaffItem(**st) for st in parsed.get("staff", [])]

    req = BulkStaffEnrollRequest(
        staff_members=staff_items,
        default_department_code=default_department_code,
        conflict_strategy=conflict_strategy or "skip",
    )
    result = await UserService.bulk_enroll_staff(db=db, payload=req)
    return StandardResponse(
        data=result,
        message=f"Faculty roster processed: {result.enrolled_count} registered, {result.skipped_count} skipped",
    )


@router.get("/staff", response_model=StandardResponse[list])
async def list_all_staff(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get all active faculty members."""
    staff_list = await UserService.get_all_staff(db=db)
    return StandardResponse(
        data=staff_list,
        message="Staff roster retrieved successfully",
    )


# ─────────────────────────────────────────────────────────────
# Mentor & Proctor Allocation Endpoints
# ─────────────────────────────────────────────────────────────
@router.get("/staff/mentors", response_model=StandardResponse[list[FacultyMentorItem]])
async def get_faculty_mentors(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get active faculty members with their current mentee count and capacity."""
    mentors = await UserService.get_faculty_mentors(db=db)
    return StandardResponse(
        data=mentors,
        message="Faculty mentors retrieved successfully",
    )


@router.get("/students/allocation", response_model=StandardResponse[StudentAllocationResponse])
async def get_student_allocation(
    db: Annotated[AsyncSession, Depends(get_db)],
    department: Optional[str] = None,
    batch: Optional[str] = None,
    section: Optional[str] = None,
    status: Optional[str] = "all",
    search: Optional[str] = None,
):
    """Get students for mentor allocation with filtering by dept, batch, section, and status."""
    result = await UserService.get_student_allocation(
        db=db,
        department_name=department,
        batch_name=batch,
        section_name=section,
        status_filter=status,
        search=search,
    )
    return StandardResponse(
        data=result,
        message="Student allocation list retrieved successfully",
    )


@router.patch("/students/assign-mentor", response_model=StandardResponse[dict])
async def assign_student_mentor(
    payload: AssignMentorRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Assign selected students to target faculty mentor."""
    result = await UserService.assign_mentor(db=db, payload=payload)
    return StandardResponse(
        data=result,
        message=result.get("message", "Mentor assigned successfully"),
    )


@router.patch("/students/unassign-mentor", response_model=StandardResponse[dict])
async def unassign_student_mentor(
    payload: UnassignMentorRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Remove mentor assignment from selected students."""
    result = await UserService.unassign_mentor(db=db, payload=payload)
    return StandardResponse(
        data=result,
        message=result.get("message", "Mentor unassigned successfully"),
    )


@router.post("/students/auto-distribute-mentors", response_model=StandardResponse[dict])
async def auto_distribute_student_mentors(
    payload: AutoDistributeMentorsRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Auto distribute unassigned students across faculty members with available capacity."""
    result = await UserService.auto_distribute_mentors(db=db, payload=payload)
    return StandardResponse(
        data=result,
        message=result.get("message", "Auto-distribution completed successfully"),
    )



