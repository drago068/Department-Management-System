import uuid
from datetime import date, datetime
from typing import Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Announcement(Base):
    __tablename__ = "announcements"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    heading: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    category: Mapped[str] = mapped_column(String(64), default="academic", nullable=False, index=True)  # coe, placement, academic, events
    target_role: Mapped[str] = mapped_column(String(20), default="ALL", nullable=False)               # ALL, STUDENT, STAFF

    reference_number: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)  # 'CIR/SCE/2024-25/089'
    tag: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)               # 'Autonomous'
    badge: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)             # 'CoE'
    badge_type: Mapped[Optional[str]] = mapped_column(String(32), default="blue", nullable=True)
    department_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)  # 'Controller of Examinations'
    footer: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)           # 'Signed by Dr. K. Ramanathan'

    publish_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    author = relationship("User")
    recipients = relationship("AnnouncementRecipient", back_populates="announcement", cascade="all, delete-orphan")


class AnnouncementRecipient(Base):
    __tablename__ = "announcement_recipients"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    announcement_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("announcements.id", ondelete="CASCADE"), nullable=False, index=True)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, ForeignKey("departments.id", ondelete="CASCADE"), nullable=True)
    batch_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, ForeignKey("batches.id", ondelete="CASCADE"), nullable=True)
    section_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, ForeignKey("sections.id", ondelete="CASCADE"), nullable=True)

    # Relationships
    announcement = relationship("Announcement", back_populates="recipients")
    department = relationship("Department")
    batch = relationship("Batch")
    section = relationship("Section")
