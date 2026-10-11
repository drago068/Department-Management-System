"""
User and Admin profile schemas.
"""
from app.schemas.profile import (
    AdminProfileData,
    AdminProfileUpdate,
    DepartmentMini,
)
from app.schemas.auth import UserAuthResponse

# Alias UserResponse for consistency
UserResponse = UserAuthResponse

__all__ = [
    "AdminProfileData",
    "AdminProfileUpdate",
    "DepartmentMini",
    "UserAuthResponse",
    "UserResponse",
]
