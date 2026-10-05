from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class StandardResponse(BaseModel, Generic[DataT]):
    success: bool = True
    data: DataT
    message: str = "Operation completed successfully"


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[object] = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail


class PaginationMetadata(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
    total_items: int = 0
    total_pages: int = 0
    has_next: bool = False
    has_prev: bool = False


class PaginatedData(BaseModel, Generic[DataT]):
    items: List[DataT]
    pagination: PaginationMetadata


class PaginatedResponse(StandardResponse[PaginatedData[DataT]], Generic[DataT]):
    pass
