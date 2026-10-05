import uuid
from datetime import time
from typing import Optional
from sqlalchemy import Boolean, ForeignKey, Integer, String, Time, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    department_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("departments.id"), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    short_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    credits: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    course_type: Mapped[str] = mapped_column(String(32), default="THEORY", nullable=False)  # THEORY, LAB, ELECTIVE
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    department = relationship("Department", back_populates="courses")
    course_offerings = relationship("CourseOffering", back_populates="course")
    timetable_entries = relationship("TimetableEntry", back_populates="course")
    materials = relationship("Material", back_populates="course")


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, ForeignKey("departments.id"), nullable=True)
    room_number: Mapped[str] = mapped_column(String(32), nullable=False)  # e.g., 'Room 204'
    building: Mapped[str] = mapped_column(String(64), nullable=False)     # e.g., 'Theory Wing'
    capacity: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    room_type: Mapped[str] = mapped_column(String(32), default="CLASSROOM", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    department = relationship("Department", back_populates="rooms")
    timetable_entries = relationship("TimetableEntry", back_populates="room")


class Period(Base):
    __tablename__ = "periods"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    period_number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(32), nullable=False)  # 'P1', 'Morning Tea Break'
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    is_break: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    timetable_entries = relationship("TimetableEntry", back_populates="period")


class CourseOffering(Base):
    __tablename__ = "course_offerings"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    course_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("courses.id"), nullable=False, index=True)
    staff_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("staff.id"), nullable=False, index=True)
    section_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("sections.id"), nullable=False, index=True)
    semester_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("semesters.id"), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    course = relationship("Course", back_populates="course_offerings")
    staff = relationship("Staff", back_populates="course_offerings")
    section = relationship("Section", back_populates="course_offerings")
    semester = relationship("Semester", back_populates="course_offerings")
