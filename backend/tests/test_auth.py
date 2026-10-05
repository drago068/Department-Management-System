import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_student_login_success(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        json={"identifier": "CS2024-001", "password": "Password123!", "role": "STUDENT"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]
    assert data["data"]["user"]["role"] == "STUDENT"
    assert data["data"]["user"]["identifier"] == "CS2024-001"
    assert data["data"]["user"]["profile"]["full_name"] == "Arjun Patel"


@pytest.mark.asyncio
async def test_faculty_login_success(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        json={"identifier": "FAC-2024-001", "password": "Password123!", "role": "STAFF"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["user"]["role"] == "STAFF"
    assert data["data"]["user"]["profile"]["full_name"] == "Dr. Kumar"


@pytest.mark.asyncio
async def test_admin_login_success(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        json={"identifier": "admin", "password": "AdminPassword123!", "role": "ADMIN"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["user"]["role"] == "ADMIN"
    assert data["data"]["user"]["profile"]["full_name"] == "Dr. V. Rajesh"


@pytest.mark.asyncio
async def test_invalid_password_fails(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        json={"identifier": "CS2024-001", "password": "WrongPassword!", "role": "STUDENT"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "UNAUTHORIZED"


@pytest.mark.asyncio
async def test_token_refresh_flow(client: AsyncClient):
    # 1. Login
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"identifier": "CS2024-001", "password": "Password123!"},
    )
    refresh_token = login_res.json()["data"]["refresh_token"]

    # 2. Refresh
    refresh_res = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert refresh_res.status_code == 200
    new_data = refresh_res.json()["data"]
    assert "access_token" in new_data
    assert "refresh_token" in new_data
    assert new_data["refresh_token"] != refresh_token  # Rotated!
