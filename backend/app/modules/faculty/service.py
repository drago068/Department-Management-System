"""
Faculty and Staff business service layer.
"""
from app.services.user_service import UserService

# Staff and mentor allocation services are provided by UserService
FacultyService = UserService

__all__ = ["FacultyService"]
