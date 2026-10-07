import asyncio
from app.core.database import async_session_maker
from app.models.user import User
from app.models.profiles import Student
from sqlalchemy import select
from app.core.security import verify_password

async def check():
    async with async_session_maker() as db:
        res = await db.execute(select(Student))
        students = res.scalars().all()
        print(f"Total students: {len(students)}")
        for s in students:
            u = await db.get(User, s.user_id)
            if not u:
                print(f"Student without user: {s.register_number}")
                continue
            test_pw1 = verify_password("Student@123", u.password_hash)
            name_clean = "".join(c for c in s.full_name if c.isalpha()).lower()[:3]
            reg_digits = "".join(c for c in s.register_number if c.isdigit())[-3:]
            formula_pw = name_clean + reg_digits
            test_pw_formula = verify_password(formula_pw, u.password_hash)
            test_pw_reg = verify_password(s.register_number.lower(), u.password_hash)
            print(f"Identifier: '{u.identifier}' | Reg: '{s.register_number}' | Name: {s.full_name} | Matches 'Student@123': {test_pw1} | Matches formula ('{formula_pw}'): {test_pw_formula} | Matches reg: {test_pw_reg}")

if __name__ == "__main__":
    asyncio.run(check())
