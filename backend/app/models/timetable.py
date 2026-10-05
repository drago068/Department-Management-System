import uuid
from typing import Optional
from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class TimetableEntry(Base):
    __tablename__ = "timetable_entries"
    __table_args__ = (
        UniqueConstraint("room_id", "day_of_week", "period_id", name="uq_room_day_period"),
        UniqueConstraint("staff_id", "day_of_week", "period_id", name="uq_staff_day_period"),
        UniqueConstraint("section_id", "day_of_week", "period_id", name="uq_section_day_period"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    section_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("sections.id"), nullable=False, index=True)
    course_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("courses.id"), nullable=False, index=True)
    staff_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("staff.id"), nullable=False, index=True)
    room_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("rooms.id"), nullable=False, index=True)
    period_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("periods.id"), nullable=False, index=True)

    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False, index=True)  # 1=Monday to 6=Saturday
    lecture_type: Mapped[str] = mapped_column(String(32), default="THEORY", nullable=False)  # THEORY, LAB, TUTORIAL
    batch_split: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)  # 'Batch 1', 'Batch 2'
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    section = relationship("Section", back_populates="timetable_entries")
    course = relationship("Course", back_populates="timetable_entries")
    staff = relationship("Staff", back_populates="timetable_entries")
    room = relationship("Room", back_populates="timetable_entries")
    period = relationship("Period", back_populates="timetable_entries")
    attendance_sessions = relationship("AttendanceSession", back_populates="timetable_entry")
