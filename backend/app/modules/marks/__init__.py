"""
Marks feature module.
"""
from app.modules.marks.schemas import MarkItem, StudentMarksSummary
from app.modules.marks.service import MarksService
from app.modules.marks.repository import MarksRepository
from app.modules.marks.router import router

__all__ = [
    "MarkItem",
    "StudentMarksSummary",
    "MarksService",
    "MarksRepository",
    "router",
]
