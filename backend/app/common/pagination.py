"""
Pagination utilities, schemas, and helpers.
"""
from typing import Generic, List, TypeVar
from pydantic import BaseModel, Field
from app.schemas.common import PaginationMetadata, PaginatedData, PaginatedResponse

DataT = TypeVar("DataT")


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number starting from 1")
    limit: int = Field(default=20, ge=1, le=100, description="Items per page (max 100)")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


def build_paginated_response(
    items: List[DataT],
    total_items: int,
    page: int,
    limit: int,
    message: str = "Items retrieved successfully",
) -> PaginatedResponse[DataT]:
    total_pages = (total_items + limit - 1) // limit if limit > 0 else 0
    return PaginatedResponse(
        success=True,
        message=message,
        data=PaginatedData(
            items=items,
            pagination=PaginationMetadata(
                page=page,
                limit=limit,
                total_items=total_items,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_prev=page > 1,
            ),
        ),
    )


__all__ = [
    "PaginationMetadata",
    "PaginatedData",
    "PaginatedResponse",
    "PaginationParams",
    "build_paginated_response",
]
