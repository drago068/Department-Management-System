"""
Authentication module schemas.
"""
from app.schemas.auth import (
    LoginRequest,
    UserProfileSummary,
    UserAuthResponse,
    TokenResponseData,
    RefreshTokenRequest,
)

# Provide TokenResponse alias for standard schema conventions
TokenResponse = TokenResponseData

__all__ = [
    "LoginRequest",
    "UserProfileSummary",
    "UserAuthResponse",
    "TokenResponseData",
    "TokenResponse",
    "RefreshTokenRequest",
]
