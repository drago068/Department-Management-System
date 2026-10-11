"""
Students feature module.
"""
from app.modules.students.models import Student
from app.modules.students.schemas import (
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
from app.modules.students.service import StudentService
from app.modules.students.repository import StudentRepository
from app.modules.students.router import router

__all__ = [
    "Student",
    "StudentProfileData",
    "StudentProfileUpdate",
    "StudentEnrollRequest",
    "StudentEnrollResponse",
    "BulkStudentItem",
    "BulkStudentEnrollRequest",
    "BulkStudentEnrollResponse",
    "StudentAllocationItem",
    "StudentAllocationResponse",
    "StudentService",
    "StudentRepository",
    "router",
]
