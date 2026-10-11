"""
Role-based access control and permission checking utilities.
"""
from typing import Annotated, List, Union
from fastapi import Depends
from app.core.dependencies import get_current_user, require_role
from app.core.exceptions import ForbiddenException
from app.models.user import User


class RoleChecker:
    """
    Dependency callable that validates if the authenticated user has one of the required roles.
    """

    def __init__(self, allowed_roles: Union[str, List[str]]):
        if isinstance(allowed_roles, str):
            self.allowed_roles = [allowed_roles]
        else:
            self.allowed_roles = allowed_roles

    async def __call__(
        self, current_user: Annotated[User, Depends(get_current_user)]
    ) -> User:
        if current_user.role not in self.allowed_roles:
            raise ForbiddenException(
                f"Access denied. Requires one of roles: {', '.join(self.allowed_roles)}. "
                f"Your role is {current_user.role}."
            )
        return current_user


def require_roles(roles: List[str]):
    """Convenience alias for require_role matching standard RBAC conventions."""
    return require_role(roles)


__all__ = [
    "RoleChecker",
    "require_role",
    "require_roles",
]
