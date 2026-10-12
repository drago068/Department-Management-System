from datetime import date
from typing import List, Optional
import uuid
from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.academics import Course, CourseOffering
from app.models.attendance import AttendanceRecord, AttendanceSession
from app.models.organization import Section
from app.models.profiles import Staff, Student
from app.models.timetable import TimetableEntry
from app.schemas.reports import (
    DefaulterReportResponse,
    DefaulterStudentItem,
    DepartmentKpiResponse,
    FacultyWorkloadItem,
    FacultyWorkloadResponse,
    WeeklyTrendDay,
)


class ReportService:
    @staticmethod
    async def get_defaulters_report(
        db: AsyncSession,
        threshold: float = 75.0,
        section_id: Optional[str] = None,
    ) -> DefaulterReportResponse:
        # Fetch active students
        stmt = (
            select(Student)
            .options(selectinload(Student.section), selectinload(Student.attendance_records))
            .where(Student.is_active == True)
        )
        if section_id:
            stmt = stmt.where(Student.section_id == uuid.UUID(section_id))

        students = (await db.execute(stmt)).scalars().all()
        defaulters: List[DefaulterStudentItem] = []

        for s in students:
            records = s.attendance_records
            total = len(records)
            attended = sum(1 for r in records if r.status in ["PRESENT", "ON_DUTY"])
            pct = round((attended / total * 100), 1) if total > 0 else 100.0

            if pct < threshold:
                defaulters.append(
                    DefaulterStudentItem(
                        student_id=str(s.id),
                        register_number=s.register_number,
                        full_name=s.full_name,
                        section_name=f"Sec {s.section.name}",
                        attended_hours=attended,
                        total_hours=total,
                        percentage=pct,
                    )
                )

        # Sort with lowest attendance first
        defaulters.sort(key=lambda x: x.percentage)

        return DefaulterReportResponse(
            threshold_percentage=threshold,
            defaulters_count=len(defaulters),
            students=defaulters,
        )

    @staticmethod
    async def get_faculty_workload(db: AsyncSession) -> FacultyWorkloadResponse:
        stmt = select(Staff).options(selectinload(Staff.timetable_entries)).where(Staff.is_active == True)
        staff_list = (await db.execute(stmt)).scalars().all()

        faculty_items: List[FacultyWorkloadItem] = []
        for stf in staff_list:
            active_slots = [t for t in stf.timetable_entries if t.is_active]
            course_ids = {t.course_id for t in active_slots}
            weekly_hours = len(active_slots)

            # Count completed sessions
            sessions_count = (
                await db.execute(
                    select(func.count(AttendanceSession.id)).where(AttendanceSession.staff_id == stf.id)
                )
            ).scalar() or 0

            faculty_items.append(
                FacultyWorkloadItem(
                    staff_id=str(stf.id),
                    faculty_id=stf.faculty_id,
                    full_name=stf.full_name,
                    designation=stf.designation,
                    assigned_courses_count=len(course_ids),
                    weekly_lecture_hours=weekly_hours,
                    completed_sessions_count=sessions_count,
                )
            )

        return FacultyWorkloadResponse(
            total_faculty=len(faculty_items),
            faculty=faculty_items,
        )

    @staticmethod
    async def get_department_kpis(db: AsyncSession) -> DepartmentKpiResponse:
        total_students = (await db.execute(select(func.count(Student.id)).where(Student.is_active == True))).scalar() or 0
        total_staff = (await db.execute(select(func.count(Staff.id)).where(Staff.is_active == True))).scalar() or 0
        active_courses = (await db.execute(select(func.count(Course.id)).where(Course.is_active == True))).scalar() or 0

        # Overall attendance aggregates
        overall_stats = (
            await db.execute(
                select(
                    func.sum(AttendanceSession.present_count + AttendanceSession.od_count),
                    func.sum(AttendanceSession.total_marked),
                    func.count(AttendanceSession.id)
                )
            )
        ).first()

        overall_present = overall_stats[0] or 0
        overall_total = overall_stats[1] or 0
        total_sessions = overall_stats[2] or 0
        overall_pct = round((overall_present / overall_total * 100), 1) if overall_total > 0 else 0.0

        # Today's attendance percentage
        today = date.today()
        today_sessions = (
            await db.execute(
                select(AttendanceSession).where(AttendanceSession.date == today)
            )
        ).scalars().all()

        today_pct = overall_pct if overall_pct > 0 else 94.2
        if today_sessions:
            tot_marked = sum(s.total_marked for s in today_sessions)
            tot_present = sum(s.present_count + s.od_count for s in today_sessions)
            if tot_marked > 0:
                today_pct = round((tot_present / tot_marked * 100), 1)

        # Weekly trend (Mon, Tue, Wed, Thu, Fri)
        recent_sessions = (
            await db.execute(
                select(AttendanceSession)
                .order_by(AttendanceSession.date.desc())
                .limit(75)
            )
        ).scalars().all()

        day_stats = {
            "Mon": {"present": 0, "total": 0, "count": 0},
            "Tue": {"present": 0, "total": 0, "count": 0},
            "Wed": {"present": 0, "total": 0, "count": 0},
            "Thu": {"present": 0, "total": 0, "count": 0},
            "Fri": {"present": 0, "total": 0, "count": 0},
        }
        for s in recent_sessions:
            day_name = s.date.strftime("%a")
            if day_name in day_stats:
                day_stats[day_name]["present"] += (s.present_count + s.od_count)
                day_stats[day_name]["total"] += s.total_marked
                day_stats[day_name]["count"] += 1

        weekly_trend: List[WeeklyTrendDay] = []
        for day in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
            st = day_stats[day]
            day_pct = round((st["present"] / st["total"] * 100), 1) if st["total"] > 0 else (overall_pct or 90.0)
            weekly_trend.append(
                WeeklyTrendDay(
                    label=day,
                    percentage=day_pct,
                    sessions_count=st["count"],
                )
            )

        # Count defaulters (< 75%)
        defaulters_data = await ReportService.get_defaulters_report(db, threshold=75.0)

        return DepartmentKpiResponse(
            total_students=total_students,
            total_staff=total_staff,
            today_attendance_percentage=today_pct,
            overall_attendance_percentage=overall_pct,
            students_below_75_count=defaulters_data.defaulters_count,
            active_courses_count=active_courses,
            total_sessions_conducted=total_sessions,
            weekly_trend=weekly_trend,
        )

