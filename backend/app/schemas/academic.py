from datetime import date, time
from typing import Optional
from pydantic import BaseModel


class DepartmentResponse(BaseModel):
    id: str
    code: str
    name: str
    is_active: bool


class AcademicYearResponse(BaseModel):
    id: str
    year_name: str
    start_date: date
    end_date: date
    is_current: bool


class SemesterResponse(BaseModel):
    id: str
    academic_year_id: str
    semester_number: int
    term_type: str
    start_date: date
    end_date: date
    is_current: bool


class BatchResponse(BaseModel):
    id: str
    department_id: str
    batch_name: str
    admission_year: int
    graduation_year: int


class SectionResponse(BaseModel):
    id: str
    batch_id: str
    name: str
    current_semester: int


class CourseResponse(BaseModel):
    id: str
    department_id: str
    code: str
    name: str
    short_name: Optional[str] = None
    credits: int
    course_type: str


class RoomResponse(BaseModel):
    id: str
    department_id: Optional[str] = None
    room_number: str
    building: str
    capacity: int
    room_type: str


class PeriodResponse(BaseModel):
    id: str
    period_number: int
    name: str
    start_time: str
    end_time: str
    is_break: bool
