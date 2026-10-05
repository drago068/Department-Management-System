from contextlib import asynccontextmanager
import os
import time
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.database import engine
from app.core.exceptions import register_exception_handlers
from app.models.base import Base
import app.models  # Ensure all models are registered in metadata
from app.routers import (
    academic_router,
    announcements_router,
    attendance_router,
    auth_router,
    materials_router,
    profiles_router,
    public_router,
    reports_router,
    timetable_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure tables are created and upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: Dispose engine connection pool
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Exception Handlers
register_exception_handlers(app)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_and_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = request_id
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    response.headers["X-Request-ID"] = request_id
    return response


# Health & Info Endpoints
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
            "version": "1.0.0",
        },
        "message": "CMS Backend API is active",
    }


@app.get("/", tags=["System"])
async def root():
    return {
        "success": True,
        "data": {
            "name": settings.PROJECT_NAME,
            "version": "1.0.0",
            "documentation": "/docs",
        },
        "message": "Welcome to Nexus CMS Backend API",
    }


# Include Routers with API Prefix
api_prefix = settings.API_V1_STR
app.include_router(auth_router, prefix=api_prefix)
app.include_router(profiles_router, prefix=api_prefix)
app.include_router(academic_router, prefix=api_prefix)
app.include_router(timetable_router, prefix=api_prefix)
app.include_router(attendance_router, prefix=api_prefix)
app.include_router(materials_router, prefix=api_prefix)
app.include_router(announcements_router, prefix=api_prefix)
app.include_router(reports_router, prefix=api_prefix)
app.include_router(public_router, prefix=api_prefix)
