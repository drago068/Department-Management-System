"""
Attendance feature module.
"""
from app.modules.attendance.models import AttendanceRecord, AttendanceSession
from app.modules.attendance.schemas import (
    StudentRosterItem,
    TimetableSlotInfo,
    SessionRosterResponse,
    AttendanceRecordInput,
    AttendanceSubmitRequest,
    AttendanceSubmitResponse,
    SubjectAttendanceItem,
    StudentAttendanceSummaryResponse,
    AttendanceHistoryItem,
    AttendanceHistoryResponse,
)
from app.modules.attendance.service import AttendanceService
from app.modules.attendance.repository import AttendanceRepository
from app.modules.attendance.router import router

__all__ = [
    "AttendanceRecord",
    "AttendanceSession",
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
    "AttendanceService",
    "AttendanceRepository",
    "router",
]
