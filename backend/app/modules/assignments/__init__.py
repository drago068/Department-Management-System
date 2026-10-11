"""
Assignments feature module.
"""
from app.modules.assignments.schemas import (
    AssignmentItem,
    AssignmentSubmissionRequest,
)
from app.modules.assignments.service import AssignmentService
from app.modules.assignments.repository import AssignmentRepository
from app.modules.assignments.router import router

__all__ = [
    "AssignmentItem",
    "AssignmentSubmissionRequest",
    "AssignmentService",
    "AssignmentRepository",
    "router",
]
