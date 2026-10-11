"""
Departments feature module.
"""
from app.modules.departments.models import (
    Department,
    AcademicYear,
    Semester,
    Batch,
    Section,
)
from app.modules.departments.schemas import (
    DepartmentResponse,
    AcademicYearResponse,
    SemesterResponse,
    BatchResponse,
    SectionResponse,
)
from app.modules.departments.service import DepartmentService
from app.modules.departments.repository import DepartmentRepository
from app.modules.departments.router import router

__all__ = [
    "Department",
    "AcademicYear",
    "Semester",
    "Batch",
    "Section",
    "DepartmentResponse",
    "AcademicYearResponse",
    "SemesterResponse",
    "BatchResponse",
    "SectionResponse",
    "DepartmentService",
    "DepartmentRepository",
    "router",
]
