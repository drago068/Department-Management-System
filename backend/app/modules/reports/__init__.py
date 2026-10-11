"""
Reports feature module.
"""
from app.modules.reports.schemas import (
    DefaulterStudentItem,
    DefaulterReportResponse,
    FacultyWorkloadItem,
    FacultyWorkloadResponse,
    DepartmentKpiResponse,
)
from app.modules.reports.service import ReportService
from app.modules.reports.repository import ReportRepository
from app.modules.reports.router import router

__all__ = [
    "DefaulterStudentItem",
    "DefaulterReportResponse",
    "FacultyWorkloadItem",
    "FacultyWorkloadResponse",
    "DepartmentKpiResponse",
    "ReportService",
    "ReportRepository",
    "router",
]
