import os
import sys
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# Prepend backend to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import engine
from app.main import app


@pytest_asyncio.fixture(autouse=True)
async def cleanup_db():
    yield
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def student_token(client: AsyncClient) -> str:
    res = await client.post(
        "/api/v1/auth/login",
        json={"identifier": "24AD012", "password": "abi012", "role": "STUDENT"},
    )
    assert res.status_code == 200
    return res.json()["data"]["access_token"]


@pytest_asyncio.fixture
async def staff_token(client: AsyncClient) -> str:
    res = await client.post(
        "/api/v1/auth/login",
        json={"identifier": "FAC-2024-001", "password": "Password123!", "role": "STAFF"},
    )
    assert res.status_code == 200
    return res.json()["data"]["access_token"]


@pytest_asyncio.fixture
async def admin_token(client: AsyncClient) -> str:
    res = await client.post(
        "/api/v1/auth/login",
        json={"identifier": "admin", "password": "AdminPassword123!", "role": "ADMIN"},
    )
    assert res.status_code == 200
    return res.json()["data"]["access_token"]
