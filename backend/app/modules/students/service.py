"""
Student service layer.
"""
from app.services.user_service import UserService

# Student operations are integrated within UserService
StudentService = UserService

__all__ = ["StudentService"]
