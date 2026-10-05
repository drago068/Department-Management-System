import uuid
from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(16), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    batches = relationship("Batch", back_populates="department")
    courses = relationship("Course", back_populates="department")
    staff = relationship("Staff", back_populates="department")
    rooms = relationship("Room", back_populates="department")
    students = relationship("Student", back_populates="department")


class AcademicYear(Base):
    __tablename__ = "academic_years"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    year_name: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)  # e.g., '2024-2025'
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    semesters = relationship("Semester", back_populates="academic_year")


class Semester(Base):
    __tablename__ = "semesters"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    academic_year_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("academic_years.id"), nullable=False, index=True)
    semester_number: Mapped[int] = mapped_column(Integer, nullable=False)  # 1 to 8
    term_type: Mapped[str] = mapped_column(String(16), nullable=False)  # ODD, EVEN
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    academic_year = relationship("AcademicYear", back_populates="semesters")
    course_offerings = relationship("CourseOffering", back_populates="semester")


class Batch(Base):
    __tablename__ = "batches"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    department_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("departments.id"), nullable=False, index=True)
    batch_name: Mapped[str] = mapped_column(String(32), nullable=False)  # e.g., '2022-2026'
    admission_year: Mapped[int] = mapped_column(Integer, nullable=False)
    graduation_year: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    department = relationship("Department", back_populates="batches")
    sections = relationship("Section", back_populates="batch")
    students = relationship("Student", back_populates="batch")


class Section(Base):
    __tablename__ = "sections"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    batch_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("batches.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(16), nullable=False)  # e.g., 'A', 'B'
    current_semester: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    batch = relationship("Batch", back_populates="sections")
    students = relationship("Student", back_populates="section")
    timetable_entries = relationship("TimetableEntry", back_populates="section")
    course_offerings = relationship("CourseOffering", back_populates="section")
