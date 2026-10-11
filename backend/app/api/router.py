"""
Central API Router aggregating all feature modules.
"""
from fastapi import APIRouter

# Import routers from feature modules
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as profiles_router
from app.modules.departments.router import router as academic_router
from app.modules.timetable.router import router as timetable_router
from app.modules.attendance.router import router as attendance_router
from app.modules.materials.router import router as materials_router
from app.modules.announcements.router import router as announcements_router
from app.modules.reports.router import router as reports_router
from app.modules.public.router import router as public_router
from app.modules.marks.router import router as marks_router
from app.modules.assignments.router import router as assignments_router

api_router = APIRouter()

# Register feature module routers
api_router.include_router(auth_router)
api_router.include_router(profiles_router)
api_router.include_router(academic_router)
api_router.include_router(timetable_router)
api_router.include_router(attendance_router)
api_router.include_router(materials_router)
api_router.include_router(announcements_router)
api_router.include_router(reports_router)
api_router.include_router(public_router)
api_router.include_router(marks_router)
api_router.include_router(assignments_router)

__all__ = ["api_router"]
