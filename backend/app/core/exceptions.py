from typing import Any, Optional
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class AppException(Exception):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        code: str = "BAD_REQUEST",
        message: str = "An error occurred",
        details: Optional[Any] = None,
    ):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found", details: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="RESOURCE_NOT_FOUND",
            message=message,
            details=details,
        )


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Authentication required", details: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="UNAUTHORIZED",
            message=message,
            details=details,
        )


class ForbiddenException(AppException):
    def __init__(self, message: str = "Access forbidden", details: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="FORBIDDEN",
            message=message,
            details=details,
        )


class ConflictException(AppException):
    def __init__(self, message: str = "Resource conflict detected", code: str = "CONFLICT", details: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code=code,
            message=message,
            details=details,
        )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details,
                },
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        code = "HTTP_ERROR"
        if exc.status_code == status.HTTP_401_UNAUTHORIZED:
            code = "UNAUTHORIZED"
        elif exc.status_code == status.HTTP_403_FORBIDDEN:
            code = "FORBIDDEN"
        elif exc.status_code == status.HTTP_404_NOT_FOUND:
            code = "NOT_FOUND"

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": code,
                    "message": exc.detail if isinstance(exc.detail, str) else "HTTP exception occurred",
                    "details": exc.detail if not isinstance(exc.detail, str) else None,
                },
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        formatted_errors = []
        for err in exc.errors():
            loc = " -> ".join(str(item) for item in err.get("loc", []))
            formatted_errors.append({"location": loc, "message": err.get("msg")})

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid request parameters",
                    "details": formatted_errors,
                },
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected server error occurred.",
                    "details": str(exc) if request.app.debug else None,
                },
            },
        )
