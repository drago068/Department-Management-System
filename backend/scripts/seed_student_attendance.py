import sys
sys.path.insert(0, ".")
import asyncio
import random
import uuid
from datetime import date, datetime, timedelta, timezone

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.core.database import async_session_maker
from app.models.academics import Course, Period, Room
from app.models.attendance import AttendanceRecord, AttendanceSession
from app.models.organization import Section
from app.models.profiles import Staff, Student
from app.models.timetable import TimetableEntry
from sqlalchemy import select, delete, insert

TOPICS = {
    "CS3301": [
        "Singly and Doubly Linked Lists Implementations",
        "Stack Applications - Expression Evaluation",
        "Queue and Priority Queue Operations",
        "Binary Search Trees & Traversal Algorithms",
        "AVL Trees & Self-Balancing Rotations",
        "B-Trees & Multilevel Indexing",
        "Graph Representations: Adjacency List & Matrix",
        "Breadth-First and Depth-First Search Algorithms",
        "Dijkstra Shortest Path Implementation",
        "Minimum Spanning Trees: Kruskal & Prim",
    ],
    "CS3352": [
        "Relational Model & Codd's Rules",
        "Relational Algebra & Tuple Calculus",
        "Complex SQL Queries, Subqueries & Joins",
        "Integrity Constraints & Triggers",
        "Functional Dependencies & 1NF/2NF Normalization",
        "Boyce-Codd Normal Form (BCNF) & 3NF Decomposition",
        "Storage Organization & B+ Tree Indexing",
        "Transaction ACID Properties & State Diagram",
        "Concurrency Control: Two-Phase Locking (2PL)",
        "Deadlock Prevention & Recovery Protocols",
    ],
    "AD3501": [
        "Biological Neurons to Artificial Perceptrons",
        "Multi-Layer Perceptrons & Universal Approximation",
        "Backpropagation Mathematics & Gradient Descent",
        "Loss Functions & Cross-Entropy Optimization",
        "Activation Functions: ReLU, Leaky ReLU, GELU",
        "Convolution Operations, Strides & Pooling Layers",
        "Modern CNN Architectures: ResNet & EfficientNet",
        "Batch Normalization, Dropout & Regularization",
        "Recurrent Neural Networks & Vanishing Gradients",
        "Attention Mechanisms & Transformer Self-Attention",
    ],
    "AD3511": [
        "PyTorch / TensorFlow Tensor Manipulations",
        "Building and Training Feedforward MLPs",
        "Image Classification on CIFAR-10 with CNN",
        "Data Augmentation & Learning Rate Schedulers",
        "Transfer Learning using Pretrained ResNet50",
        "Semantic Segmentation with U-Net",
    ],
    "CS3351": [
        "Supervised vs Unsupervised Learning Paradigms",
        "Linear Regression & Cost Function Optimization",
        "Logistic Regression & Classification Thresholds",
        "Evaluation Metrics: Precision, Recall, F1 & ROC-AUC",
        "Decision Trees & Information Gain / Gini Impurity",
        "Ensemble Methods: Random Forests & AdaBoost",
        "Support Vector Machines (SVM) & Kernel Trick",
        "K-Means Clustering & Elbow Method Evaluation",
        "Principal Component Analysis (PCA) Dimensionality Reduction",
        "Cross-Validation & Hyperparameter Tuning Strategies",
    ],
    "CS3451": [
        "Operating System Structures & System Call Architecture",
        "Process Lifecycle & Process Control Blocks (PCB)",
        "CPU Scheduling: FCFS, Round Robin & Priority Scheduling",
        "Critical Section Problem & Peterson's Algorithm",
        "Counting Semaphores & Mutex Locks",
        "Deadlock Characterization & Resource Allocation Graphs",
        "Banker's Algorithm for Deadlock Avoidance",
        "Memory Management: Paging & Segmentation",
        "Virtual Memory & Demand Paging Mechanics",
        "Page Replacement Algorithms: FIFO, LRU, Optimal",
    ],
}

