"""
Subjects and Academic courses business service.
"""
from app.services.academic_service import AcademicService

# AcademicService handles course offerings and catalog
SubjectService = AcademicService

__all__ = ["SubjectService"]
