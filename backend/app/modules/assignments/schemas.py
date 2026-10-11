"""
Assignment schemas.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class AssignmentItem(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    course_code: str
    due_date: datetime
    total_marks: float
    status: str = "PENDING"


class AssignmentSubmissionRequest(BaseModel):
    assignment_id: str
    submission_notes: Optional[str] = None
    file_url: Optional[str] = None


__all__ = ["AssignmentItem", "AssignmentSubmissionRequest"]
