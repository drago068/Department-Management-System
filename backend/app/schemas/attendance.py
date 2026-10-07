from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class StudentRosterItem(BaseModel):
    id: str
    register_number: str
    name: str
    default_status: str = "PRESENT"


class TimetableSlotInfo(BaseModel):
    course_name: str
    course_code: str
    section_name: str
    period: str
    room: str
    date: str


class SessionRosterResponse(BaseModel):
    timetable_info: TimetableSlotInfo
    already_submitted: bool
    students: List[StudentRosterItem]


class AttendanceRecordInput(BaseModel):
    student_id: str
    status: str = Field(..., description="PRESENT, ABSENT, or ON_DUTY")


class AttendanceSubmitRequest(BaseModel):
    timetable_entry_id: str
    date: date
    topic_covered: Optional[str] = None
    records: List[AttendanceRecordInput]


class AttendanceSubmitResponse(BaseModel):
    session_id: str
    total_marked: int
    present_count: int
    absent_count: int
    od_count: int
    submitted_at: datetime


class SubjectAttendanceItem(BaseModel):
    course_code: str
    course_name: str
    staff_name: str
    attended_hours: int
    total_hours: int
    percentage: float
    status: str  # EXCELLENT, GOOD, CRITICAL
    max_absences_allowed: int


class StudentAttendanceSummaryResponse(BaseModel):
    overall_percentage: float
    total_attended_hours: int
    total_conducted_hours: int
    benchmark_percentage: float = 75.0
    status: str  # SAFE, WARNING, CRITICAL
    subjects: List[SubjectAttendanceItem]


class AttendanceHistoryItem(BaseModel):
    id: str
    date: str
    day: str
    course_name: str
    course_code: str
    period: str
    present_count: int
    total_count: int
    staff_name: str
    section_name: str
