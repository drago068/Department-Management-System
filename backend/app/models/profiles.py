import uuid
from datetime import date
from typing import Optional
from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    department_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("departments.id"), nullable=False, index=True)
    batch_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("batches.id"), nullable=False, index=True)
    section_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("sections.id"), nullable=False, index=True)
    faculty_mentor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, ForeignKey("staff.id", ondelete="SET NULL"), nullable=True)

    roll_number: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    register_number: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    parent_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    parent_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    blood_group: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    cgpa: Mapped[float] = mapped_column(Numeric(3, 2), default=0.00, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    user = relationship("User", back_populates="student_profile")
    department = relationship("Department", back_populates="students")
    batch = relationship("Batch", back_populates="students")
    section = relationship("Section", back_populates="students")
    faculty_mentor = relationship("Staff", foreign_keys=[faculty_mentor_id], back_populates="mentored_students")
    attendance_records = relationship("AttendanceRecord", back_populates="student")


class Staff(Base):
    __tablename__ = "staff"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    department_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("departments.id"), nullable=False, index=True)

    faculty_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    designation: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    cabin_number: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    qualifications: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    experience: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    user = relationship("User", back_populates="staff_profile")
    department = relationship("Department", back_populates="staff")
    mentored_students = relationship("Student", foreign_keys=[Student.faculty_mentor_id], back_populates="faculty_mentor")
    timetable_entries = relationship("TimetableEntry", back_populates="staff")
    course_offerings = relationship("CourseOffering", back_populates="staff")
    materials = relationship("Material", back_populates="staff")


class AdminProfile(Base):
    __tablename__ = "admin_profiles"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, ForeignKey("departments.id"), nullable=True)

    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    designation: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    office_location: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    user = relationship("User", back_populates="admin_profile")
