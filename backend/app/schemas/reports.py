from typing import List
from pydantic import BaseModel


class DefaulterStudentItem(BaseModel):
    student_id: str
    register_number: str
    full_name: str
    section_name: str
    attended_hours: int
    total_hours: int
    percentage: float


class DefaulterReportResponse(BaseModel):
    threshold_percentage: float = 75.0
    defaulters_count: int
    students: List[DefaulterStudentItem]


class FacultyWorkloadItem(BaseModel):
    staff_id: str
    faculty_id: str
    full_name: str
    designation: str
    assigned_courses_count: int
    weekly_lecture_hours: int
    completed_sessions_count: int


class FacultyWorkloadResponse(BaseModel):
    total_faculty: int
    faculty: List[FacultyWorkloadItem]


class DepartmentKpiResponse(BaseModel):
    total_students: int
    total_staff: int
    today_attendance_percentage: float
    students_below_75_count: int
    active_courses_count: int
