from datetime import date, datetime, timezone
import math
from typing import List, Optional
import uuid
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.exceptions import ConflictException, ForbiddenException, NotFoundException
from app.models.academics import Course, Period, Room
from app.models.attendance import AttendanceRecord, AttendanceSession
from app.models.organization import Section
from app.models.profiles import Staff, Student
from app.models.timetable import TimetableEntry
from app.models.user import User
from app.schemas.attendance import (
    AttendanceHistoryItem,
    AttendanceSubmitRequest,
    AttendanceSubmitResponse,
    SessionRosterResponse,
    StudentAttendanceSummaryResponse,
    StudentRosterItem,
    SubjectAttendanceItem,
    TimetableSlotInfo,
)
from app.services.audit_service import AuditService


class AttendanceService:
    @staticmethod
    async def get_session_roster(
        db: AsyncSession,
        timetable_entry_id: str,
        target_date: date,
        current_user: User,
    ) -> SessionRosterResponse:
        entry_uuid = uuid.UUID(timetable_entry_id)
        stmt = (
            select(TimetableEntry)
            .options(
                selectinload(TimetableEntry.course),
                selectinload(TimetableEntry.section),
                selectinload(TimetableEntry.period),
                selectinload(TimetableEntry.room),
                selectinload(TimetableEntry.staff),
            )
            .where(TimetableEntry.id == entry_uuid)
        )
        entry = (await db.execute(stmt)).scalar_one_or_none()
        if not entry:
            raise NotFoundException("Timetable entry not found")

        # Staff assignment authorization check
        if current_user.role == "STAFF":
            staff = (await db.execute(select(Staff).where(Staff.user_id == current_user.id))).scalar_one_or_none()
            if not staff or entry.staff_id != staff.id:
                raise ForbiddenException("You are not assigned to mark attendance for this class period.")

        # Check existing session
        session_check = (
            await db.execute(
                select(AttendanceSession).where(
                    AttendanceSession.timetable_entry_id == entry.id,
                    AttendanceSession.date == target_date,
                )
            )
        ).scalar_one_or_none()

        # Fetch students for this section
        students_stmt = (
            select(Student)
            .where(Student.section_id == entry.section_id, Student.is_active == True)
            .order_by(Student.roll_number)
        )
        students = (await db.execute(students_stmt)).scalars().all()

        roster_items = [
            StudentRosterItem(
                id=str(s.id),
                roll_number=s.roll_number,
                name=s.full_name,
                default_status="PRESENT",
            )
            for s in students
        ]

        info = TimetableSlotInfo(
            course_name=entry.course.name,
            course_code=entry.course.code,
            section_name=f"Sec {entry.section.name}",
            period=f"Period {entry.period.period_number} ({entry.period.name})",
            room=entry.room.room_number,
            date=target_date.strftime("%Y-%m-%d"),
        )

        return SessionRosterResponse(
            timetable_info=info,
            already_submitted=session_check is not None,
            students=roster_items,
        )

    @staticmethod
    async def submit_session_attendance(
        db: AsyncSession,
        request: AttendanceSubmitRequest,
        current_user: User,
        ip_address: Optional[str] = None,
    ) -> AttendanceSubmitResponse:
        entry_uuid = uuid.UUID(request.timetable_entry_id)
        stmt = (
            select(TimetableEntry)
            .options(selectinload(TimetableEntry.course), selectinload(TimetableEntry.section))
            .where(TimetableEntry.id == entry_uuid)
        )
        entry = (await db.execute(stmt)).scalar_one_or_none()
        if not entry:
            raise NotFoundException("Timetable entry not found")

        # Staff assignment check
        acting_staff_id = entry.staff_id
        if current_user.role == "STAFF":
            staff = (await db.execute(select(Staff).where(Staff.user_id == current_user.id))).scalar_one_or_none()
            if not staff or entry.staff_id != staff.id:
                raise ForbiddenException("You are not assigned to mark attendance for this lecture.")
            acting_staff_id = staff.id

        # Idempotency / Duplicate Check
        existing = (
            await db.execute(
                select(AttendanceSession).where(
                    AttendanceSession.timetable_entry_id == entry_uuid,
                    AttendanceSession.date == request.date,
                )
            )
        ).scalar_one_or_none()
        if existing:
            raise ConflictException(
                code="ATTENDANCE_ALREADY_SUBMITTED",
                message="Attendance has already been marked and finalized for this slot on this date.",
            )

        # Count statuses
        present_count = 0
        absent_count = 0
        od_count = 0

        for r in request.records:
            st = r.status.upper()
            if st in ["PRESENT", "P"]:
                present_count += 1
            elif st in ["ABSENT", "A"]:
                absent_count += 1
            elif st in ["ON_DUTY", "OD"]:
                od_count += 1

        total_marked = len(request.records)

        # Atomic Transaction
        session_record = AttendanceSession(
            timetable_entry_id=entry_uuid,
            staff_id=acting_staff_id,
            date=request.date,
            conducted_hours=1,
            topic_covered=request.topic_covered,
            present_count=present_count,
            absent_count=absent_count,
            od_count=od_count,
            total_marked=total_marked,
        )
        db.add(session_record)
        await db.flush()

        # Bulk insert attendance records
        records_to_add = [
            AttendanceRecord(
                attendance_session_id=session_record.id,
                student_id=uuid.UUID(r.student_id),
                status=r.status.upper() if r.status.upper() != "OD" else "ON_DUTY",
            )
            for r in request.records
        ]
        db.add_all(records_to_add)

        # Audit log
        await AuditService.log_action(
            db=db,
            action="ATTENDANCE_SUBMIT",
            entity_name="attendance_sessions",
            entity_id=str(session_record.id),
            user_id=current_user.id,
            details={
                "timetable_entry_id": request.timetable_entry_id,
                "date": request.date.isoformat(),
                "total_marked": total_marked,
                "present_count": present_count,
                "absent_count": absent_count,
                "od_count": od_count,
            },
            ip_address=ip_address,
        )

        await db.commit()
        await db.refresh(session_record)

        return AttendanceSubmitResponse(
            session_id=str(session_record.id),
            total_marked=total_marked,
            present_count=present_count,
            absent_count=absent_count,
            od_count=od_count,
            submitted_at=session_record.submitted_at,
        )

    @staticmethod
    async def get_student_summary(
        db: AsyncSession,
        current_user: User,
        target_student_id: Optional[str] = None,
    ) -> StudentAttendanceSummaryResponse:
        student_uuid = None
        if current_user.role == "STUDENT":
            s = (await db.execute(select(Student).where(Student.user_id == current_user.id))).scalar_one_or_none()
            if not s:
                raise NotFoundException("Student profile not found")
            student_uuid = s.id
        elif target_student_id:
            student_uuid = uuid.UUID(target_student_id)
        else:
            raise ForbiddenException("Target student ID must be provided")

        # Fetch all attendance records for this student with sessions and course info
        records_stmt = (
            select(AttendanceRecord)
            .options(
                selectinload(AttendanceRecord.session)
                .selectinload(AttendanceSession.timetable_entry)
                .selectinload(TimetableEntry.course),
                selectinload(AttendanceRecord.session)
                .selectinload(AttendanceSession.staff),
            )
            .where(AttendanceRecord.student_id == student_uuid)
        )
        records = (await db.execute(records_stmt)).scalars().all()

        total_conducted = len(records)
        total_attended = sum(1 for r in records if r.status in ["PRESENT", "ON_DUTY"])
        overall_pct = round((total_attended / total_conducted * 100), 1) if total_conducted > 0 else 100.0

        # Group by course
        courses_map = {}
        for r in records:
            course = r.session.timetable_entry.course
            staff = r.session.staff
            if course.id not in courses_map:
                courses_map[course.id] = {
                    "code": course.code,
                    "name": course.name,
                    "staff_name": staff.full_name if staff else "Faculty",
                    "attended": 0,
                    "total": 0,
                }
            courses_map[course.id]["total"] += 1
            if r.status in ["PRESENT", "ON_DUTY"]:
                courses_map[course.id]["attended"] += 1

        subject_items: List[SubjectAttendanceItem] = []
        for c in courses_map.values():
            pct = round((c["attended"] / c["total"] * 100), 1) if c["total"] > 0 else 100.0
            status_label = "EXCELLENT" if pct >= 90.0 else ("GOOD" if pct >= 75.0 else "CRITICAL")

            # Max absences allowed formula: floor( (attended - 0.75 * total) / 0.75 )
            excess = c["attended"] - 0.75 * c["total"]
            max_absences = max(0, math.floor(excess / 0.75)) if excess > 0 else 0

            subject_items.append(
                SubjectAttendanceItem(
                    course_code=c["code"],
                    course_name=c["name"],
                    staff_name=c["staff_name"],
                    attended_hours=c["attended"],
                    total_hours=c["total"],
                    percentage=pct,
                    status=status_label,
                    max_absences_allowed=max_absences,
                )
            )

        overall_status = "SAFE" if overall_pct >= 85.0 else ("WARNING" if overall_pct >= 75.0 else "CRITICAL")

        return StudentAttendanceSummaryResponse(
            overall_percentage=overall_pct,
            total_attended_hours=total_attended,
            total_conducted_hours=total_conducted,
            benchmark_percentage=75.0,
            status=overall_status,
            subjects=subject_items,
        )

    @staticmethod
    async def get_attendance_history(
        db: AsyncSession,
        date_filter: Optional[date] = None,
        limit: int = 50,
    ) -> List[AttendanceHistoryItem]:
        stmt = (
            select(AttendanceSession)
            .options(
                selectinload(AttendanceSession.timetable_entry).selectinload(TimetableEntry.course),
                selectinload(AttendanceSession.timetable_entry).selectinload(TimetableEntry.section),
                selectinload(AttendanceSession.timetable_entry).selectinload(TimetableEntry.period),
                selectinload(AttendanceSession.staff),
            )
            .order_by(AttendanceSession.date.desc(), AttendanceSession.submitted_at.desc())
            .limit(limit)
        )
        if date_filter:
            stmt = stmt.where(AttendanceSession.date == date_filter)

        sessions = (await db.execute(stmt)).scalars().all()
        history_items: List[AttendanceHistoryItem] = []
        for s in sessions:
            history_items.append(
                AttendanceHistoryItem(
                    id=str(s.id),
                    date=s.date.strftime("%Y-%m-%d"),
                    day=s.date.strftime("%A"),
                    course_name=s.timetable_entry.course.name,
                    course_code=s.timetable_entry.course.code,
                    period=f"Period {s.timetable_entry.period.period_number}",
                    present_count=s.present_count + s.od_count,
                    total_count=s.total_marked,
                    staff_name=s.staff.full_name,
                    section_name=f"Sec {s.timetable_entry.section.name}",
                )
            )
        return history_items
