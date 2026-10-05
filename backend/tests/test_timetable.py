import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_student_timetable_retrieval(client: AsyncClient, student_token: str):
    response = await client.get(
        "/api/v1/timetable/student?day_of_week=1",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["day_name"] == "Monday"
    schedule = data["data"]["schedule"]
    assert len(schedule) > 0
    # First slot should be DSA
    dsa_slot = next((s for s in schedule if s.get("course_code") == "CS3301"), None)
    assert dsa_slot is not None
    assert dsa_slot["room"] == "Room 204"
    assert dsa_slot["status"] in ["COMPLETED", "IN_PROGRESS", "UPCOMING"]


@pytest.mark.asyncio
async def test_staff_timetable_retrieval(client: AsyncClient, staff_token: str):
    response = await client.get(
        "/api/v1/timetable/staff?day_of_week=1",
        headers={"Authorization": f"Bearer {staff_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    schedule = data["data"]["schedule"]
    dl_slot = next((s for s in schedule if s.get("course_code") == "AD3501"), None)
    assert dl_slot is not None
    assert dl_slot["attendance_status"] in ["MARKED", "PENDING"]


@pytest.mark.asyncio
async def test_timetable_triple_conflict_detection(client: AsyncClient, admin_token: str):
    # Fetch existing IDs from academic endpoints
    depts_res = await client.get("/api/v1/academic/departments")
    dept_id = depts_res.json()["data"][0]["id"]

    courses_res = await client.get(f"/api/v1/academic/courses?department_id={dept_id}")
    course_id = courses_res.json()["data"][0]["id"]

    rooms_res = await client.get("/api/v1/academic/rooms")
    room_id = rooms_res.json()["data"][0]["id"]  # Room 204

    periods_res = await client.get("/api/v1/academic/periods")
    period_id = periods_res.json()["data"][0]["id"]  # Period 1

    # Get Staff and Section IDs from DB
    from app.core.database import async_session_maker
    from app.models.organization import Section
    from app.models.profiles import Staff
    from sqlalchemy import select

    async with async_session_maker() as db:
        sec = (await db.execute(select(Section).limit(1))).scalar_one()
        stf = (await db.execute(select(Staff).limit(1))).scalar_one()
        section_id = str(sec.id)
        staff_id = str(stf.id)

    # Attempt to schedule in an already occupied room (Room 204, Monday, Period 1)
    conflict_payload = {
        "section_id": section_id,
        "course_id": course_id,
        "staff_id": staff_id,
        "room_id": room_id,
        "period_id": period_id,
        "day_of_week": 1,
        "lecture_type": "THEORY",
    }
    response = await client.post(
        "/api/v1/timetable/entries",
        json=conflict_payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    # Must be rejected with 409 Conflict
    assert response.status_code == 409
    data = response.json()
    assert data["success"] is False
    assert "CONFLICT" in data["error"]["code"] or "ROOM" in data["error"]["code"] or "SECTION" in data["error"]["code"]
