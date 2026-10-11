"""
Faculty and Staff module schemas.
"""
from app.schemas.profile import (
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

__all__ = [
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
]
