"""
Common standardized API response envelopes and response builders.
"""
from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel
from app.schemas.common import StandardResponse, ErrorDetail, ErrorResponse

DataT = TypeVar("DataT")

# Alias APIResponse to StandardResponse for target architecture consistency
APIResponse = StandardResponse


def success_response(
    data: Any,
    message: str = "Operation completed successfully",
) -> StandardResponse:
    return StandardResponse(success=True, data=data, message=message)


def error_response(
    code: str,
    message: str,
    details: Optional[Any] = None,
) -> ErrorResponse:
    return ErrorResponse(
        success=False,
        error=ErrorDetail(code=code, message=message, details=details),
    )


__all__ = [
    "StandardResponse",
    "APIResponse",
    "ErrorDetail",
    "ErrorResponse",
    "success_response",
    "error_response",
]
