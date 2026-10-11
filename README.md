# NEXUS College Management System (CMS)

A modern, full-stack College Management & Attendance System featuring a **Role-Based Modular Frontend** built with **React Native / Expo** and a robust **FastAPI backend**.

---

## 🏛️ Project Architecture

```text
CMS-REACT-NATIVE/
├── frontend/                        # Dedicated React Native / Expo application
│   ├── assets/                      # Application icons, images, branding
│   ├── src/
│   │   ├── app/                     # App initialization, routing & providers
│   │   │   ├── navigation/          # AppNavigator (Role-based screen stacks)
│   │   │   └── providers/           # AppProviders (AuthProvider wrapper)
│   │   ├── modules/                 # Role-based feature domains
│   │   │   ├── auth/                # Login, credentials & Common Campus Hub
│   │   │   ├── student/             # Student dashboard, attendance, timetable, materials, profile
│   │   │   ├── staff/               # Faculty dashboard, attendance roll call, timetable, notes, mentor
│   │   │   └── admin/               # Admin dashboard, reports, onboarding, enrollments, governance
│   │   ├── components/              # Shared reusable components (TopAppBar, BottomNavBar, etc.)
│   │   ├── services/                # API communication clients (Auth, Attendance, Timetable, etc.)
│   │   ├── constants/               # Colors and typography design tokens
│   │   └── theme/                   # Material Design 3 theme system
│   ├── App.js                       # Frontend root component
│   ├── index.js                     # Expo root registry
│   ├── app.json                     # Expo configuration
│   └── package.json                 # Frontend dependencies & scripts
├── backend/                         # FastAPI / Python backend
│   ├── app/                         # Modular routers, schemas, services, and models
│   ├── alembic/                     # Database migrations
│   └── tests/                       # Pytest test suite
├── docs/                            # Project specifications & architecture docs
│   ├── API_SPECIFICATION.md
│   ├── DATABASE_DESIGN.md
│   ├── AUTHORIZATION_MATRIX.md
│   └── ROLE_BASED_ARCHITECTURE.md
├── screens/                         # Backward-compatibility re-exports
├── components/                      # Backward-compatibility re-exports
└── package.json                     # Root delegation scripts
```

---

## ✨ Features by Role

### 🎓 Student Module (`frontend/src/modules/student/`)
- **Dashboard**: Live attendance percentages, upcoming timetable classes, announcements.
- **Attendance**: Subject-by-subject percentage dials, detailed session breakdown, calendar logs.
- **Timetable**: Day-wise weekly lecture and lab timetable.
- **Materials**: Download course handouts, lecture slides, and syllabus documents.
- **Profile**: Student bio, roll number, department, mentor details, and contact updater.

### 👨‍🏫 Staff Module (`frontend/src/modules/staff/`)
- **Dashboard**: Teaching schedule, pending attendance alerts, quick actions.
- **Attendance**: Interactive roll call marking (Present/Absent toggles) and attendance revision review.
- **Timetable**: Assigned teaching slots, room locations, and lab allocations.
- **Materials**: Upload lecture notes, study materials, and reference guides.
- **Profile**: Faculty bio, designation, department info, and profile editor.
- **Mentor/Proctor**: Mentee roster and student proctor allocation management.

### 🛡️ Admin Module (`frontend/src/modules/admin/`)
- **Dashboard**: Institutional analytics, student/staff metrics, operational controls.
- **Attendance Oversight**: Institutional attendance reporting and audit logs.
- **Timetable Management**: Master timetable scheduler and slot conflict resolver.
- **Faculty Onboarding**: Faculty registration and department onboarding.
- **Student Admissions**: Student enrollment, department assignment, and registration summary.
- **Governance Profile**: System administrator security and institutional settings.

### 🔐 Auth Module & Campus Hub (`frontend/src/modules/auth/`)
- **Login Portal**: Centralized portal supporting role-specific login workflows.
- **Common Campus Hub**: Official circulars, academic calendar, facility info, and Q-Fix redressal.
- **AuthContext**: Persistent session state using AsyncStorage and JWT authorization.

---

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- npm or yarn
- Expo CLI (`npx expo`)

### 1. Frontend Setup
```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies (if needed)
npm install

# Start the Expo development server
npm start

# Or run directly on specific platforms:
npm run web       # Run in web browser
npm run android   # Run on Android device/emulator
npm run ios       # Run on iOS simulator
```

*Note: You can also start the frontend directly from the root directory:*
```bash
npm start
# or
npm run frontend:start
```

### 2. Backend Setup
```bash
# Navigate to backend
cd backend

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Unix/macOS:
source .venv/bin/activate

# Run database migrations
alembic upgrade head

# Start FastAPI server
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🧪 Testing & Verification

- **Backend Tests**:
  ```bash
  backend\.venv\Scripts\python.exe -m pytest backend/tests
  ```
- **Frontend Config & Imports**:
  ```bash
  cd frontend && npx expo config --type public
  ```

---

## 📱 Tech Stack
- **Frontend:** React Native (v0.86), Expo SDK (~57), React Navigation (v7), Expo Blur & Linear Gradient, Vector Icons
- **Backend:** FastAPI, Python 3.11+, SQLAlchemy 2.0, Alembic, Pydantic v2
- **Database:** PostgreSQL / SQLite
