"""
Student module schemas.
"""
from app.schemas.profile import (
    StudentProfileData,
    StudentProfileUpdate,
    StudentEnrollRequest,
    StudentEnrollResponse,
    BulkStudentItem,
    BulkStudentEnrollRequest,
    BulkStudentEnrollResponse,
    StudentAllocationItem,
    StudentAllocationResponse,
)

__all__ = [
    "StudentProfileData",
    "StudentProfileUpdate",
    "StudentEnrollRequest",
    "StudentEnrollResponse",
    "BulkStudentItem",
    "BulkStudentEnrollRequest",
    "BulkStudentEnrollResponse",
    "StudentAllocationItem",
    "StudentAllocationResponse",
]
