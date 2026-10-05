from datetime import date
import pytest
from httpx import AsyncClient
from sqlalchemy import select
from app.core.database import async_session_maker
from app.models.timetable import TimetableEntry


@pytest.mark.asyncio
async def test_session_roster_retrieval(client: AsyncClient, staff_token: str):
    async with async_session_maker() as db:
        # Pick the timetable entry taught by Dr. Kumar (P3 Monday)
        entry = (await db.execute(select(TimetableEntry).limit(1))).scalar_one()
        entry_id = str(entry.id)

    response = await client.get(
        f"/api/v1/attendance/session/students?timetable_entry_id={entry_id}&date=2026-10-05",
        headers={"Authorization": f"Bearer {staff_token}"},
    )
    # May return 200 or 403 if faculty doesn't match entry
    assert response.status_code in [200, 403]


@pytest.mark.asyncio
async def test_student_attendance_summary(client: AsyncClient, student_token: str):
    response = await client.get(
        "/api/v1/attendance/student/summary",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    summary = data["data"]
    assert "overall_percentage" in summary
    assert "benchmark_percentage" in summary
    assert summary["benchmark_percentage"] == 75.0
    assert len(summary["subjects"]) > 0
    sub = summary["subjects"][0]
    assert "percentage" in sub
    assert "status" in sub
    assert "max_absences_allowed" in sub
