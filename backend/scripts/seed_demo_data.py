import asyncio
from datetime import date, datetime, time, timedelta, timezone
import os
import sys
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from sqlalchemy import delete, select
from app.core.database import async_session_maker, engine
from app.core.security import get_password_hash
from app.models.academics import Course, CourseOffering, Period, Room
from app.models.announcements import Announcement, AnnouncementRecipient
from app.models.attendance import AttendanceRecord, AttendanceSession
from app.models.base import Base
from app.models.materials import Material
from app.models.organization import AcademicYear, Batch, Department, Section, Semester
from app.models.profiles import AdminProfile, Staff, Student
from app.models.timetable import TimetableEntry
from app.models.user import User


async def seed():
    print("[INFO] Initializing CMS Database Seeder...")

    # Ensure tables are created
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as db:
        # Check if already seeded
        dept_check = (await db.execute(select(Department).where(Department.code == "AIDS"))).scalar_one_or_none()
        if dept_check:
            print("[CLEANUP] Database already has seed data. Cleaning up old demo records...")
            # For a fresh demo clean slate:
            for tbl in [
                AttendanceRecord,
                AttendanceSession,
                TimetableEntry,
                CourseOffering,
                Material,
                AnnouncementRecipient,
                Announcement,
                Student,
                Staff,
                AdminProfile,
                User,
                Section,
                Batch,
                Course,
                Room,
                Period,
                Semester,
                AcademicYear,
                Department,
            ]:
                await db.execute(delete(tbl))
            await db.commit()

        print("[ACADEMIC] Seeding Departments, Academic Years, and Semesters...")
        dept_aids = Department(
            id=uuid.uuid4(),
            code="AIDS",
            name="Artificial Intelligence & Data Science",
            is_active=True,
        )
        dept_cse = Department(
            id=uuid.uuid4(),
            code="CSE",
            name="Computer Science & Engineering",
            is_active=True,
        )
        db.add_all([dept_aids, dept_cse])

        ay_2024 = AcademicYear(
            id=uuid.uuid4(),
            year_name="2024-2025",
            start_date=date(2024, 7, 1),
            end_date=date(2025, 5, 31),
            is_current=True,
            is_active=True,
        )
        db.add(ay_2024)
        await db.flush()

        sem_5 = Semester(
            id=uuid.uuid4(),
            academic_year_id=ay_2024.id,
            semester_number=5,
            term_type="ODD",
            start_date=date(2024, 7, 15),
            end_date=date(2024, 11, 30),
            is_current=True,
            is_active=True,
        )
        db.add(sem_5)

        batch_22_26 = Batch(
            id=uuid.uuid4(),
            department_id=dept_aids.id,
            batch_name="2022-2026",
            admission_year=2022,
            graduation_year=2026,
            is_active=True,
        )
        db.add(batch_22_26)
        await db.flush()

        sec_a = Section(
            id=uuid.uuid4(),
            batch_id=batch_22_26.id,
            name="A",
            current_semester=5,
            is_active=True,
        )
        sec_b = Section(
            id=uuid.uuid4(),
            batch_id=batch_22_26.id,
            name="B",
            current_semester=5,
            is_active=True,
        )
        db.add_all([sec_a, sec_b])

        print("[COURSES] Seeding Courses and Classrooms...")
        c_dsa = Course(
            id=uuid.uuid4(),
            department_id=dept_aids.id,
            code="CS3301",
            name="Data Structures & Algorithms",
            short_name="DSA",
            credits=3,
            course_type="THEORY",
        )
        c_dbms = Course(
            id=uuid.uuid4(),
            department_id=dept_aids.id,
            code="CS3352",
            name="Database Management Systems",
            short_name="DBMS",
            credits=3,
            course_type="THEORY",
        )
        c_dl = Course(
            id=uuid.uuid4(),
            department_id=dept_aids.id,
            code="AD3501",
            name="Deep Learning & Neural Networks",
            short_name="DL",
            credits=3,
            course_type="THEORY",
        )
        c_dllab = Course(
            id=uuid.uuid4(),
            department_id=dept_aids.id,
            code="AD3511",
            name="Deep Learning Laboratory",
            short_name="DL Lab",
            credits=2,
            course_type="LAB",
        )
        c_ml = Course(
            id=uuid.uuid4(),
            department_id=dept_aids.id,
            code="CS3351",
            name="Machine Learning Techniques",
            short_name="ML",
            credits=3,
            course_type="THEORY",
        )
        c_os = Course(
            id=uuid.uuid4(),
            department_id=dept_aids.id,
            code="CS3451",
            name="Operating Systems",
            short_name="OS",
            credits=3,
            course_type="THEORY",
        )
        db.add_all([c_dsa, c_dbms, c_dl, c_dllab, c_ml, c_os])

        r_204 = Room(
            id=uuid.uuid4(),
            department_id=dept_aids.id,
            room_number="Room 204",
            building="Theory Wing (Second Floor)",
            capacity=60,
            room_type="CLASSROOM",
        )
        r_302 = Room(
            id=uuid.uuid4(),
            department_id=dept_aids.id,
            room_number="Room 302",
            building="Turing Hall (Third Floor)",
            capacity=70,
            room_type="CLASSROOM",
        )
        r_lab2 = Room(
            id=uuid.uuid4(),
            department_id=dept_aids.id,
            room_number="AI Lab 2",
            building="Advanced Computing Wing",
            capacity=45,
            room_type="LAB",
        )
        db.add_all([r_204, r_302, r_lab2])

        print("[PERIODS] Seeding Periods & Break Schedules...")
        periods_data = [
            (1, "P1", time(8, 45), time(9, 35), False),
            (2, "P2", time(9, 35), time(10, 25), False),
            (3, "Morning Tea Break", time(10, 25), time(10, 40), True),
            (4, "P3", time(10, 40), time(11, 30), False),
            (5, "P4", time(11, 30), time(12, 20), False),
            (6, "Lunch Break", time(12, 20), time(13, 10), True),
            (7, "P5", time(13, 10), time(14, 0), False),
            (8, "P6", time(14, 0), time(14, 50), False),
            (9, "P7", time(14, 50), time(15, 40), False),
        ]
        period_objs = {}
        for num, name, st, et, is_b in periods_data:
            p = Period(id=uuid.uuid4(), period_number=num, name=name, start_time=st, end_time=et, is_break=is_b)
            db.add(p)
            period_objs[num] = p

        await db.flush()

        print("[STAFF] Seeding Staff Members & Administrators...")
        default_pwd = get_password_hash("Password123!")
        admin_pwd = get_password_hash("AdminPassword123!")

        # Faculty 1: Dr. Kumar
        u_kumar = User(identifier="FAC-2024-001", password_hash=default_pwd, role="STAFF")
        db.add(u_kumar)
        await db.flush()
        stf_kumar = Staff(
            id=uuid.uuid4(),
            user_id=u_kumar.id,
            department_id=dept_aids.id,
            faculty_id="FAC-2024-001",
            full_name="Dr. Kumar",
            designation="Associate Professor",
            email="kumar.ad@suguna.edu",
            phone="+91 9443211220",
            cabin_number="Cabin #312",
            qualifications="Ph.D. (Deep Learning), M.E.",
            experience="12 Years",
            avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=256",
        )
        db.add(stf_kumar)

        # Faculty 2: Prof. Saravanan M
        u_saravanan = User(identifier="FAC-2024-002", password_hash=default_pwd, role="STAFF")
        db.add(u_saravanan)
        await db.flush()
        stf_saravanan = Staff(
            id=uuid.uuid4(),
            user_id=u_saravanan.id,
            department_id=dept_aids.id,
            faculty_id="FAC-2024-002",
            full_name="Prof. Saravanan M",
            designation="Assistant Professor (Sr. Gr.)",
            email="saravanan.cs@suguna.edu",
            phone="+91 9842155667",
            cabin_number="Cabin #208",
            qualifications="M.Tech (Data Systems)",
            experience="8 Years",
            avatar_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=256",
        )
        db.add(stf_saravanan)

        # Faculty 3: Dr. Arulprakash P (HOD)
        u_arulprakash = User(identifier="FAC-2024-003", password_hash=default_pwd, role="STAFF")
        db.add(u_arulprakash)
        await db.flush()
        stf_arulprakash = Staff(
            id=uuid.uuid4(),
            user_id=u_arulprakash.id,
            department_id=dept_aids.id,
            faculty_id="FAC-2024-003",
            full_name="Dr. Arulprakash P",
            designation="Professor & Head",
            email="hod.aids@suguna.edu",
            phone="+91 9843099881",
            cabin_number="HOD Office Suite",
            qualifications="Ph.D, M.E, Post-Doc (NUS)",
            experience="18 Years",
            avatar_url="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&q=80&w=256",
        )
        db.add(stf_arulprakash)

        # Admin User: admin
        u_admin = User(identifier="admin", password_hash=admin_pwd, role="ADMIN")
        db.add(u_admin)
        await db.flush()
        admin_prof = AdminProfile(
            id=uuid.uuid4(),
            user_id=u_admin.id,
            department_id=dept_aids.id,
            full_name="Dr. V. Rajesh",
            designation="Dean of Academic Governance",
            email="admin@suguna.edu",
            phone="+91 9442100001",
            office_location="Office of Academic Governance • Suite 101",
            avatar_url="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&q=80&w=256",
        )
        db.add(admin_prof)

        print("[STUDENTS] Seeding Students...")
        students_roster = [
            ("714022AD001", "Arjun Patel", "arjun.p@suguna.edu", 8.75, "O+", "+91 9876543210", "+91 9876500000", "Rajesh Patel", "142, North Street, Coimbatore"),
            ("714022AD002", "Priya Sharma", "priya.s@suguna.edu", 9.10, "A+", "+91 9876543211", "+91 9876500001", "Sanjay Sharma", "54, Gandhi Nagar, Coimbatore"),
            ("714022AD003", "Rahul V", "rahul.v@suguna.edu", 7.20, "B+", "+91 9876543212", "+91 9876500002", "Vijay Kumar", "12, Crosscut Road, Coimbatore"),
            ("714022AD004", "Sneha K", "sneha.k@suguna.edu", 8.40, "AB+", "+91 9876543213", "+91 9876500003", "Krishnan S", "88, R.S. Puram, Coimbatore"),
            ("714022AD005", "Dinesh M", "dinesh.m@suguna.edu", 6.95, "O-", "+91 9876543214", "+91 9876500004", "Murugan K", "102, Peelamedu, Coimbatore"),
            ("714022AD006", "Ananya R", "ananya.r@suguna.edu", 8.90, "A-", "+91 9876543215", "+91 9876500005", "Ramanathan G", "23, Saibaba Colony, Coimbatore"),
            ("714022AD007", "Karthik B", "karthik.b@suguna.edu", 7.65, "B-", "+91 9876543216", "+91 9876500006", "Balaji T", "71, Race Course, Coimbatore"),
            ("714022AD008", "Meera N", "meera.n@suguna.edu", 9.35, "O+", "+91 9876543217", "+91 9876500007", "Narayanan S", "9, Avinashi Road, Coimbatore"),
        ]

        student_objs = []
        for reg, name, email, cgpa, bg, ph, pph, pname, addr in students_roster:
            u = User(identifier=reg, password_hash=default_pwd, role="STUDENT")
            db.add(u)
            await db.flush()
            st = Student(
                id=uuid.uuid4(),
                user_id=u.id,
                department_id=dept_aids.id,
                batch_id=batch_22_26.id,
                section_id=sec_a.id,
                faculty_mentor_id=stf_kumar.id,
                register_number=reg,
                full_name=name,
                email=email,
                phone=ph,
                parent_name=pname,
                parent_phone=pph,
                date_of_birth=date(2004, 5, 14),
                blood_group=bg,
                address=addr,
                avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed={reg}",
                cgpa=cgpa,
                is_active=True,
            )
            db.add(st)
            student_objs.append(st)

        print("[TIMETABLE] Seeding Timetable Entries (Monday to Friday)...")
        # Monday Timetable
        tt_p1 = TimetableEntry(
            section_id=sec_a.id,
            course_id=c_dsa.id,
            staff_id=stf_saravanan.id,
            room_id=r_204.id,
            period_id=period_objs[1].id,
            day_of_week=1,
            lecture_type="THEORY",
            is_active=True,
        )
        tt_p2 = TimetableEntry(
            section_id=sec_a.id,
            course_id=c_dbms.id,
            staff_id=stf_saravanan.id,
            room_id=r_204.id,
            period_id=period_objs[2].id,
            day_of_week=1,
            lecture_type="THEORY",
            is_active=True,
        )
        tt_p3 = TimetableEntry(
            section_id=sec_a.id,
            course_id=c_dl.id,
            staff_id=stf_kumar.id,
            room_id=r_302.id,
            period_id=period_objs[4].id,
            day_of_week=1,
            lecture_type="THEORY",
            is_active=True,
        )
        tt_p4 = TimetableEntry(
            section_id=sec_a.id,
            course_id=c_dllab.id,
            staff_id=stf_kumar.id,
            room_id=r_lab2.id,
            period_id=period_objs[5].id,
            day_of_week=1,
            lecture_type="LAB",
            batch_split="Batch 1 & 2",
            is_active=True,
        )
        tt_p5 = TimetableEntry(
            section_id=sec_a.id,
            course_id=c_os.id,
            staff_id=stf_arulprakash.id,
            room_id=r_204.id,
            period_id=period_objs[7].id,
            day_of_week=1,
            lecture_type="THEORY",
            is_active=True,
        )
        db.add_all([tt_p1, tt_p2, tt_p3, tt_p4, tt_p5])

        # Tuesday schedule
        tt_tue1 = TimetableEntry(
            section_id=sec_a.id,
            course_id=c_ml.id,
            staff_id=stf_kumar.id,
            room_id=r_302.id,
            period_id=period_objs[1].id,
            day_of_week=2,
            lecture_type="THEORY",
            is_active=True,
        )
        tt_tue2 = TimetableEntry(
            section_id=sec_a.id,
            course_id=c_dl.id,
            staff_id=stf_kumar.id,
            room_id=r_302.id,
            period_id=period_objs[2].id,
            day_of_week=2,
            lecture_type="THEORY",
            is_active=True,
        )
        db.add_all([tt_tue1, tt_tue2])

        await db.flush()

        print("[ATTENDANCE] Seeding Attendance History & Sessions...")
        # Session 1: Yesterday
        yesterday = date.today() - timedelta(days=1)
        sess_1 = AttendanceSession(
            timetable_entry_id=tt_p1.id,
            staff_id=stf_saravanan.id,
            date=yesterday,
            conducted_hours=1,
            topic_covered="Binary Search Trees and AVL Rotations",
            present_count=7,
            absent_count=1,
            od_count=0,
            total_marked=8,
        )
        db.add(sess_1)
        await db.flush()

        for idx, st in enumerate(student_objs):
            # student 5 is absent to test defaulter
            status = "ABSENT" if idx == 4 else "PRESENT"
            db.add(AttendanceRecord(
                attendance_session_id=sess_1.id,
                student_id=st.id,
                status=status,
            ))

        # Session 2: Deep Learning with Dr. Kumar
        sess_2 = AttendanceSession(
            timetable_entry_id=tt_p3.id,
            staff_id=stf_kumar.id,
            date=yesterday,
            conducted_hours=1,
            topic_covered="Backpropagation in Multi-Layer Perceptrons",
            present_count=7,
            absent_count=0,
            od_count=1,
            total_marked=8,
        )
        db.add(sess_2)
        await db.flush()

        for idx, st in enumerate(student_objs):
            status = "ON_DUTY" if idx == 2 else "PRESENT"
            db.add(AttendanceRecord(
                attendance_session_id=sess_2.id,
                student_id=st.id,
                status=status,
            ))

        print("[MATERIALS] Seeding Study Materials...")
        os.makedirs("./uploads", exist_ok=True)
        dummy_file = "./uploads/demo_notes.pdf"
        if not os.path.exists(dummy_file):
            with open(dummy_file, "w") as f:
                f.write("%PDF-1.4 Demonstration PDF file for Nexus CMS Study Materials")

        m1 = Material(
            course_id=c_dl.id,
            uploaded_by=stf_kumar.id,
            title="Introduction to Deep Neural Networks & Backprop",
            unit="Unit 1",
            topic="Architectures, Activation Functions & Loss Surfaces",
            material_type="LECTURE_NOTE",
            file_path=dummy_file,
            file_format="PDF",
            file_size_bytes=4400000,
            page_count=24,
            reads_count=1420,
            downloads_count=520,
            is_active=True,
        )
        m2 = Material(
            course_id=c_dbms.id,
            uploaded_by=stf_saravanan.id,
            title="Relational Algebra, SQL & Normal Forms (1NF to BCNF)",
            unit="Unit 2",
            topic="Schema Normalization and Functional Dependencies",
            material_type="LECTURE_NOTE",
            file_path=dummy_file,
            file_format="PDF",
            file_size_bytes=3100000,
            page_count=18,
            reads_count=890,
            downloads_count=310,
            is_active=True,
        )
        m3 = Material(
            course_id=c_dsa.id,
            uploaded_by=stf_saravanan.id,
            title="End Semester Question Bank & Model Solutions",
            unit="Unit 1-5",
            topic="Comprehensive 2-Mark & 16-Mark Question Bank",
            material_type="QUESTION_BANK",
            file_path=dummy_file,
            file_format="PDF",
            file_size_bytes=5200000,
            page_count=36,
            reads_count=2100,
            downloads_count=980,
            is_active=True,
        )
        db.add_all([m1, m2, m3])

        print("[ANNOUNCEMENTS] Seeding Campus Circulars & Announcements...")
        ann_coe = Announcement(
            category="coe",
            reference_number="CIR/SCE/2024-25/089",
            title="Revaluation & Paper Viewing Window - June/July Session",
            heading="Revaluation & Answer Script Verification Window for UG Sem II & IV",
            content="Candidates interested in script xerox copies and subsequent revaluation are requested to register through their student portal before October 26, 2024. Nominal fee of ₹400 per course applies.",
            department_name="Controller of Examinations",
            tag="Autonomous",
            badge="CoE",
            badge_type="blue",
            footer="Signed by Dr. K. Ramanathan",
            publish_date=date(2024, 10, 18),
            is_active=True,
        )
        ann_placement = Announcement(
            category="placement",
            reference_number="T&P/2024-25/042",
            title="Campus Placement Drive by HexaCorp Tech Solutions",
            heading="Campus Recruitment Drive 2025 Batch: HexaCorp Solutions (CTC 9.5 LPA)",
            content="Online technical assessment will be conducted at Campus Lab 4 & 5 on Saturday, Oct 21. Students with minimum CGPA 7.5 and no standing arrears must report in formal dress code by 8:30 AM.",
            department_name="Training & Placement Cell",
            tag="Eligible: CSE/ECE/AIDS",
            badge="T&P",
            badge_type="gray",
            footer="Venue: Seminar Hall III",
            publish_date=date(2024, 10, 17),
            is_active=True,
        )
        ann_acad = Announcement(
            category="academic",
            reference_number="ACAD/REG/2024/118",
            title="Internal Assessment II Schedule & Syllabus Coverage",
            heading="Continuous Internal Assessment (CIA-II) Exam Schedule",
            content="Internal Assessment II for all III and IV Year UG students will commence from November 4, 2024. Question paper will cover 100% of Units 3, 4, and 5.",
            department_name="Office of Academic Affairs",
            tag="Dean Academics",
            badge="ACD",
            badge_type="blueDim",
            footer="Office of Academic Governance",
            publish_date=date(2024, 10, 15),
            is_active=True,
        )
        db.add_all([ann_coe, ann_placement, ann_acad])

        await db.commit()
        print("[SUCCESS] Demo Data Seeding Completed Successfully!")
        print("\n[CREDENTIALS] Demo Credentials:")
        print("   * Student : Identifier: 714022AD001   | Password: Password123!")
        print("   * Faculty : Identifier: FAC-2024-001  | Password: Password123!")
        print("   * Admin   : Identifier: admin         | Password: AdminPassword123!")


if __name__ == "__main__":
    asyncio.run(seed())
