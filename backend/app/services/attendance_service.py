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
            .order_by(Student.register_number)
        )
        students = (await db.execute(students_stmt)).scalars().all()

        roster_items = [
            StudentRosterItem(
                id=str(s.id),
                register_number=s.register_number,
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
        student_obj = None
        if current_user.role == "STUDENT":
            s = (await db.execute(select(Student).where(Student.user_id == current_user.id))).scalar_one_or_none()
            if not s:
                raise NotFoundException("Student profile not found")
            student_uuid = s.id
            student_obj = s
        elif target_student_id:
            student_uuid = uuid.UUID(target_student_id)
            student_obj = (await db.execute(select(Student).where(Student.id == student_uuid))).scalar_one_or_none()
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
        od_hours = sum(1 for r in records if r.status == "ON_DUTY")
        absent_hours = sum(1 for r in records if r.status == "ABSENT")
        overall_pct = round((total_attended / total_conducted * 100), 1) if total_conducted > 0 else 100.0

        # Group by course
        courses_map = {}

        # Pre-populate all courses scheduled for the student's section from timetable
        if student_obj and student_obj.section_id:
            tt_stmt = (
                select(TimetableEntry)
                .options(
                    selectinload(TimetableEntry.course),
                    selectinload(TimetableEntry.staff),
                )
                .where(TimetableEntry.section_id == student_obj.section_id)
            )
            tt_entries = (await db.execute(tt_stmt)).scalars().all()
            for entry in tt_entries:
                c = entry.course
                if c and c.id not in courses_map:
                    courses_map[c.id] = {
                        "code": c.code,
                        "name": c.name,
                        "staff_name": entry.staff.full_name if entry.staff else "Faculty",
                        "attended": 0,
                        "total": 0,
                        "absent": 0,
                        "od": 0,
                        "credits": f"{c.credits} Credits" if hasattr(c, "credits") else "3 Credits",
                    }

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
                    "absent": 0,
                    "od": 0,
                    "credits": f"{course.credits} Credits" if hasattr(course, "credits") else "3 Credits",
                }
            courses_map[course.id]["total"] += 1
            if r.status in ["PRESENT", "ON_DUTY"]:
                courses_map[course.id]["attended"] += 1
            if r.status == "ABSENT":
                courses_map[course.id]["absent"] += 1
            elif r.status == "ON_DUTY":
                courses_map[course.id]["od"] += 1

        subject_items: List[SubjectAttendanceItem] = []
        for c in courses_map.values():
            if c["total"] > 0:
                pct = round((c["attended"] / c["total"] * 100), 1)
                status_label = "EXCELLENT" if pct >= 90.0 else ("GOOD" if pct >= 75.0 else "CRITICAL")
                excess = c["attended"] - 0.75 * c["total"]
                max_absences = max(0, math.floor(excess / 0.75)) if excess > 0 else 0
            else:
                pct = 100.0
                status_label = "SAFE"
                max_absences = 0

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
                    credits=c.get("credits", "3 Credits"),
                    absent_hours=c.get("absent", 0),
                    od_hours=c.get("od", 0),
                )
            )

        overall_status = "SAFE" if overall_pct >= 85.0 else ("WARNING" if overall_pct >= 75.0 else "CRITICAL")

        return StudentAttendanceSummaryResponse(
            overall_percentage=overall_pct,
            total_attended_hours=total_attended,
            total_conducted_hours=total_conducted,
            benchmark_percentage=75.0,
            status=overall_status,
            od_hours=od_hours,
            absent_hours=absent_hours,
            subjects=subject_items,
        )

    @staticmethod
    async def get_attendance_history(
        db: AsyncSession,
        date_filter: Optional[date] = None,
        limit: int = 50,
        current_user: Optional[User] = None,
    ) -> List[AttendanceHistoryItem]:
        stmt = (
            select(AttendanceSession)
            .options(
                selectinload(AttendanceSession.timetable_entry).selectinload(TimetableEntry.course),
                selectinload(AttendanceSession.timetable_entry).selectinload(TimetableEntry.section),
                selectinload(AttendanceSession.timetable_entry).selectinload(TimetableEntry.period),
                selectinload(AttendanceSession.staff),
            )
        )

        stud_obj = None
        if current_user and current_user.role == "STAFF":
            staff_res = await db.execute(select(Staff).where(Staff.user_id == current_user.id))
            staff_obj = staff_res.scalar_one_or_none()
            if staff_obj:
                stmt = stmt.where(AttendanceSession.staff_id == staff_obj.id)
        elif current_user and current_user.role == "STUDENT":
            stud_res = await db.execute(select(Student).where(Student.user_id == current_user.id))
            stud_obj = stud_res.scalar_one_or_none()
            if stud_obj and stud_obj.section_id:
                stmt = stmt.join(AttendanceSession.timetable_entry).where(TimetableEntry.section_id == stud_obj.section_id)

        if date_filter:
            stmt = stmt.where(AttendanceSession.date == date_filter)

        stmt = stmt.order_by(AttendanceSession.date.desc(), AttendanceSession.submitted_at.desc()).limit(limit)
        sessions = (await db.execute(stmt)).scalars().all()

        # Map student's individual attendance status for each session
        student_records_map = {}
        if current_user and current_user.role == "STUDENT" and stud_obj:
            session_ids = [s.id for s in sessions]
            if session_ids:
                rec_stmt = select(AttendanceRecord).where(
                    AttendanceRecord.student_id == stud_obj.id,
                    AttendanceRecord.attendance_session_id.in_(session_ids),
                )
                recs = (await db.execute(rec_stmt)).scalars().all()
                for r in recs:
                    student_records_map[r.attendance_session_id] = r.status

        history_items: List[AttendanceHistoryItem] = []
        for s in sessions:
            student_status = student_records_map.get(s.id)
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
                    status=student_status,
                    topic_covered=s.topic_covered,
                )
            )
        return history_items
