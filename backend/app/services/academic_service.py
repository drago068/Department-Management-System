from typing import Any, Dict, List
import uuid
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.academics import Course, Period, Room
from app.models.organization import Batch, Department, Section
from app.models.profiles import Staff, Student


class AcademicService:
    @staticmethod
    async def get_departments(db: AsyncSession) -> List[Department]:
        stmt = select(Department).where(Department.is_active == True).order_by(Department.name)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_courses(db: AsyncSession, department_id: str = None) -> List[Course]:
        stmt = select(Course).where(Course.is_active == True)
        if department_id:
            dept_uuid = uuid.UUID(department_id) if isinstance(department_id, str) else department_id
            stmt = stmt.where(Course.department_id == dept_uuid)
        stmt = stmt.order_by(Course.code)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_rooms(db: AsyncSession) -> List[Room]:
        stmt = select(Room).where(Room.is_active == True).order_by(Room.building, Room.room_number)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_periods(db: AsyncSession) -> List[Period]:
        stmt = select(Period).order_by(Period.period_number)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_showcase(db: AsyncSession) -> Dict[str, Any]:
        # Count stats
        student_count = (await db.execute(select(func.count(Student.id)).where(Student.is_active == True))).scalar() or 0
        faculty_count = (await db.execute(select(func.count(Staff.id)).where(Staff.is_active == True))).scalar() or 0
        lab_count = (await db.execute(select(func.count(Room.id)).where(Room.room_type == "LAB", Room.is_active == True))).scalar() or 0
        course_count = (await db.execute(select(func.count(Course.id)).where(Course.is_active == True))).scalar() or 0

        # Faculty directory
        staff_stmt = select(Staff).where(Staff.is_active == True).order_by(Staff.full_name)
        staff_list = (await db.execute(staff_stmt)).scalars().all()
        faculty_dir = [
            {
                "id": str(s.id),
                "name": s.full_name,
                "role": f"{s.designation} • {s.cabin_number or 'Department Office'}",
                "email": s.email,
                "qualifications": s.qualifications,
                "experience": s.experience,
                "avatar_url": s.avatar_url,
            }
            for s in staff_list
        ]

        # Labs list
        labs_stmt = select(Room).where(Room.room_type == "LAB", Room.is_active == True).order_by(Room.room_number)
        labs = (await db.execute(labs_stmt)).scalars().all()
        laboratories = [
            {
                "id": str(lab.id),
                "name": lab.room_number,
                "building": lab.building,
                "capacity": lab.capacity,
            }
            for lab in labs
        ]

        return {
            "department": {
                "name": "Artificial Intelligence & Data Science",
                "code": "AI & DS",
                "college": "Suguna College of Engineering",
                "accreditation": "NBA & NAAC 'A+' Accredited • Autonomous",
                "vision": "To produce visionary AI engineers and data scientists equipped with rigorous analytical, algorithmic, and ethical problem-solving abilities.",
            },
            "stats": {
                "total_students": student_count,
                "faculty_members": faculty_count,
                "specialized_labs": lab_count,
                "accredited_courses": course_count,
            },
            "faculty": faculty_dir,
            "laboratories": laboratories,
        }
