import uuid
from datetime import date
from typing import Any, Dict, List, Optional, Union
from sqlalchemy import func, select
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
    AssignMentorRequest,
    AutoDistributeMentorsRequest,
    BulkStaffEnrollRequest,
    BulkStaffEnrollResponse,
    BulkStaffItem,
    BulkStudentEnrollRequest,
    BulkStudentEnrollResponse,
    DepartmentMini,
    FacultyMentorItem,
    MentorMini,
    StaffEnrollRequest,
    StaffEnrollResponse,
    StaffProfileData,
    StaffProfileUpdate,
    StudentAllocationItem,
    StudentAllocationResponse,
    StudentEnrollRequest,
    StudentEnrollResponse,
    StudentProfileData,
    StudentProfileUpdate,
    UnassignMentorRequest,
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
                if field == "date_of_birth" and isinstance(val, str):
                    try:
                        val = date.fromisoformat(val.strip()) if val.strip() else None
                    except ValueError:
                        continue
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
        conflict_strategy = (payload.conflict_strategy or "skip").strip().lower()

        # 1. Resolve default Department
        default_dept = None
        if payload.default_department_id:
            try:
                default_dept = (await db.execute(select(Department).where(Department.id == uuid.UUID(payload.default_department_id)))).scalar_one_or_none()
            except Exception:
                pass
        if not default_dept and payload.default_department_code:
            code_clean = payload.default_department_code.strip().upper()
            default_dept = (await db.execute(select(Department).where(func.upper(Department.code) == code_clean))).scalar_one_or_none()
            if not default_dept:
                default_dept = (await db.execute(select(Department).where(Department.name.ilike(f"%{payload.default_department_code.strip()}%")))).scalars().first()
        if not default_dept:
            default_dept = (await db.execute(select(Department).where(Department.is_active == True))).scalars().first()
        if not default_dept:
            default_dept = Department(id=uuid.uuid4(), name="Artificial Intelligence & Data Science", code="AIDS", is_active=True)
            db.add(default_dept)
            await db.flush()

        # 2. Resolve default Batch
        default_batch = None
        if payload.default_batch_id:
            try:
                default_batch = (await db.execute(select(Batch).where(Batch.id == uuid.UUID(payload.default_batch_id)))).scalar_one_or_none()
            except Exception:
                pass
        if not default_batch and payload.default_batch_name:
            clean_batch = payload.default_batch_name.replace("–", "-").strip()
            batch_q = select(Batch).where(func.replace(Batch.batch_name, "–", "-").ilike(f"%{clean_batch}%"))
            if default_dept:
                batch_q = batch_q.where(Batch.department_id == default_dept.id)
            default_batch = (await db.execute(batch_q)).scalars().first()
            if not default_batch:
                default_batch = (await db.execute(select(Batch).where(func.replace(Batch.batch_name, "–", "-").ilike(f"%{clean_batch}%")))).scalars().first()
        if not default_batch and default_dept:
            default_batch = (await db.execute(select(Batch).where(Batch.department_id == default_dept.id, Batch.is_active == True))).scalars().first()
        if not default_batch:
            default_batch = (await db.execute(select(Batch).where(Batch.is_active == True))).scalars().first()
        if not default_batch:
            default_batch = Batch(
                id=uuid.uuid4(),
                department_id=default_dept.id,
                batch_name="2024-2028",
                admission_year=2024,
                graduation_year=2028,
                is_active=True,
            )
            db.add(default_batch)
            await db.flush()

        # 3. Resolve default Section
        default_sec = None
        if payload.default_section_id:
            try:
                default_sec = (await db.execute(select(Section).where(Section.id == uuid.UUID(payload.default_section_id)))).scalar_one_or_none()
            except Exception:
                pass
        if not default_sec and payload.default_section_name:
            sec_clean = payload.default_section_name.replace("Section", "").strip()
            sec_q = select(Section).where(func.replace(Section.name, "Section", "").ilike(f"%{sec_clean}%"))
            if default_batch:
                sec_q = sec_q.where(Section.batch_id == default_batch.id)
            default_sec = (await db.execute(sec_q)).scalars().first()
            if not default_sec:
                default_sec = (await db.execute(select(Section).where(func.replace(Section.name, "Section", "").ilike(f"%{sec_clean}%")))).scalars().first()
        if not default_sec and default_batch:
            default_sec = (await db.execute(select(Section).where(Section.batch_id == default_batch.id))).scalars().first()
        if not default_sec:
            default_sec = (await db.execute(select(Section).where(Section.is_active == True))).scalars().first()
        if not default_sec:
            default_sec = Section(id=uuid.uuid4(), batch_id=default_batch.id, name="A", is_active=True)
            db.add(default_sec)
            await db.flush()

        for item in payload.students:
            reg = item.register_number.strip().upper()
            if not reg or not item.full_name:
                skipped_count += 1
                results.append({"register_number": reg, "status": "SKIPPED", "reason": "Missing required fields"})
                continue

            # Predefined password rule
            pwd = item.generated_password or generate_predefined_password(item.full_name, reg)

            # Resolve email
            first_token = item.full_name.split()[0].lower() if item.full_name.split() else "student"
            email = item.email or f"{first_token}.{reg.lower()}@suguna.edu.in"

            # Parse DOB
            st_dob = None
            if item.date_of_birth:
                if isinstance(item.date_of_birth, date):
                    st_dob = item.date_of_birth
                elif isinstance(item.date_of_birth, str) and item.date_of_birth.strip():
                    try:
                        st_dob = date.fromisoformat(item.date_of_birth.strip()[:10])
                    except Exception:
                        pass

            # Check if student exists
            existing_student = (await db.execute(select(Student).where(Student.register_number == reg))).scalar_one_or_none()
            if existing_student:
                if conflict_strategy == "update":
                    existing_student.full_name = item.full_name.strip()
                    existing_student.email = email
                    if item.phone:
                        existing_student.phone = item.phone.strip()
                    if st_dob:
                        existing_student.date_of_birth = st_dob
                    if item.blood_group:
                        existing_student.blood_group = item.blood_group.strip()
                    if item.address:
                        existing_student.address = item.address.strip()
                    if default_dept:
                        existing_student.department_id = default_dept.id
                    if default_batch:
                        existing_student.batch_id = default_batch.id
                    if default_sec:
                        existing_student.section_id = default_sec.id

                    # Also update User credentials
                    user_rec = (await db.execute(select(User).where(User.id == existing_student.user_id))).scalar_one_or_none()
                    if user_rec:
                        user_rec.password_hash = get_password_hash(pwd)
                        user_rec.is_active = True

                    enrolled_count += 1
                    results.append({
                        "register_number": reg,
                        "name": item.full_name,
                        "status": "UPDATED",
                        "generated_password": pwd,
                        "email": email,
                    })
                    continue
                else:
                    skipped_count += 1
                    results.append({"register_number": reg, "name": item.full_name, "status": "SKIPPED", "reason": "Already exists"})
                    continue

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
                phone=item.phone.strip() if item.phone else None,
                date_of_birth=st_dob,
                blood_group=item.blood_group.strip() if item.blood_group else None,
                address=item.address.strip() if item.address else None,
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

    # ─────────────────────────────────────────────────────────
    # Staff Onboarding Services
    # ─────────────────────────────────────────────────────────
    @staticmethod
    async def enroll_staff(db: AsyncSession, payload: StaffEnrollRequest) -> StaffEnrollResponse:
        """Enroll single faculty/staff member with auto or custom credentials."""
        fid = payload.faculty_id.strip().upper()

        existing_staff = (await db.execute(select(Staff).where(Staff.faculty_id == fid))).scalar_one_or_none()
        if existing_staff:
            raise ConflictException(f"Staff member with Faculty ID '{fid}' already exists.")

        existing_user = (await db.execute(select(User).where(User.identifier == fid))).scalar_one_or_none()
        if existing_user:
            raise ConflictException(f"User account with identifier '{fid}' already exists.")

        # Resolve Department
        dept = None
        if payload.department_id:
            try:
                dept = (await db.execute(select(Department).where(Department.id == uuid.UUID(payload.department_id)))).scalar_one_or_none()
            except Exception:
                pass
        if not dept and payload.department_code:
            dept = (await db.execute(select(Department).where(func.upper(Department.code) == payload.department_code.strip().upper()))).scalar_one_or_none()
        if not dept and payload.department_name:
            dept = (await db.execute(select(Department).where(Department.name.ilike(f"%{payload.department_name.strip()}%")))).scalars().first()
        if not dept:
            dept = (await db.execute(select(Department).where(Department.is_active == True))).scalars().first()
        if not dept:
            dept = Department(id=uuid.uuid4(), name="Artificial Intelligence & Data Science", code="AIDS", is_active=True)
            db.add(dept)
            await db.flush()

        pwd = payload.custom_password or generate_predefined_password(payload.full_name, fid)
        clean_name = payload.full_name.lower().replace("dr.", "").replace("prof.", "").strip().split()[0] if payload.full_name else "faculty"
        email = payload.email.strip() if payload.email else f"{clean_name}.{fid.lower()}@suguna.edu.in"

        new_user = User(
            id=uuid.uuid4(),
            identifier=fid,
            password_hash=get_password_hash(pwd),
            role="STAFF",
            is_active=True,
        )
        db.add(new_user)
        await db.flush()

        new_staff = Staff(
            id=uuid.uuid4(),
            user_id=new_user.id,
            department_id=dept.id,
            faculty_id=fid,
            full_name=payload.full_name.strip(),
            designation=payload.designation or "Assistant Professor",
            email=email,
            phone=payload.phone.strip() if payload.phone else None,
            cabin_number=payload.cabin_number.strip() if payload.cabin_number else None,
            qualifications=payload.qualifications.strip() if payload.qualifications else None,
            experience=payload.experience.strip() if payload.experience else None,
            avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed={fid}",
            is_active=True,
        )
        db.add(new_staff)
        await db.commit()

        return StaffEnrollResponse(
            id=str(new_staff.id),
            user_id=str(new_user.id),
            faculty_id=fid,
            full_name=new_staff.full_name,
            email=new_staff.email,
            generated_password=pwd,
            designation=new_staff.designation,
            department_name=dept.name,
            message="Faculty member registered successfully with STAFF role.",
        )

    @staticmethod
    async def bulk_enroll_staff(db: AsyncSession, payload: BulkStaffEnrollRequest) -> BulkStaffEnrollResponse:
        """Bulk enroll faculty members from spreadsheet upload."""
        results = []
        enrolled_count = 0
        skipped_count = 0
        conflict_strategy = (payload.conflict_strategy or "skip").strip().lower()

        default_dept = None
        if payload.default_department_code:
            default_dept = (await db.execute(select(Department).where(func.upper(Department.code) == payload.default_department_code.strip().upper()))).scalar_one_or_none()
        if not default_dept:
            default_dept = (await db.execute(select(Department).where(Department.is_active == True))).scalars().first()

        for item in payload.staff_members:
            fid = item.faculty_id.strip().upper()
            if not fid or not item.full_name:
                skipped_count += 1
                results.append({"faculty_id": fid, "status": "SKIPPED", "reason": "Missing required fields"})
                continue

            pwd = item.generated_password or generate_predefined_password(item.full_name, fid)
            clean_name = item.full_name.lower().replace("dr.", "").replace("prof.", "").strip().split()[0] if item.full_name else "faculty"
            email = item.email.strip() if item.email else f"{clean_name}.{fid.lower()}@suguna.edu.in"

            # Check if staff exists
            existing_staff = (await db.execute(select(Staff).where(Staff.faculty_id == fid))).scalar_one_or_none()
            if existing_staff:
                if conflict_strategy == "update":
                    existing_staff.full_name = item.full_name.strip()
                    existing_staff.email = email
                    if item.designation:
                        existing_staff.designation = item.designation.strip()
                    if item.phone:
                        existing_staff.phone = item.phone.strip()
                    if item.cabin_number:
                        existing_staff.cabin_number = item.cabin_number.strip()
                    if item.qualifications:
                        existing_staff.qualifications = item.qualifications.strip()
                    if item.experience:
                        existing_staff.experience = item.experience.strip()

                    user_rec = (await db.execute(select(User).where(User.id == existing_staff.user_id))).scalar_one_or_none()
                    if user_rec:
                        user_rec.password_hash = get_password_hash(pwd)
                        user_rec.is_active = True

                    enrolled_count += 1
                    results.append({"faculty_id": fid, "name": item.full_name, "status": "UPDATED", "email": email, "generated_password": pwd})
                    continue
                else:
                    skipped_count += 1
                    results.append({"faculty_id": fid, "name": item.full_name, "status": "SKIPPED", "reason": "Already exists"})
                    continue

            user = User(
                id=uuid.uuid4(),
                identifier=fid,
                password_hash=get_password_hash(pwd),
                role="STAFF",
                is_active=True,
            )
            db.add(user)
            await db.flush()

            st = Staff(
                id=uuid.uuid4(),
                user_id=user.id,
                department_id=default_dept.id if default_dept else None,
                faculty_id=fid,
                full_name=item.full_name.strip(),
                designation=item.designation or "Assistant Professor",
                email=email,
                phone=item.phone.strip() if item.phone else None,
                cabin_number=item.cabin_number.strip() if item.cabin_number else None,
                qualifications=item.qualifications.strip() if item.qualifications else None,
                experience=item.experience.strip() if item.experience else None,
                avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed={fid}",
                is_active=True,
            )
            db.add(st)
            enrolled_count += 1
            results.append({"faculty_id": fid, "name": item.full_name, "status": "ENROLLED", "email": email, "generated_password": pwd})

        await db.commit()
        return BulkStaffEnrollResponse(
            total_processed=len(payload.staff_members),
            enrolled_count=enrolled_count,
            skipped_count=skipped_count,
            results=results,
        )

    @staticmethod
    async def get_all_staff(db: AsyncSession) -> List[Dict[str, Any]]:
        """Fetch all active faculty members."""
        stmt = select(Staff).options(selectinload(Staff.department)).where(Staff.is_active == True).order_by(Staff.full_name)
        staff_list = (await db.execute(stmt)).scalars().all()
        return [
            {
                "id": str(s.id),
                "faculty_id": s.faculty_id,
                "full_name": s.full_name,
                "designation": s.designation,
                "department": s.department.name if s.department else "General",
                "email": s.email,
                "phone": s.phone,
                "cabin_number": s.cabin_number,
                "avatar_url": s.avatar_url,
            }
            for s in staff_list
        ]

    # ─────────────────────────────────────────────────────────
    # Mentor & Proctor Allocation Services
    # ─────────────────────────────────────────────────────────
    @staticmethod
    async def get_faculty_mentors(db: AsyncSession) -> List[FacultyMentorItem]:
        """Fetch faculty mentors with their assigned student counts and capacity."""
        staff_stmt = select(Staff).options(selectinload(Staff.department)).where(Staff.is_active == True).order_by(Staff.full_name)
        staff_members = (await db.execute(staff_stmt)).scalars().all()

        results = []
        for s in staff_members:
            count_stmt = select(func.count(Student.id)).where(Student.faculty_mentor_id == s.id, Student.is_active == True)
            assigned_count = (await db.execute(count_stmt)).scalar() or 0
            dept_name = s.department.name if s.department else "General"
            title = f"{s.designation} • {dept_name}"
            results.append(
                FacultyMentorItem(
                    id=str(s.id),
                    faculty_id=s.faculty_id,
                    name=s.full_name,
                    title=title,
                    department=dept_name,
                    assigned=assigned_count,
                    capacity=20,
                )
            )
        return results

    @staticmethod
    async def get_student_allocation(
        db: AsyncSession,
        department_name: Optional[str] = None,
        batch_name: Optional[str] = None,
        section_name: Optional[str] = None,
        status_filter: Optional[str] = "all",
        search: Optional[str] = None,
    ) -> StudentAllocationResponse:
        """Fetch students for mentor allocation with filter and search capabilities."""
        stmt = select(Student).options(
            selectinload(Student.department),
            selectinload(Student.batch),
            selectinload(Student.section),
            selectinload(Student.faculty_mentor),
        ).where(Student.is_active == True)

        if department_name and department_name.strip():
            dept_term = department_name.strip()
            stmt = stmt.join(Student.department).where(Department.name.ilike(f"%{dept_term}%") | Department.code.ilike(f"%{dept_term}%"))

        if batch_name and batch_name.strip():
            clean_b = batch_name.strip().replace("–", "-").split()[0]
            stmt = stmt.join(Student.batch).where(Batch.batch_name.ilike(f"%{clean_b}%"))

        if section_name and section_name.strip():
            sec_clean = section_name.strip().replace("Sec", "").replace("Section", "").strip()
            stmt = stmt.join(Student.section).where(Section.name.ilike(f"%{sec_clean}%"))

        students_all = (await db.execute(stmt.order_by(Student.register_number))).scalars().all()

        total_count = len(students_all)
        unassigned_count = sum(1 for s in students_all if s.faculty_mentor_id is None)
        assigned_count = total_count - unassigned_count

        filtered = []
        term = search.strip().lower() if search else ""
        s_filter = (status_filter or "all").lower()

        for s in students_all:
            is_assigned = s.faculty_mentor_id is not None
            if s_filter == "unassigned" and is_assigned:
                continue
            if s_filter == "assigned" and not is_assigned:
                continue

            if term:
                match_name = term in s.full_name.lower()
                match_reg = term in s.register_number.lower()
                if not (match_name or match_reg):
                    continue

            # Initials
            parts = [p[0] for p in s.full_name.split() if p]
            initials = "".join(parts[:2]).upper() if parts else "ST"

            sec_display = "Sec A"
            if s.section and s.batch:
                sec_display = f"{s.batch.batch_name} • Sec {s.section.name}"
            elif s.section:
                sec_display = f"Sec {s.section.name}"

            mentor_name = s.faculty_mentor.full_name if s.faculty_mentor else None

            filtered.append(
                StudentAllocationItem(
                    id=str(s.id),
                    register_number=s.register_number,
                    name=s.full_name,
                    section=sec_display,
                    department=s.department.name if s.department else None,
                    batch=s.batch.batch_name if s.batch else None,
                    mentor=mentor_name,
                    mentor_id=str(s.faculty_mentor_id) if s.faculty_mentor_id else None,
                    initials=initials,
                    avatar=s.avatar_url,
                )
            )

        return StudentAllocationResponse(
            students=filtered,
            total_count=total_count,
            unassigned_count=unassigned_count,
            assigned_count=assigned_count,
        )

    @staticmethod
    async def assign_mentor(db: AsyncSession, payload: AssignMentorRequest) -> Dict[str, Any]:
        """Assign list of students to target faculty mentor."""
        if not payload.student_ids:
            return {"success": False, "message": "No students provided for assignment"}

        # Resolve Mentor Staff
        mentor = None
        if payload.faculty_mentor_id:
            try:
                mentor = (await db.execute(select(Staff).where(Staff.id == uuid.UUID(payload.faculty_mentor_id)))).scalar_one_or_none()
            except Exception:
                pass
            if not mentor:
                mentor = (await db.execute(select(Staff).where(Staff.faculty_id == payload.faculty_mentor_id.strip()))).scalar_one_or_none()
            if not mentor:
                mentor = (await db.execute(select(Staff).where(Staff.full_name.ilike(f"%{payload.faculty_mentor_id.strip()}%")))).scalars().first()

        if not mentor:
            raise NotFoundException("Target faculty mentor not found.")

        # Update matching students
        assigned_count = 0
        for sid in payload.student_ids:
            sid_str = sid.strip()
            student = None
            try:
                student = (await db.execute(select(Student).where(Student.id == uuid.UUID(sid_str)))).scalar_one_or_none()
            except Exception:
                pass
            if not student:
                student = (await db.execute(select(Student).where(Student.register_number == sid_str.upper()))).scalar_one_or_none()

            if student:
                student.faculty_mentor_id = mentor.id
                assigned_count += 1

        await db.commit()
        return {
            "success": True,
            "assigned_count": assigned_count,
            "mentor_id": str(mentor.id),
            "mentor_name": mentor.full_name,
            "message": f"Successfully assigned {assigned_count} student(s) to {mentor.full_name}",
        }

    @staticmethod
    async def unassign_mentor(db: AsyncSession, payload: UnassignMentorRequest) -> Dict[str, Any]:
        """Remove mentor assignment from selected students."""
        if not payload.student_ids:
            return {"success": False, "message": "No students provided to unassign"}

        unassigned_count = 0
        for sid in payload.student_ids:
            sid_str = sid.strip()
            student = None
            try:
                student = (await db.execute(select(Student).where(Student.id == uuid.UUID(sid_str)))).scalar_one_or_none()
            except Exception:
                pass
            if not student:
                student = (await db.execute(select(Student).where(Student.register_number == sid_str.upper()))).scalar_one_or_none()

            if student:
                student.faculty_mentor_id = None
                unassigned_count += 1

        await db.commit()
        return {
            "success": True,
            "unassigned_count": unassigned_count,
            "message": f"Successfully removed mentor from {unassigned_count} student(s)",
        }

    @staticmethod
    async def auto_distribute_mentors(db: AsyncSession, payload: AutoDistributeMentorsRequest) -> Dict[str, Any]:
        """Auto-distribute unassigned students across faculty members with available capacity."""
        # 1. Fetch faculty mentors
        staff_query = select(Staff).where(Staff.is_active == True)
        if payload.faculty_ids:
            staff_uuids = []
            for fid in payload.faculty_ids:
                try:
                    staff_uuids.append(uuid.UUID(fid))
                except Exception:
                    pass
            if staff_uuids:
                staff_query = staff_query.where(Staff.id.in_(staff_uuids))

        faculty_list = (await db.execute(staff_query.order_by(Staff.full_name))).scalars().all()
        if not faculty_list:
            raise NotFoundException("No faculty members found for auto-distribution.")

        # Compute remaining capacities
        capacities = []
        for f in faculty_list:
            cnt = (await db.execute(select(func.count(Student.id)).where(Student.faculty_mentor_id == f.id, Student.is_active == True))).scalar() or 0
            capacities.append(max(0, 20 - cnt))

        # 2. Fetch unassigned students
        student_query = select(Student).where(Student.faculty_mentor_id.is_(None), Student.is_active == True)
        if payload.student_ids:
            st_uuids = []
            st_regs = []
            for sid in payload.student_ids:
                try:
                    st_uuids.append(uuid.UUID(sid))
                except Exception:
                    st_regs.append(sid.strip().upper())
            student_query = student_query.where((Student.id.in_(st_uuids)) | (Student.register_number.in_(st_regs)))

        students = (await db.execute(student_query.order_by(Student.register_number))).scalars().all()
        if not students:
            return {"success": True, "distributed_count": 0, "message": "No unassigned students to distribute."}

        # 3. Round-robin assignment
        distributed_count = 0
        f_idx = 0
        total_faculty = len(faculty_list)

        for st in students:
            tries = 0
            while tries < total_faculty and capacities[f_idx] <= 0:
                f_idx = (f_idx + 1) % total_faculty
                tries += 1

            if tries >= total_faculty:
                break  # All faculty capacity full

            st.faculty_mentor_id = faculty_list[f_idx].id
            capacities[f_idx] -= 1
            distributed_count += 1
            f_idx = (f_idx + 1) % total_faculty

        await db.commit()
        return {
            "success": True,
            "distributed_count": distributed_count,
            "message": f"Successfully auto-distributed {distributed_count} student(s) across faculty mentors.",
        }


