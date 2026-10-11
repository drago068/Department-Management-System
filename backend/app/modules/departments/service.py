"""
Department and Organization business service.
"""
from app.services.academic_service import AcademicService

# AcademicService provides department and organizational unit queries
DepartmentService = AcademicService

__all__ = ["DepartmentService"]
