"""
Attendance module schemas.
"""
from typing import List
from pydantic import BaseModel
from app.schemas.attendance import (
    StudentRosterItem,
    TimetableSlotInfo,
    SessionRosterResponse,
    AttendanceRecordInput,
    AttendanceSubmitRequest,
    AttendanceSubmitResponse,
    SubjectAttendanceItem,
    StudentAttendanceSummaryResponse,
    AttendanceHistoryItem,
)


class AttendanceHistoryResponse(BaseModel):
    history: List[AttendanceHistoryItem]


__all__ = [
    "StudentRosterItem",
    "TimetableSlotInfo",
    "SessionRosterResponse",
    "AttendanceRecordInput",
    "AttendanceSubmitRequest",
    "AttendanceSubmitResponse",
    "SubjectAttendanceItem",
    "StudentAttendanceSummaryResponse",
    "AttendanceHistoryItem",
    "AttendanceHistoryResponse",
]
