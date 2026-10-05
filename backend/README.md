# College Management System (CMS) — Production Backend

A high-performance, asynchronous REST API built with **FastAPI**, **SQLAlchemy 2.0 (Async)**, **Alembic**, and **Pydantic V2**, architected around the Nexus CMS React Native frontend.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
* Python 3.10+ (or Python 3.11/3.12 recommended)
* [uv](https://docs.astral.sh/uv/) (recommended for lightning-fast package management) or standard `pip`

### 2. Virtual Environment & Dependencies
```bash
# If using uv (fastest):
uv venv backend/.venv
uv pip install -r backend/requirements.txt --python backend/.venv/Scripts/python.exe

# Or if using standard python venv:
python -m venv backend/.venv
backend\.venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 3. Database Migration & Seeding
The backend is pre-configured with SQLite (`sqlite+aiosqlite:///./cms.db`) for immediate out-of-the-box local development, and is 100% compatible with PostgreSQL / Supabase for production.

```bash
# Apply Alembic Migrations
backend\.venv\Scripts\alembic.exe -c backend\alembic.ini upgrade head

# Seed Demo Data (Students, Faculty, Timetable, Attendance, Materials, Circulars)
backend\.venv\Scripts\python.exe backend\scripts\seed_demo_data.py
```

### 4. Running the Development Server
```bash
backend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --reload --port 8000
```
* **Interactive OpenAPI Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
* **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

## 🔑 Demo Credentials

| Role | Portal / Screen | Identifier / Login ID | Password | Access Capabilities |
| :--- | :--- | :--- | :--- | :--- |
| **Student** | `StudentLogin.js` | `CS2024-001` | `Password123!` | View Timetable, View 75% Attendance Breakdown, Download Materials, View Circulars |
| **Faculty** | `StaffLogin.js` | `FAC-2024-001` | `Password123!` | View Teaching Timetable, Mark Class Attendance, Upload Study Materials |
| **Admin** | `AdminLogin.js` | `admin` | `AdminPassword123!` | Department KPI Analytics, Conflict-Free Timetable Scheduling, Defaulters Report |

---

## 🧪 Running the Automated Test Suite

```bash
backend\.venv\Scripts\pytest.exe backend\tests -v
```

Tests cover:
* Multi-role authentication & token rotation (`test_auth.py`)
* Timetable slot querying & triple conflict prevention (`test_timetable.py`)
* Attendance roster & 75% percentage calculator (`test_attendance.py`)
* Server-side RBAC role denial checks (`test_rbac.py`)
