"""
Faculty feature module.
"""
from app.modules.faculty.models import Staff
from app.modules.faculty.schemas import (
    StaffProfileData,
    StaffProfileUpdate,
    StaffEnrollRequest,
    StaffEnrollResponse,
    BulkStaffEnrollRequest,
    BulkStaffEnrollResponse,
    BulkStaffItem,
    FacultyMentorItem,
    MentorMini,
    AssignMentorRequest,
    UnassignMentorRequest,
    AutoDistributeMentorsRequest,
)
from app.modules.faculty.service import FacultyService
from app.modules.faculty.repository import FacultyRepository
from app.modules.faculty.router import router

__all__ = [
    "Staff",
    "StaffProfileData",
    "StaffProfileUpdate",
    "StaffEnrollRequest",
    "StaffEnrollResponse",
    "BulkStaffEnrollRequest",
    "BulkStaffEnrollResponse",
    "BulkStaffItem",
    "FacultyMentorItem",
    "MentorMini",
    "AssignMentorRequest",
    "UnassignMentorRequest",
    "AutoDistributeMentorsRequest",
    "FacultyService",
    "FacultyRepository",
    "router",
]
