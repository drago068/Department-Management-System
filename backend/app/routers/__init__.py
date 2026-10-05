from app.routers.auth import router as auth_router
from app.routers.profiles import router as profiles_router
from app.routers.academic import router as academic_router
from app.routers.timetable import router as timetable_router
from app.routers.attendance import router as attendance_router
from app.routers.materials import router as materials_router
from app.routers.announcements import router as announcements_router
from app.routers.reports import router as reports_router
from app.routers.public import router as public_router

__all__ = [
    "auth_router",
    "profiles_router",
    "academic_router",
    "timetable_router",
    "attendance_router",
    "materials_router",
    "announcements_router",
    "reports_router",
    "public_router",
]
