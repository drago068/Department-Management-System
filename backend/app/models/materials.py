import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Material(Base):
    __tablename__ = "materials"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    course_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("courses.id"), nullable=False, index=True)
    uploaded_by: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("staff.id"), nullable=False, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    unit: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)  # 'Unit 1'
    topic: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    material_type: Mapped[str] = mapped_column(String(32), default="LECTURE_NOTE", nullable=False)  # LECTURE_NOTE, QUESTION_BANK, LAB_MANUAL, SYLLABUS

    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    file_format: Mapped[str] = mapped_column(String(16), default="PDF", nullable=False)  # PDF, DOCX
    file_size_bytes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    page_count: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)

    reads_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    downloads_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    course = relationship("Course", back_populates="materials")
    staff = relationship("Staff", back_populates="materials")
    downloads = relationship("MaterialDownload", back_populates="material", cascade="all, delete-orphan")


class MaterialDownload(Base):
    __tablename__ = "material_downloads"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    material_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("materials.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False, index=True)
    downloaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    material = relationship("Material", back_populates="downloads")
    user = relationship("User")
