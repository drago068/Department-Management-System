from datetime import date, datetime, time
from typing import List, Optional
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.exceptions import ConflictException, NotFoundException
from app.models.academics import Course, Period, Room
from app.models.attendance import AttendanceSession
from app.models.organization import Section
from app.models.profiles import Staff, Student
from app.models.timetable import TimetableEntry
from app.models.user import User
from app.schemas.timetable import (
    TimetableEntryCreate,
    TimetableEntryUpdate,
    TimetableScheduleResponse,
    TimetableSlotItem,
)
from app.services.audit_service import AuditService

WEEKDAYS = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}


class TimetableService:
    @staticmethod
    def compute_slot_status(slot_start: time, slot_end: time, is_today: bool) -> str:
        if not is_today:
            return "UPCOMING"

        now = datetime.now()
        current_time = now.time()

        if current_time > slot_end:
            return "COMPLETED"
        elif slot_start <= current_time <= slot_end:
            return "IN_PROGRESS"
        else:
            return "UPCOMING"

    @staticmethod
    async def get_student_schedule(db: AsyncSession, current_user: User, day_of_week: Optional[int] = None) -> TimetableScheduleResponse:
        stmt_student = select(Student).where(Student.user_id == current_user.id)
        student = (await db.execute(stmt_student)).scalar_one_or_none()
        if not student:
            raise NotFoundException("Student profile not found")

        today = date.today()
        # Python weekday: Monday is 0, so +1 = 1..7. If Sunday (7), default to Monday (1)
        today_weekday = today.weekday() + 1
        if today_weekday > 6:
            today_weekday = 1

        selected_day = day_of_week if day_of_week else today_weekday
        is_today = selected_day == (today.weekday() + 1)

        # Fetch all periods to order schedule properly including breaks
        periods = (await db.execute(select(Period).order_by(Period.period_number))).scalars().all()

        # Fetch timetable entries for this section and day
        entries_stmt = (
            select(TimetableEntry)
            .options(
                selectinload(TimetableEntry.course),
                selectinload(TimetableEntry.staff),
                selectinload(TimetableEntry.room),
                selectinload(TimetableEntry.period),
            )
            .where(
                TimetableEntry.section_id == student.section_id,
                TimetableEntry.day_of_week == selected_day,
                TimetableEntry.is_active == True,
            )
        )
        entries = (await db.execute(entries_stmt)).scalars().all()
        entry_by_period = {e.period_id: e for e in entries}

        slots: List[TimetableSlotItem] = []
        for period in periods:
            start_str = period.start_time.strftime("%H:%M")
            end_str = period.end_time.strftime("%H:%M")
            status = TimetableService.compute_slot_status(period.start_time, period.end_time, is_today)

            if period.is_break:
                slots.append(
                    TimetableSlotItem(
                        id=f"break-{period.id}",
                        period_number=period.period_number,
                        period_name=period.name,
                        start_time=start_str,
                        end_time=end_str,
                        is_break=True,
                        title=period.name,
                        status=status,
                    )
                )
            else:
                entry = entry_by_period.get(period.id)
                if entry:
                    slots.append(
                        TimetableSlotItem(
                            id=str(entry.id),
                            period_number=period.period_number,
                            period_name=period.name,
                            start_time=start_str,
                            end_time=end_str,
                            is_break=False,
                            course_code=entry.course.code,
                            course_name=entry.course.name,
                            short_name=entry.course.short_name,
                            lecture_type=entry.lecture_type,
                            room=entry.room.room_number,
                            faculty_name=entry.staff.full_name,
                            status=status,
                            batch_split=entry.batch_split,
                        )
                    )
                else:
                    slots.append(
                        TimetableSlotItem(
                            id=f"empty-{period.id}",
                            period_number=period.period_number,
                            period_name=period.name,
                            start_time=start_str,
                            end_time=end_str,
                            is_break=False,
                            title="Free Period / Library",
                            status=status,
                        )
                    )

        return TimetableScheduleResponse(
            day_of_week=selected_day,
            day_name=WEEKDAYS.get(selected_day, "Monday"),
            schedule=slots,
        )

    @staticmethod
    async def get_staff_schedule(db: AsyncSession, current_user: User, day_of_week: Optional[int] = None) -> TimetableScheduleResponse:
        stmt_staff = select(Staff).where(Staff.user_id == current_user.id)
        staff = (await db.execute(stmt_staff)).scalar_one_or_none()
        if not staff:
            raise NotFoundException("Staff profile not found")

        today = date.today()
        today_weekday = today.weekday() + 1
        if today_weekday > 6:
            today_weekday = 1

        selected_day = day_of_week if day_of_week else today_weekday
        is_today = selected_day == (today.weekday() + 1)

        periods = (await db.execute(select(Period).order_by(Period.period_number))).scalars().all()

        entries_stmt = (
            select(TimetableEntry)
            .options(
                selectinload(TimetableEntry.course),
                selectinload(TimetableEntry.section).selectinload(Section.batch),
                selectinload(TimetableEntry.room),
                selectinload(TimetableEntry.period),
            )
            .where(
                TimetableEntry.staff_id == staff.id,
                TimetableEntry.day_of_week == selected_day,
                TimetableEntry.is_active == True,
            )
        )
        entries = (await db.execute(entries_stmt)).scalars().all()
        entry_by_period = {e.period_id: e for e in entries}

        # Check attendance sessions marked today for these entries
        entry_ids = [e.id for e in entries]
        sessions_stmt = select(AttendanceSession.timetable_entry_id).where(
            AttendanceSession.timetable_entry_id.in_(entry_ids),
            AttendanceSession.date == today,
        )
        marked_entry_ids = set((await db.execute(sessions_stmt)).scalars().all())

        slots: List[TimetableSlotItem] = []
        for period in periods:
            start_str = period.start_time.strftime("%H:%M")
            end_str = period.end_time.strftime("%H:%M")
            status = TimetableService.compute_slot_status(period.start_time, period.end_time, is_today)

            if period.is_break:
                slots.append(
                    TimetableSlotItem(
                        id=f"break-{period.id}",
                        period_number=period.period_number,
                        period_name=period.name,
                        start_time=start_str,
                        end_time=end_str,
                        is_break=True,
                        title=period.name,
                        status=status,
                    )
                )
            else:
                entry = entry_by_period.get(period.id)
                if entry:
                    att_status = "MARKED" if entry.id in marked_entry_ids else "PENDING"
                    sec_name = f"Year {entry.section.current_semester // 2 + 1} • Sec {entry.section.name}"
                    slots.append(
                        TimetableSlotItem(
                            id=str(entry.id),
                            period_number=period.period_number,
                            period_name=period.name,
                            start_time=start_str,
                            end_time=end_str,
                            is_break=False,
                            course_code=entry.course.code,
                            course_name=entry.course.name,
                            short_name=entry.course.short_name,
                            lecture_type=entry.lecture_type,
                            room=entry.room.room_number,
                            section_name=sec_name,
                            status=status,
                            attendance_status=att_status,
                            batch_split=entry.batch_split,
                        )
                    )
                else:
                    slots.append(
                        TimetableSlotItem(
                            id=f"empty-{period.id}",
                            period_number=period.period_number,
                            period_name=period.name,
                            start_time=start_str,
                            end_time=end_str,
                            is_break=False,
                            title="Preparation / Research Hour",
                            status=status,
                        )
                    )

        return TimetableScheduleResponse(
            day_of_week=selected_day,
            day_name=WEEKDAYS.get(selected_day, "Monday"),
            schedule=slots,
        )

    @staticmethod
    async def create_entry_with_conflict_check(db: AsyncSession, entry_data: TimetableEntryCreate, acting_user_id: uuid.UUID) -> TimetableEntry:
        # Convert IDs to UUIDs
        sec_uuid = uuid.UUID(entry_data.section_id)
        crs_uuid = uuid.UUID(entry_data.course_id)
        stf_uuid = uuid.UUID(entry_data.staff_id)
        rm_uuid = uuid.UUID(entry_data.room_id)
        per_uuid = uuid.UUID(entry_data.period_id)

        # 1. Room conflict check
        room_check = (
            await db.execute(
                select(TimetableEntry)
                .options(selectinload(TimetableEntry.room), selectinload(TimetableEntry.course))
                .where(
                    TimetableEntry.room_id == rm_uuid,
                    TimetableEntry.day_of_week == entry_data.day_of_week,
                    TimetableEntry.period_id == per_uuid,
                    TimetableEntry.is_active == True,
                )
            )
        ).scalar_one_or_none()
        if room_check:
            raise ConflictException(
                code="ROOM_OCCUPIED",
                message=f"Room {room_check.room.room_number} is already occupied by {room_check.course.code} during this period.",
            )

        # 2. Staff conflict check
        staff_check = (
            await db.execute(
                select(TimetableEntry)
                .options(selectinload(TimetableEntry.staff), selectinload(TimetableEntry.course))
                .where(
                    TimetableEntry.staff_id == stf_uuid,
                    TimetableEntry.day_of_week == entry_data.day_of_week,
                    TimetableEntry.period_id == per_uuid,
                    TimetableEntry.is_active == True,
                )
            )
        ).scalar_one_or_none()
        if staff_check:
            raise ConflictException(
                code="STAFF_DOUBLE_BOOKED",
                message=f"Faculty {staff_check.staff.full_name} is already teaching {staff_check.course.code} in another section during this period.",
            )

        # 3. Section conflict check
        section_check = (
            await db.execute(
                select(TimetableEntry)
                .options(selectinload(TimetableEntry.course))
                .where(
                    TimetableEntry.section_id == sec_uuid,
                    TimetableEntry.day_of_week == entry_data.day_of_week,
                    TimetableEntry.period_id == per_uuid,
                    TimetableEntry.is_active == True,
                )
            )
        ).scalar_one_or_none()
        if section_check:
            raise ConflictException(
                code="SECTION_CONFLICT",
                message=f"This section already has a lecture scheduled ({section_check.course.code}) during this period.",
            )

        new_entry = TimetableEntry(
            section_id=sec_uuid,
            course_id=crs_uuid,
            staff_id=stf_uuid,
            room_id=rm_uuid,
            period_id=per_uuid,
            day_of_week=entry_data.day_of_week,
            lecture_type=entry_data.lecture_type,
            batch_split=entry_data.batch_split,
            is_active=True,
        )
        db.add(new_entry)
        await db.flush()

        await AuditService.log_action(
            db=db,
            action="TIMETABLE_CREATE",
            entity_name="timetable_entries",
            entity_id=str(new_entry.id),
            user_id=acting_user_id,
            details=entry_data.model_dump(),
        )
        await db.commit()
        await db.refresh(new_entry)
        return new_entry
