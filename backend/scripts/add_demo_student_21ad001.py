import asyncio
import uuid
from datetime import date
from sqlalchemy import select
from app.core.database import async_session_maker
from app.core.security import get_password_hash
from app.models.organization import Batch, Department, Section
from app.models.profiles import Staff, Student
from app.models.user import User

async def main():
    async with async_session_maker() as db:
        # Check if 21AD001 already exists
        existing = (await db.execute(select(Student).where(Student.register_number == "21AD001"))).scalar_one_or_none()
        if existing:
            print("Student 21AD001 already exists in database.")
            # Ensure password is set to Student@123
            u = await db.get(User, existing.user_id)
            if u:
                u.password_hash = get_password_hash("Student@123")
                await db.commit()
                print("Updated password to Student@123")
            return

        # Fetch department AIDS
        dept = (await db.execute(select(Department).where(Department.code == "AIDS"))).scalars().first()
        if not dept:
            dept = (await db.execute(select(Department))).scalars().first()

        # Fetch batch
        batch = (await db.execute(select(Batch))).scalars().first()

        # Fetch section
        sec = (await db.execute(select(Section))).scalars().first()

        # Fetch mentor
        mentor = (await db.execute(select(Staff))).scalars().first()

        # Create user
        user = User(
            id=uuid.uuid4(),
            identifier="21AD001",
            password_hash=get_password_hash("Student@123"),
            role="STUDENT",
            is_active=True,
        )
        db.add(user)
        await db.flush()

        student = Student(
            id=uuid.uuid4(),
            user_id=user.id,
            department_id=dept.id,
            batch_id=batch.id,
            section_id=sec.id,
            faculty_mentor_id=mentor.id if mentor else None,
            register_number="21AD001",
            full_name="Kavitha R",
            email="kavitha.21ad001@suguna.edu.in",
            phone="+91 9876543299",
            date_of_birth=date(2003, 6, 12),
            blood_group="B+",
            address="56, Avinashi Road, Coimbatore",
            avatar_url="https://api.dicebear.com/7.x/avataaars/svg?seed=21AD001",
            cgpa=8.50,
            is_active=True,
        )
        db.add(student)
        await db.commit()
        print("Successfully created student 21AD001 with password Student@123!")

if __name__ == "__main__":
    asyncio.run(main())
