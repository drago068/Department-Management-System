"""
API-level dependencies combining authentication, database session, and authorization.
"""
from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    get_optional_user,
    require_role,
    oauth2_scheme,
)
from app.core.permissions import require_roles, RoleChecker

__all__ = [
    "get_db",
    "get_current_user",
    "get_optional_user",
    "require_role",
    "require_roles",
    "RoleChecker",
    "oauth2_scheme",
]
