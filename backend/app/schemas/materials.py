from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MaterialItemResponse(BaseModel):
    id: str
    course_id: str
    course_code: str
    course_name: str
    unit: Optional[str] = None
    title: str
    topic: Optional[str] = None
    instructor: str
    material_type: str
    file_format: str
    file_size: str
    page_count: Optional[int] = 0
    reads_count: int = 0
    downloads_count: int = 0
    download_url: str
    created_at: datetime
