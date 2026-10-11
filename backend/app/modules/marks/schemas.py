"""
Marks and Assessment schemas.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class MarkItem(BaseModel):
    student_id: str
    course_code: str
    assessment_name: str
    max_marks: float
    obtained_marks: float
    grade: Optional[str] = None


class StudentMarksSummary(BaseModel):
    student_id: str
    register_number: str
    marks: List[MarkItem]
    gpa: Optional[float] = None


__all__ = ["MarkItem", "StudentMarksSummary"]
