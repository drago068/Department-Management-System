import uuid
from datetime import date, datetime
from typing import Optional
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, UniqueConstraint, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class AttendanceSession(Base):
    __tablename__ = "attendance_sessions"
    __table_args__ = (
        UniqueConstraint("timetable_entry_id", "date", name="uq_timetable_session_date"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    timetable_entry_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("timetable_entries.id"), nullable=False, index=True)
    staff_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("staff.id"), nullable=False, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    conducted_hours: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    topic_covered: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    present_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    absent_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    od_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_marked: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    timetable_entry = relationship("TimetableEntry", back_populates="attendance_sessions")
    staff = relationship("Staff")
    records = relationship("AttendanceRecord", back_populates="session", cascade="all, delete-orphan")


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    __table_args__ = (
        UniqueConstraint("attendance_session_id", "student_id", name="uq_session_student"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    attendance_session_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("attendance_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("students.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False)  # PRESENT, ABSENT, ON_DUTY
    remarks: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    marked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    session = relationship("AttendanceSession", back_populates="records")
    student = relationship("Student", back_populates="attendance_records")