async def seed_attendance():
    async with async_session_maker() as db:
        print("[SEED] Fetching Section A...")
        sec_stmt = select(Section).where(Section.name == "A")
        sec_a = (await db.execute(sec_stmt)).scalars().first()
        if not sec_a:
            print("Section A not found!")
            return

        print(f"[SEED] Found Section A: {sec_a.id}")

        # Fetch all courses
        courses_res = (await db.execute(select(Course))).scalars().all()
        courses_map = {c.code: c for c in courses_res}

        # Fetch staff
        staff_res = (await db.execute(select(Staff))).scalars().all()
        staff_by_name = {s.full_name: s for s in staff_res}
        stf_kumar = staff_by_name.get("Dr. Kumar")
        stf_saravanan = staff_by_name.get("Prof. Saravanan M")
        stf_arulprakash = staff_by_name.get("Dr. Arulprakash P")

        # Fetch rooms
        rooms_res = (await db.execute(select(Room))).scalars().all()
        rooms_map = {r.room_number: r for r in rooms_res}
        r_204 = rooms_map.get("Room 204")
        r_302 = rooms_map.get("Room 302")
        r_lab2 = rooms_map.get("AI Lab 2")

        # Fetch periods
        periods_res = (await db.execute(select(Period).where(Period.is_break == False))).scalars().all()
        periods_map = {p.period_number: p for p in periods_res}

        # Build comprehensive Monday-Friday Timetable for Section A
        weekly_plan = [
            # Monday (1)
            (1, 1, "CS3301", stf_saravanan, r_204, "THEORY"),
            (1, 2, "CS3352", stf_saravanan, r_204, "THEORY"),
            (1, 4, "AD3501", stf_kumar, r_302, "THEORY"),
            (1, 5, "AD3511", stf_kumar, r_lab2, "LAB"),
            (1, 7, "CS3451", stf_arulprakash, r_204, "THEORY"),

            # Tuesday (2)
            (2, 1, "CS3351", stf_kumar, r_302, "THEORY"),
            (2, 2, "AD3501", stf_kumar, r_302, "THEORY"),
            (2, 4, "CS3301", stf_saravanan, r_204, "THEORY"),
            (2, 5, "CS3352", stf_saravanan, r_204, "THEORY"),
            (2, 7, "CS3451", stf_arulprakash, r_204, "THEORY"),

            # Wednesday (3)
            (3, 1, "CS3352", stf_saravanan, r_204, "THEORY"),
            (3, 2, "CS3351", stf_kumar, r_302, "THEORY"),
            (3, 4, "AD3501", stf_kumar, r_302, "THEORY"),
            (3, 5, "CS3451", stf_arulprakash, r_204, "THEORY"),
            (3, 7, "CS3301", stf_saravanan, r_204, "THEORY"),

            # Thursday (4)
            (4, 1, "CS3351", stf_kumar, r_302, "THEORY"),
            (4, 2, "CS3451", stf_arulprakash, r_204, "THEORY"),
            (4, 4, "AD3511", stf_kumar, r_lab2, "LAB"),
            (4, 5, "CS3301", stf_saravanan, r_204, "THEORY"),
            (4, 7, "CS3352", stf_saravanan, r_204, "THEORY"),

            # Friday (5)
            (5, 1, "AD3501", stf_kumar, r_302, "THEORY"),
            (5, 2, "CS3351", stf_kumar, r_302, "THEORY"),
            (5, 4, "CS3301", stf_saravanan, r_204, "THEORY"),
            (5, 5, "CS3352", stf_saravanan, r_204, "THEORY"),
            (5, 7, "CS3451", stf_arulprakash, r_204, "THEORY"),
        ]

        print("[SEED] Ensuring Timetable entries for Section A...")
        existing_tt = (
            await db.execute(
                select(TimetableEntry).where(TimetableEntry.section_id == sec_a.id)
            )
        ).scalars().all()

        tt_lookup = {(e.day_of_week, e.period_id): e for e in existing_tt}
        timetable_by_day = {1: [], 2: [], 3: [], 4: [], 5: []}

        for day_num, period_num, course_code, staff_obj, room_obj, l_type in weekly_plan:
            period_obj = periods_map.get(period_num)
            course_obj = courses_map.get(course_code)
            if not period_obj or not course_obj or not staff_obj:
                continue

            entry = tt_lookup.get((day_num, period_obj.id))
            if not entry:
                entry = TimetableEntry(
                    id=uuid.uuid4(),
                    section_id=sec_a.id,
                    course_id=course_obj.id,
                    staff_id=staff_obj.id,
                    room_id=room_obj.id,
                    period_id=period_obj.id,
                    day_of_week=day_num,
                    lecture_type=l_type,
                    is_active=True,
                )
                db.add(entry)
                await db.flush()
                tt_lookup[(day_num, period_obj.id)] = entry

            timetable_by_day[day_num].append((entry, course_code, staff_obj))

        await db.commit()
        print(f"[SEED] Timetable populated successfully. Days: {list(timetable_by_day.keys())}")

        # Fetch active students in Section A
        stud_stmt = select(Student).where(
            Student.section_id == sec_a.id,
            Student.is_active == True,
        ).order_by(Student.register_number)
        students = (await db.execute(stud_stmt)).scalars().all()
        print(f"[SEED] Found {len(students)} active students in Section A.")

        abishek = next((s for s in students if "24AD012" in s.register_number.upper()), None)
        if abishek:
            print(f"[SEED] Found target student: {abishek.full_name} ({abishek.register_number})")

        # Purge existing sessions for Section A entries
        sec_tt_ids = (
            await db.execute(
                select(TimetableEntry.id).where(TimetableEntry.section_id == sec_a.id)
            )
        ).scalars().all()

        if sec_tt_ids:
            old_sess_ids = (
                await db.execute(
                    select(AttendanceSession.id).where(AttendanceSession.timetable_entry_id.in_(sec_tt_ids))
                )
            ).scalars().all()

            if old_sess_ids:
                print(f"[SEED] Purging {len(old_sess_ids)} existing attendance sessions...")
                await db.execute(delete(AttendanceRecord).where(AttendanceRecord.attendance_session_id.in_(old_sess_ids)))
                await db.execute(delete(AttendanceSession).where(AttendanceSession.id.in_(old_sess_ids)))
                await db.commit()

        # Date range: 3 weeks: Sep 21, 2026 to Oct 9, 2026 (15 working days * 5 periods = 75 sessions)
        start_date = date(2026, 9, 21)
        end_date = date(2026, 10, 9)

        session_dicts = []
        record_dicts = []

        topic_idx = {c_code: 0 for c_code in TOPICS}
        random.seed(12345)

        current = start_date
        now_ts = datetime.now(timezone.utc)

        while current <= end_date:
            weekday = current.isoweekday()
            if 1 <= weekday <= 5:
                day_entries = timetable_by_day.get(weekday, [])
                for entry, c_code, staff_obj in day_entries:
                    sess_id = uuid.uuid4()
                    topics_list = TOPICS.get(c_code, ["Advanced Concepts"])
                    topic = topics_list[topic_idx[c_code] % len(topics_list)]
                    topic_idx[c_code] += 1

                    pres_count = 0
                    abs_count = 0
                    od_cnt = 0

                    for st in students:
                        rec_id = uuid.uuid4()
                        is_target = (abishek and st.id == abishek.id)
                        if is_target:
                            # Abishek: 92% Present, 5% OD, 3% Absent
                            val = random.random()
                            if val < 0.92:
                                status = "PRESENT"
                                pres_count += 1
                            elif val < 0.97:
                                status = "ON_DUTY"
                                od_cnt += 1
                            else:
                                status = "ABSENT"
                                abs_count += 1
                        else:
                            val = random.random()
                            if val < 0.88:
                                status = "PRESENT"
                                pres_count += 1
                            elif val < 0.93:
                                status = "ON_DUTY"
                                od_cnt += 1
                            else:
                                status = "ABSENT"
                                abs_count += 1

                        record_dicts.append({
                            "id": rec_id,
                            "attendance_session_id": sess_id,
                            "student_id": st.id,
                            "status": status,
                            "remarks": None,
                            "marked_at": now_ts,
                        })

                    session_dicts.append({
                        "id": sess_id,
                        "timetable_entry_id": entry.id,
                        "staff_id": staff_obj.id,
                        "date": current,
                        "conducted_hours": 1,
                        "topic_covered": topic,
                        "present_count": pres_count,
                        "absent_count": abs_count,
                        "od_count": od_cnt,
                        "total_marked": len(students),
                        "submitted_at": now_ts,
                    })

            current += timedelta(days=1)

        print(f"[SEED] Inserting {len(session_dicts)} sessions via bulk insert...")
        await db.execute(insert(AttendanceSession).values(session_dicts))

        print(f"[SEED] Inserting {len(record_dicts)} records in chunks of 500...")
        chunk_size = 500
        for i in range(0, len(record_dicts), chunk_size):
            chunk = record_dicts[i:i + chunk_size]
            await db.execute(insert(AttendanceRecord).values(chunk))

        await db.commit()
        print(f"[SUCCESS] Successfully seeded {len(session_dicts)} Attendance Sessions and {len(record_dicts)} Attendance Records!")

if __name__ == "__main__":
    asyncio.run(seed_attendance())
