import uuid
from datetime import datetime
from typing import Any, Optional
from sqlalchemy import DateTime, ForeignKey, JSON, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(64), nullable=False, index=True)  # ATTENDANCE_SUBMIT, TIMETABLE_UPDATE
    entity_name: Mapped[str] = mapped_column(String(64), nullable=False)        # attendance_sessions, timetable_entries
    entity_id: Mapped[str] = mapped_column(String(64), nullable=False)
    details: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    user = relationship("User")
