import uuid
from typing import Any, Dict, List, Optional, Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.exceptions import ConflictException, NotFoundException
from app.core.security import get_password_hash
from app.models.organization import Batch, Department, Section
from app.models.profiles import AdminProfile, Staff, Student
from app.models.user import User
from app.schemas.profile import (
    AdminProfileData,
    AdminProfileUpdate,
    BulkStudentEnrollRequest,
    BulkStudentEnrollResponse,
    DepartmentMini,
    MentorMini,
    StaffProfileData,
    StaffProfileUpdate,
    StudentEnrollRequest,
    StudentEnrollResponse,
    StudentProfileData,
    StudentProfileUpdate,
)


def generate_predefined_password(full_name: str, register_number: str) -> str:
    """Predefined password rule:

    First 3 chars of name in lowercase + last 3 digits/numbers of register
    number.
    """
    alpha_chars = [c for c in full_name if c.isalpha()]
    if len(alpha_chars) >= 3:
        name_part = "".join(alpha_chars[:3]).lower()
    else:
        name_part = full_name.replace(" ", "")[:3].lower()

    digits = [c for c in register_number if c.isdigit()]
    if len(digits) >= 3:
        reg_part = "".join(digits[-3:])
    else:
        reg_part = register_number.strip()[-3:]

    return f"{name_part}{reg_part}"


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
                if hasattr(student, field) and field not in ["id", "user_id", "register_number", "cgpa", "department_id", "batch_id", "section_id"]:
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

    @staticmethod
    async def get_cohort_options(db: AsyncSession) -> Dict[str, Any]:
        """Fetch all departments, batches, sections, and staff mentors."""
        depts = (await db.execute(select(Department).where(Department.is_active == True).order_by(Department.name))).scalars().all()
        batches = (await db.execute(select(Batch).where(Batch.is_active == True).order_by(Batch.batch_name.desc()))).scalars().all()
        sections = (await db.execute(select(Section).where(Section.is_active == True).order_by(Section.name))).scalars().all()
        mentors = (await db.execute(select(Staff).where(Staff.is_active == True).order_by(Staff.full_name))).scalars().all()

        return {
            "departments": [{"id": str(d.id), "code": d.code, "name": d.name} for d in depts],
            "batches": [{"id": str(b.id), "batch_name": b.batch_name, "department_id": str(b.department_id)} for b in batches],
            "sections": [{"id": str(s.id), "name": s.name, "batch_id": str(s.batch_id), "semester": s.current_semester} for s in sections],
            "mentors": [{"id": str(m.id), "full_name": m.full_name, "designation": m.designation, "email": m.email} for m in mentors],
        }

    @staticmethod
    async def enroll_student(db: AsyncSession, payload: StudentEnrollRequest) -> StudentEnrollResponse:
        """Enroll single student with predefined password rule."""
        reg = payload.register_number.strip().upper()

        # Check existing register number
        existing_student = (await db.execute(select(Student).where(Student.register_number == reg))).scalar_one_or_none()
        if existing_student:
            raise ConflictException(f"A student with Registration Number '{reg}' already exists.")

        existing_user = (await db.execute(select(User).where(User.identifier == reg))).scalar_one_or_none()
        if existing_user:
            raise ConflictException(f"User account with identifier '{reg}' already exists.")

        # Resolve Department
        dept = None
        if payload.department_id:
            try:
                dept_uuid = uuid.UUID(payload.department_id)
                dept = (await db.execute(select(Department).where(Department.id == dept_uuid))).scalar_one_or_none()
            except Exception:
                pass
        if not dept and payload.department_code:
            dept = (await db.execute(select(Department).where(Department.code == payload.department_code.strip()))).scalar_one_or_none()
        if not dept:
            dept = (await db.execute(select(Department).where(Department.is_active == True))).scalars().first()
        if not dept:
            raise NotFoundException("No active department found in the system.")

        # Resolve Batch
        batch = None
        if payload.batch_id:
            try:
                b_uuid = uuid.UUID(payload.batch_id)
                batch = (await db.execute(select(Batch).where(Batch.id == b_uuid))).scalar_one_or_none()
            except Exception:
                pass
        if not batch and payload.batch_name:
            batch = (await db.execute(select(Batch).where(Batch.batch_name == payload.batch_name.strip()))).scalar_one_or_none()
        if not batch:
            batch = (await db.execute(select(Batch).where(Batch.department_id == dept.id, Batch.is_active == True))).scalars().first()
        if not batch:
            batch = (await db.execute(select(Batch).where(Batch.is_active == True))).scalars().first()
        if not batch:
            raise NotFoundException("No active academic batch found.")

        # Resolve Section
        section = None
        if payload.section_id:
            try:
                s_uuid = uuid.UUID(payload.section_id)
                section = (await db.execute(select(Section).where(Section.id == s_uuid))).scalar_one_or_none()
            except Exception:
                pass
        if not section and payload.section_name:
            s_name = payload.section_name.strip().upper()
            if s_name.startswith("SECTION "):
                s_name = s_name.replace("SECTION ", "").strip()
            section = (await db.execute(select(Section).where(Section.batch_id == batch.id, Section.name == s_name))).scalar_one_or_none()
        if not section:
            section = (await db.execute(select(Section).where(Section.batch_id == batch.id))).scalars().first()
        if not section:
            section = (await db.execute(select(Section).where(Section.is_active == True))).scalars().first()
        if not section:
            raise NotFoundException("No active section found.")

        # Resolve Mentor
        mentor = None
        if payload.faculty_mentor_id:
            try:
                m_uuid = uuid.UUID(payload.faculty_mentor_id)
                mentor = (await db.execute(select(Staff).where(Staff.id == m_uuid))).scalar_one_or_none()
            except Exception:
                pass

        # Generate Predefined Password
        generated_pwd = generate_predefined_password(payload.full_name, reg)

        # Generate Email if not supplied
        first_token = payload.full_name.split()[0].lower() if payload.full_name.split() else "student"
        email = payload.email or f"{first_token}.{reg.lower()}@suguna.edu.in"

        # Create User account
        new_user = User(
            id=uuid.uuid4(),
            identifier=reg,
            password_hash=get_password_hash(generated_pwd),
            role="STUDENT",
            is_active=True,
        )
        db.add(new_user)
        await db.flush()

        # Create Student profile
        new_student = Student(
            id=uuid.uuid4(),
            user_id=new_user.id,
            department_id=dept.id,
            batch_id=batch.id,
            section_id=section.id,
            faculty_mentor_id=mentor.id if mentor else None,
            register_number=reg,
            full_name=payload.full_name.strip(),
            email=email,
            phone=payload.phone,
            parent_name=payload.parent_name,
            parent_phone=payload.parent_phone,
            date_of_birth=payload.date_of_birth,
            blood_group=payload.blood_group,
            address=payload.address,
            avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed={reg}",
            cgpa=0.0,
            is_active=True,
        )
        db.add(new_student)
        await db.commit()

        return StudentEnrollResponse(
            id=str(new_student.id),
            user_id=str(new_user.id),
            register_number=reg,
            full_name=new_student.full_name,
            email=new_student.email,
            generated_password=generated_pwd,
            department_name=dept.name,
            batch_name=batch.batch_name,
            section_name=section.name,
            message="Student enrolled successfully with predefined credentials.",
        )

    @staticmethod
    async def bulk_enroll_students(db: AsyncSession, payload: BulkStudentEnrollRequest) -> BulkStudentEnrollResponse:
        """Bulk enroll multiple students with predefined passwords."""
        results = []
        enrolled_count = 0
        skipped_count = 0

        # Resolve defaults
        default_dept = None
        if payload.default_department_id:
            try:
                default_dept = (await db.execute(select(Department).where(Department.id == uuid.UUID(payload.default_department_id)))).scalar_one_or_none()
            except Exception:
                pass
        if not default_dept:
            default_dept = (await db.execute(select(Department).where(Department.is_active == True))).scalars().first()

        default_batch = None
        if payload.default_batch_id:
            try:
                default_batch = (await db.execute(select(Batch).where(Batch.id == uuid.UUID(payload.default_batch_id)))).scalar_one_or_none()
            except Exception:
                pass
        if not default_batch and default_dept:
            default_batch = (await db.execute(select(Batch).where(Batch.department_id == default_dept.id, Batch.is_active == True))).scalars().first()
        if not default_batch:
            default_batch = (await db.execute(select(Batch).where(Batch.is_active == True))).scalars().first()

        default_sec = None
        if payload.default_section_id:
            try:
                default_sec = (await db.execute(select(Section).where(Section.id == uuid.UUID(payload.default_section_id)))).scalar_one_or_none()
            except Exception:
                pass
        if not default_sec and default_batch:
            default_sec = (await db.execute(select(Section).where(Section.batch_id == default_batch.id))).scalars().first()
        if not default_sec:
            default_sec = (await db.execute(select(Section).where(Section.is_active == True))).scalars().first()

        for item in payload.students:
            reg = item.register_number.strip().upper()
            if not reg or not item.full_name:
                skipped_count += 1
                results.append({"register_number": reg, "status": "SKIPPED", "reason": "Missing required fields"})
                continue

            # Check if exists
            exists = (await db.execute(select(Student.id).where(Student.register_number == reg))).scalar_one_or_none()
            if exists:
                skipped_count += 1
                results.append({"register_number": reg, "name": item.full_name, "status": "SKIPPED", "reason": "Already exists"})
                continue

            # Generate predefined password
            pwd = generate_predefined_password(item.full_name, reg)

            # Resolve email
            first_token = item.full_name.split()[0].lower() if item.full_name.split() else "student"
            email = item.email or f"{first_token}.{reg.lower()}@suguna.edu.in"

            user = User(
                id=uuid.uuid4(),
                identifier=reg,
                password_hash=get_password_hash(pwd),
                role="STUDENT",
                is_active=True,
            )
            db.add(user)
            await db.flush()

            st = Student(
                id=uuid.uuid4(),
                user_id=user.id,
                department_id=default_dept.id if default_dept else None,
                batch_id=default_batch.id if default_batch else None,
                section_id=default_sec.id if default_sec else None,
                register_number=reg,
                full_name=item.full_name.strip(),
                email=email,
                phone=item.phone,
                parent_name=item.parent_name,
                parent_phone=item.parent_phone,
                avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed={reg}",
                cgpa=0.0,
                is_active=True,
            )
            db.add(st)
            enrolled_count += 1
            results.append({
                "register_number": reg,
                "name": item.full_name,
                "status": "ENROLLED",
                "generated_password": pwd,
                "email": email,
            })

        await db.commit()
        return BulkStudentEnrollResponse(
            total_processed=len(payload.students),
            enrolled_count=enrolled_count,
            skipped_count=skipped_count,
            results=results,
        )
