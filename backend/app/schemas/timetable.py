from typing import List, Optional
from pydantic import BaseModel, Field


class TimetableSlotItem(BaseModel):
    id: str
    period_number: int
    period_name: str
    start_time: str
    end_time: str
    is_break: bool
    title: Optional[str] = None  # for break titles like "Morning Tea Break & Refreshment"
    course_code: Optional[str] = None
    course_name: Optional[str] = None
    short_name: Optional[str] = None
    lecture_type: Optional[str] = None
    room: Optional[str] = None
    faculty_name: Optional[str] = None
    section_name: Optional[str] = None
    status: str = "UPCOMING"  # COMPLETED, IN_PROGRESS, UPCOMING
    attendance_status: Optional[str] = None  # MARKED, PENDING
    batch_split: Optional[str] = None


class TimetableScheduleResponse(BaseModel):
    day_of_week: int
    day_name: str
    schedule: List[TimetableSlotItem]


class TimetableEntryCreate(BaseModel):
    section_id: str
    course_id: str
    staff_id: str
    room_id: str
    period_id: str
    day_of_week: int = Field(..., ge=1, le=6, description="1=Monday to 6=Saturday")
    lecture_type: str = "THEORY"
    batch_split: Optional[str] = None


class TimetableEntryUpdate(BaseModel):
    course_id: Optional[str] = None
    staff_id: Optional[str] = None
    room_id: Optional[str] = None
    period_id: Optional[str] = None
    day_of_week: Optional[int] = Field(None, ge=1, le=6)
    lecture_type: Optional[str] = None
    batch_split: Optional[str] = None
