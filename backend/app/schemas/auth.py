from typing import Optional
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    identifier: str = Field(..., min_length=2, max_length=64, description="Roll No, Faculty ID, or Admin Username")
    password: str = Field(..., min_length=4, max_length=128)
    role: Optional[str] = Field(None, description="STUDENT, STAFF, or ADMIN")


class UserProfileSummary(BaseModel):
    full_name: str
    avatar_url: Optional[str] = None
    department_code: Optional[str] = None
    department_name: Optional[str] = None


class UserAuthResponse(BaseModel):
    id: str
    identifier: str
    role: str
    profile: UserProfileSummary


class TokenResponseData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    user: UserAuthResponse


class RefreshTokenRequest(BaseModel):
    refresh_token: str
