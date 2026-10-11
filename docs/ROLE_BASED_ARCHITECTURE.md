# CMS Role-Based Frontend Architecture

## 1. Overview
The College Management System (CMS) frontend is structured as a **Role-Based Modular Application** inside `frontend/`. 

This architecture aligns screens, features, and workflows directly to user roles (`student`, `staff`, `admin`), while maintaining shared modules for authentication, UI components, API services, theme tokens, and application routing.

## 2. Directory Hierarchy

```text
frontend/
├── assets/                          # Static assets, branding, and images
│   ├── icon.png
│   ├── adaptive-icon.png
│   ├── splash-icon.png
│   └── time table 3 yr.jpeg
├── src/
│   ├── app/                         # Application bootstrapping and routing
│   │   ├── navigation/              # React Navigation configuration
│   │   │   ├── AppNavigator.js      # Central stack navigator referencing role modules
│   │   │   └── index.js
│   │   ├── providers/               # Global context providers
│   │   │   ├── AppProviders.js      # AuthProvider & theme provider wrapper
│   │   │   └── index.js
│   │   └── index.js
│   ├── modules/                     # Role-based feature domains
│   │   ├── auth/                    # Shared authentication & campus hub
│   │   │   ├── screens/             # LoginPage, StudentLogin, StaffLogin, AdminLogin, CommonPortal
│   │   │   ├── context/             # AuthContext (token, role, session persistence)
│   │   │   └── index.js
│   │   ├── student/                 # Student domain
│   │   │   ├── dashboard/           # StudentDashboard
│   │   │   ├── attendance/          # AttendanceHistory, StudentAttendanceDetail
│   │   │   ├── timetable/           # StudentTimetable
│   │   │   ├── materials/           # StudyMaterials
│   │   │   ├── profile/             # StudentProfile, StudentEditProfile
│   │   │   └── index.js             # Student module barrel
│   │   ├── staff/                   # Faculty domain
│   │   │   ├── dashboard/           # StaffDashboard
│   │   │   ├── attendance/          # MarkAttendance, AttendanceReview
│   │   │   ├── timetable/           # StaffTimetable
│   │   │   ├── materials/           # StaffNotes
│   │   │   ├── profile/             # StaffProfile, StaffEditProfile
│   │   │   ├── mentor-proctor/      # MentorProctorAllocationScreen (shared)
│   │   │   └── index.js             # Staff module barrel
│   │   └── admin/                   # Administrative domain
│   │       ├── dashboard/           # AdminDashboard
│   │       ├── attendance/          # ReportManagement
│   │       ├── timetable/           # AdminTimetable
│   │       ├── faculty/             # AdminStaffOnboardingScreen, MentorProctorAllocationScreen
│   │       ├── students/            # EnrollStudent, EnrollmentSuccess
│   │       ├── profile/             # AdminProfile, AdminEditProfile
│   │       └── index.js             # Admin module barrel
│   ├── components/                  # Shared UI components
│   │   ├── common/                  # TopAppBar, BottomNavBar, StudentBottomNav, NavigationDrawer
│   │   ├── forms/                   # Form controls and validation elements
│   │   ├── layout/                  # Screen scaffolds and containers
│   │   └── index.js
│   ├── services/                    # Shared API integration services
│   │   ├── api/                     # Axios/Fetch clients: auth, attendance, timetable, profiles, materials
│   │   └── index.js
│   ├── constants/                   # Application constants, design tokens
│   ├── theme/                       # MD3 design palette & typography
│   ├── context/                     # Global context proxies
│   ├── hooks/                       # Custom hooks
│   ├── utils/                       # Helper functions
│   └── index.js                     # Root source barrel
├── App.js                           # Frontend application entry point
├── index.js                         # Expo root component registry
├── app.json                         # Expo configuration
├── package.json                     # Frontend dependencies and scripts
└── package-lock.json
```

## 3. Role Responsibilities

### Student Module (`frontend/src/modules/student/`)
- **Dashboard**: Academic progress, quick attendance stats, class alerts.
- **Attendance**: View attendance percentage per subject, monthly breakdown, session logs.
- **Timetable**: Day-wise weekly lecture and lab timetable.
- **Materials**: Subject notes, PDFs, assignments, and study materials.
- **Profile**: Student bio, roll number, department, mentor details, profile edit.

### Staff Module (`frontend/src/modules/staff/`)
- **Dashboard**: Teaching schedule, pending attendance alerts, quick actions.
- **Attendance**: Mark period attendance with present/absent toggles, review and edit history.
- **Timetable**: Assigned teaching slots, room locations, lab schedules.
- **Materials**: Upload notes, share syllabus files and lecture handouts.
- **Profile**: Faculty bio, designation, department info, profile edit.
- **Mentor/Proctor**: Assigned mentee roster, academic tracking.

### Admin Module (`frontend/src/modules/admin/`)
- **Dashboard**: Institution KPIs, student/staff metrics, operational controls.
- **Attendance**: Institutional attendance report generation and department oversight.
- **Timetable**: Master timetable editor, room allocation, instructor mapping.
- **Faculty**: Staff onboarding, mentor/proctor allocations.
- **Students**: Student registration, admission enrollment, confirmation receipt.
- **Profile**: Administrative credentials and security settings.

### Auth Module (`frontend/src/modules/auth/`)
- **Login Portal**: Common entry point with role selectors (`Student`, `Staff`, `Admin`).
- **Role Credentials**: Dedicated secure login forms for each role.
- **Campus Hub (CommonPortal)**: Public campus news, guest events, announcement portal.
- **AuthContext**: Session persistence via AsyncStorage, role resolution, JWT headers.

## 4. How to Run

### Frontend
```bash
# Navigate to frontend and start with Expo
cd frontend
npm start

# Or run on specific platforms
npm run android
npm run ios
npm run web
```

Alternatively, from the repository root:
```bash
npm start
# or
npm run frontend:start
```

### Backend
```bash
# Activate virtual environment
backend\.venv\Scripts\activate

# Run FastAPI server
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```
