import uuid
from typing import Any, Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.exceptions import NotFoundException
from app.models.profiles import AdminProfile, Staff, Student
from app.models.user import User
from app.schemas.profile import (
    AdminProfileData,
    AdminProfileUpdate,
    DepartmentMini,
    MentorMini,
    StaffProfileData,
    StaffProfileUpdate,
    StudentProfileData,
    StudentProfileUpdate,
)


class UserService:
    @staticmethod
    async def get_profile(db: AsyncSession, current_user: User) -> Union[StudentProfileData, StaffProfileData, AdminProfileData]:
        if current_user.role == "STUDENT":
            stmt = (
                select(Student)
                .options(
                    selectinload(Student.department),
                    selectinload(Student.batch),
                    selectinload(Student.section),
                    selectinload(Student.faculty_mentor),
                )
                .where(Student.user_id == current_user.id)
            )
            result = await db.execute(stmt)
            student = result.scalar_one_or_none()
            if not student:
                raise NotFoundException("Student profile not found")

            mentor = None
            if student.faculty_mentor:
                mentor = MentorMini(
                    id=str(student.faculty_mentor.id),
                    full_name=student.faculty_mentor.full_name,
                    designation=student.faculty_mentor.designation,
                    email=student.faculty_mentor.email,
                    cabin_number=student.faculty_mentor.cabin_number,
                )

            return StudentProfileData(
                role="STUDENT",
                id=str(student.id),
                roll_number=student.roll_number,
                register_number=student.register_number,
                full_name=student.full_name,
                department=DepartmentMini(
                    id=str(student.department.id),
                    code=student.department.code,
                    name=student.department.name,
                ),
                batch=student.batch.batch_name,
                section=student.section.name,
                semester=student.section.current_semester,
                cgpa=float(student.cgpa),
                phone=student.phone,
                email=student.email,
                parent_name=student.parent_name,
                parent_phone=student.parent_phone,
                date_of_birth=student.date_of_birth,
                blood_group=student.blood_group,
                address=student.address,
                avatar_url=student.avatar_url,
                faculty_mentor=mentor,
            )

        elif current_user.role == "STAFF":
            stmt = (
                select(Staff)
                .options(selectinload(Staff.department))
                .where(Staff.user_id == current_user.id)
            )
            result = await db.execute(stmt)
            staff = result.scalar_one_or_none()
            if not staff:
                raise NotFoundException("Staff profile not found")

            return StaffProfileData(
                role="STAFF",
                id=str(staff.id),
                faculty_id=staff.faculty_id,
                full_name=staff.full_name,
                designation=staff.designation,
                department=DepartmentMini(
                    id=str(staff.department.id),
                    code=staff.department.code,
                    name=staff.department.name,
                ),
                email=staff.email,
                phone=staff.phone,
                cabin_number=staff.cabin_number,
                qualifications=staff.qualifications,
                experience=staff.experience,
                avatar_url=staff.avatar_url,
            )

        elif current_user.role == "ADMIN":
            stmt = (
                select(AdminProfile)
                .options(selectinload(AdminProfile.department))
                .where(AdminProfile.user_id == current_user.id)
            )
            result = await db.execute(stmt)
            admin = result.scalar_one_or_none()
            if not admin:
                raise NotFoundException("Admin profile not found")

            dept = None
            if admin.department:
                dept = DepartmentMini(
                    id=str(admin.department.id),
                    code=admin.department.code,
                    name=admin.department.name,
                )

            return AdminProfileData(
                role="ADMIN",
                id=str(admin.id),
                full_name=admin.full_name,
                designation=admin.designation,
                email=admin.email,
                phone=admin.phone,
                office_location=admin.office_location,
                avatar_url=admin.avatar_url,
                department=dept,
            )

        raise NotFoundException("Role profile not found")

    @staticmethod
    async def update_profile(db: AsyncSession, current_user: User, payload: Union[StudentProfileUpdate, StaffProfileUpdate, AdminProfileUpdate]) -> Any:
        if current_user.role == "STUDENT":
            stmt = select(Student).where(Student.user_id == current_user.id)
            result = await db.execute(stmt)
            student = result.scalar_one_or_none()
            if not student:
                raise NotFoundException("Student profile not found")

            update_data = payload.model_dump(exclude_unset=True)
            for field, val in update_data.items():
                if hasattr(student, field) and field not in ["id", "user_id", "register_number", "roll_number", "cgpa", "department_id", "batch_id", "section_id"]:
                    setattr(student, field, val)

            await db.commit()
            return await UserService.get_profile(db, current_user)

        elif current_user.role == "STAFF":
            stmt = select(Staff).where(Staff.user_id == current_user.id)
            result = await db.execute(stmt)
            staff = result.scalar_one_or_none()
            if not staff:
                raise NotFoundException("Staff profile not found")

            update_data = payload.model_dump(exclude_unset=True)
            for field, val in update_data.items():
                if hasattr(staff, field) and field not in ["id", "user_id", "faculty_id", "department_id"]:
                    setattr(staff, field, val)

            await db.commit()
            return await UserService.get_profile(db, current_user)

        elif current_user.role == "ADMIN":
            stmt = select(AdminProfile).where(AdminProfile.user_id == current_user.id)
            result = await db.execute(stmt)
            admin = result.scalar_one_or_none()
            if not admin:
                raise NotFoundException("Admin profile not found")

            update_data = payload.model_dump(exclude_unset=True)
            for field, val in update_data.items():
                if hasattr(admin, field) and field not in ["id", "user_id"]:
                    setattr(admin, field, val)

            await db.commit()
            return await UserService.get_profile(db, current_user)
