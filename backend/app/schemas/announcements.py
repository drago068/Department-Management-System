from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class AnnouncementItemResponse(BaseModel):
    id: str
    category: str
    reference_number: Optional[str] = None
    title: str
    heading: Optional[str] = None
    content: str
    department: Optional[str] = None
    date: str
    tag: Optional[str] = None
    badge: Optional[str] = None
    badge_type: Optional[str] = "blue"
    footer: Optional[str] = None
    publish_date: str
    expires_at: Optional[datetime] = None


class AnnouncementCreateRequest(BaseModel):
    title: str
    heading: Optional[str] = None
    content: str
    category: str = "academic"
    target_role: str = "ALL"
    reference_number: Optional[str] = None
    tag: Optional[str] = None
    badge: Optional[str] = None
    badge_type: Optional[str] = "blue"
    department_name: Optional[str] = None
    footer: Optional[str] = None
    publish_date: Optional[date] = None
    expires_at: Optional[datetime] = None
