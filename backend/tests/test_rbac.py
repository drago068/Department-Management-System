import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_student_cannot_access_attendance_submit(client: AsyncClient, student_token: str):
    response = await client.post(
        "/api/v1/attendance/submit",
        json={"timetable_entry_id": "00000000-0000-0000-0000-000000000000", "date": "2026-10-05", "records": []},
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert response.status_code == 403
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "FORBIDDEN"


@pytest.mark.asyncio
async def test_student_cannot_access_timetable_entries_create(client: AsyncClient, student_token: str):
    response = await client.post(
        "/api/v1/timetable/entries",
        json={
            "section_id": "00000000-0000-0000-0000-000000000000",
            "course_id": "00000000-0000-0000-0000-000000000000",
            "staff_id": "00000000-0000-0000-0000-000000000000",
            "room_id": "00000000-0000-0000-0000-000000000000",
            "period_id": "00000000-0000-0000-0000-000000000000",
            "day_of_week": 1,
        },
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"


@pytest.mark.asyncio
async def test_staff_cannot_access_defaulters_report(client: AsyncClient, staff_token: str):
    response = await client.get(
        "/api/v1/reports/attendance/defaulters",
        headers={"Authorization": f"Bearer {staff_token}"},
    )
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"


@pytest.mark.asyncio
async def test_public_can_access_showcase_unauthenticated(client: AsyncClient):
    response = await client.get("/api/v1/public/department/showcase")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "department" in data["data"]
    assert "faculty" in data["data"]
    assert "laboratories" in data["data"]


@pytest.mark.asyncio
async def test_public_can_access_announcements_unauthenticated(client: AsyncClient):
    response = await client.get("/api/v1/announcements")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert len(data["data"]) >= 3
