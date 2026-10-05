# CMS REST API Specification (`/api/v1`)

---

## 1. Global API Standards & Envelopes

### 1.1. Base URL & Versioning
All backend endpoints are prefixed with `/api/v1/`.

### 1.2. Standard Success Response Envelope
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully"
}
```

### 1.3. Standard Error Response Envelope
```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested timetable entry does not exist.",
    "details": null
  }
}
```

### 1.4. Standard Pagination Query Parameters & Envelope
* `page` (integer, default `1`, min `1`)
* `limit` (integer, default `20`, max `100`)

```json
{
  "success": true,
  "data": {
    "items": [ ... ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total_items": 58,
      "total_pages": 3,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

---

## 2. Authentication & Authorization Endpoints (`/api/v1/auth`)

### 2.1. Unified Multi-Role Login
* **Endpoint**: `POST /api/v1/auth/login`
* **Access**: Public
* **Description**: Authenticates Student (Roll No / Reg No), Faculty (Faculty ID), or Admin (Username/Admin ID).
* **Request Body**:
```json
{
  "identifier": "CS2024-001",
  "password": "SecurePassword123!",
  "role": "STUDENT"
}
```
* **Success Response (`200 OK`)**:
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOi...",
    "refresh_token": "8f4a1c...",
    "token_type": "Bearer",
    "expires_in": 3600,
    "user": {
      "id": "c1f7b0e2-...",
      "identifier": "CS2024-001",
      "role": "STUDENT",
      "profile": {
        "full_name": "Arjun Patel",
        "avatar_url": "https://..."
      }
    }
  },
  "message": "Authentication successful"
}
```
* **Error Codes**: `INVALID_CREDENTIALS` (401), `ACCOUNT_LOCKED` (403), `VALIDATION_ERROR` (422).

### 2.2. Refresh Access Token
* **Endpoint**: `POST /api/v1/auth/refresh`
* **Access**: Public (Requires valid refresh token)
* **Request Body**:
```json
{
  "refresh_token": "8f4a1c..."
}
```
* **Success Response (`200 OK`)**: Returns new `access_token` and rotated `refresh_token`.

### 2.3. Logout / Token Revocation
* **Endpoint**: `POST /api/v1/auth/logout`
* **Access**: Authenticated (`STUDENT`, `STAFF`, `ADMIN`)
* **Success Response (`200 OK`)**: Revokes active refresh token.

---

## 3. Profile Management Endpoints (`/api/v1/profiles`)

### 3.1. Get Current User Profile
* **Endpoint**: `GET /api/v1/profiles/me`
* **Access**: Authenticated (`STUDENT`, `STAFF`, `ADMIN`)
* **Response for Student**:
```json
{
  "success": true,
  "data": {
    "role": "STUDENT",
    "id": "s8d9f-...",
    "register_number": "714022AD001",
    "roll_number": "CS2024-001",
    "full_name": "Arjun Patel",
    "department": { "id": "...", "code": "AIDS", "name": "Artificial Intelligence & Data Science" },
    "batch": "2022-2026",
    "section": "A",
    "semester": 3,
    "cgpa": 8.75,
    "phone": "+91 9876543210",
    "email": "arjun.p@suguna.edu",
    "parent_name": "Rajesh Patel",
    "parent_phone": "+91 9876500000",
    "blood_group": "O+",
    "address": "142, North Street, Coimbatore",
    "avatar_url": "https://..."
  }
}
```

### 3.2. Update Own Profile (Self-Service)
* **Endpoint**: `PUT /api/v1/profiles/me`
* **Access**: Authenticated
* **Request Body (Protected fields are ignored/forbidden)**:
```json
{
  "phone": "+91 9876543211",
  "email": "arjun.new@suguna.edu",
  "address": "144, North Street, Coimbatore",
  "avatar_url": "https://..."
}
```

---

## 4. Timetable System Endpoints (`/api/v1/timetable`)

### 4.1. Get Student Timetable
* **Endpoint**: `GET /api/v1/timetable/student`
* **Access**: `STUDENT`
* **Query Params**: `day_of_week` (optional, 1=Monday to 6=Saturday)
* **Success Response (`200 OK`)**:
```json
{
  "success": true,
  "data": {
    "day_of_week": 1,
    "day_name": "Monday",
    "schedule": [
      {
        "id": "t1-...",
        "period_number": 1,
        "period_name": "P1",
        "start_time": "08:45",
        "end_time": "09:35",
        "is_break": false,
        "course_code": "CS3301",
        "course_name": "Data Structures",
        "short_name": "DSA",
        "lecture_type": "THEORY",
        "room": "Room 204",
        "faculty_name": "Dr. S. Karthikeyan",
        "status": "COMPLETED"
      },
      {
        "id": "t2-...",
        "period_number": 2,
        "period_name": "P2",
        "start_time": "09:35",
        "end_time": "10:25",
        "is_break": false,
        "course_code": "CS3352",
        "course_name": "Database Management",
        "short_name": "DBMS",
        "lecture_type": "THEORY",
        "room": "Room 204",
        "faculty_name": "Prof. Saravanan M",
        "status": "COMPLETED"
      },
      {
        "id": "t-break-...",
        "is_break": true,
        "title": "Morning Tea Break & Refreshment",
        "start_time": "10:25",
        "end_time": "10:40",
        "status": "COMPLETED"
      },
      {
        "id": "t3-...",
        "period_number": 3,
        "period_name": "P3",
        "start_time": "10:40",
        "end_time": "11:30",
        "is_break": false,
        "course_code": "AD3501",
        "course_name": "Deep Learning",
        "short_name": "DL",
        "lecture_type": "THEORY",
        "room": "Room 302 (Turing Hall)",
        "faculty_name": "Dr. Kumar",
        "status": "IN_PROGRESS"
      }
    ]
  }
}
```

### 4.2. Get Staff Timetable
* **Endpoint**: `GET /api/v1/timetable/staff`
* **Access**: `STAFF`
* **Query Params**: `day_of_week` (optional)
* **Success Response (`200 OK`)**: Returns teaching workload, assigned sections, venue, and `attendance_status` (`MARKED` or `PENDING` for today's date).

### 4.3. Get Department Master Timetable (Admin)
* **Endpoint**: `GET /api/v1/timetable/admin`
* **Access**: `ADMIN`
* **Query Params**: `section_id` (required), `day_of_week` (optional)

### 4.4. Create / Update Timetable Entry
* **Endpoint**: `POST /api/v1/timetable/entries` | `PUT /api/v1/timetable/entries/{id}`
* **Access**: `ADMIN`
* **Conflict Checking**: Automatically runs validator against room availability, faculty overlap, and section double-booking.

---

## 5. Attendance System Endpoints (`/api/v1/attendance`)

### 5.1. Get Eligible Students for Attendance Marking
* **Endpoint**: `GET /api/v1/attendance/session/students`
* **Access**: `STAFF`, `ADMIN`
* **Query Params**: `timetable_entry_id` (required), `date` (required, `YYYY-MM-DD`)
* **Response**:
```json
{
  "success": true,
  "data": {
    "timetable_info": {
      "course_name": "Data Structures",
      "course_code": "CS3301",
      "section_name": "III AI & DS - A",
      "period": "Period 1",
      "room": "Room 204",
      "date": "2024-09-06"
    },
    "already_submitted": false,
    "students": [
      { "id": "st-001", "roll_number": "CS2024-001", "name": "Arjun Patel", "default_status": "PRESENT" },
      { "id": "st-002", "roll_number": "CS2024-002", "name": "Priya Sharma", "default_status": "PRESENT" }
    ]
  }
}
```

### 5.2. Submit Class Attendance
* **Endpoint**: `POST /api/v1/attendance/submit`
* **Access**: `STAFF`, `ADMIN`
* **Request Body**:
```json
{
  "timetable_entry_id": "t1-001-...",
  "date": "2024-09-06",
  "records": [
    { "student_id": "st-001", "status": "PRESENT" },
    { "student_id": "st-002", "status": "PRESENT" },
    { "student_id": "st-003", "status": "ABSENT" },
    { "student_id": "st-006", "status": "ON_DUTY" }
  ]
}
```
* **Success Response (`201 Created`)**:
```json
{
  "success": true,
  "data": {
    "session_id": "as-771-...",
    "total_marked": 60,
    "present_count": 55,
    "absent_count": 4,
    "od_count": 1,
    "submitted_at": "2024-09-06T09:45:00Z"
  },
  "message": "Attendance marked successfully"
}
```
* **Error Codes**: `ATTENDANCE_ALREADY_SUBMITTED` (409), `UNAUTHORIZED_STAFF_ASSIGNMENT` (403), `INVALID_STUDENT_LIST` (422).

### 5.3. Get Student Attendance Summary & Subject Breakdown
* **Endpoint**: `GET /api/v1/attendance/student/summary`
* **Access**: `STUDENT` (or `ADMIN`/`STAFF` passing `?student_id=...`)
* **Success Response (`200 OK`)**:
```json
{
  "success": true,
  "data": {
    "overall_percentage": 88.5,
    "total_attended_hours": 177,
    "total_conducted_hours": 200,
    "benchmark_percentage": 75.0,
    "status": "SAFE",
    "subjects": [
      {
        "course_code": "CS3351",
        "course_name": "Machine Learning",
        "staff_name": "Dr. S. Karthikeyan",
        "attended_hours": 37,
        "total_hours": 40,
        "percentage": 92.5,
        "status": "EXCELLENT",
        "max_absences_allowed": 3
      },
      {
        "course_code": "AD3401",
        "course_name": "Deep Learning",
        "staff_name": "Prof. R. Menaka",
        "attended_hours": 34,
        "total_hours": 40,
        "percentage": 85.0,
        "status": "GOOD",
        "max_absences_allowed": 1
      }
    ]
  }
}
```

### 5.4. Query Attendance History (Admin Audit)
* **Endpoint**: `GET /api/v1/attendance/history`
* **Access**: `ADMIN`
* **Query Params**: `date`, `section_id`, `course_id`, `page`, `limit`

---

## 6. Study Materials Endpoints (`/api/v1/materials`)

### 6.1. List / Search Study Materials
* **Endpoint**: `GET /api/v1/materials`
* **Access**: `STUDENT`, `STAFF`, `ADMIN`
* **Query Params**: `course_id`, `material_type`, `unit`, `search`, `page`, `limit`
* **Success Response (`200 OK`)**:
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "mat-001",
        "course_code": "CS3351",
        "course_name": "Machine Learning",
        "unit": "Unit 1",
        "title": "Introduction to Machine Learning & Supervised Algorithms",
        "instructor": "Dr. Sarah Williams",
        "material_type": "LECTURE_NOTE",
        "file_format": "PDF",
        "file_size": "4.2 MB",
        "reads_count": 1420,
        "downloads_count": 520,
        "download_url": "/api/v1/materials/mat-001/download",
        "created_at": "2024-08-20T10:00:00Z"
      }
    ]
  }
}
```

### 6.2. Upload Study Material
* **Endpoint**: `POST /api/v1/materials/upload`
* **Access**: `STAFF`, `ADMIN`
* **Content-Type**: `multipart/form-data`
* **Form Fields**: `course_id`, `title`, `unit`, `topic`, `material_type`, `file`

### 6.3. Download Study Material (Increments Counter)
* **Endpoint**: `GET /api/v1/materials/{id}/download`
* **Access**: Authenticated

### 6.4. Delete Study Material
* **Endpoint**: `DELETE /api/v1/materials/{id}`
* **Access**: `STAFF` (only if own upload), `ADMIN`

---

## 7. Reports & Analytics Endpoints (`/api/v1/reports`)

### 7.1. Low Attendance Defaulters Report
* **Endpoint**: `GET /api/v1/reports/attendance/defaulters`
* **Access**: `ADMIN`
* **Query Params**: `threshold` (default `75.0`), `section_id`, `semester_id`

### 7.2. Faculty Teaching Load & Workload Report
* **Endpoint**: `GET /api/v1/reports/faculty/workload`
* **Access**: `ADMIN`

### 7.3. Department Performance Summary
* **Endpoint**: `GET /api/v1/reports/department/summary`
* **Access**: `ADMIN`

---

## 8. Public Common Campus Portal (`/api/v1/public`)

### 8.1. Get Department Showcase Overview
* **Endpoint**: `GET /api/v1/public/department/showcase`
* **Access**: Public
* **Response**: Vision, stats, curriculum roadmap, laboratories, and faculty directory.

---

## 9. Campus Circulars & Announcements Endpoints (`/api/v1/announcements`)

### 9.1. List Announcements & Circulars
* **Endpoint**: `GET /api/v1/announcements`
* **Access**: Public / Authenticated (Tailored to role when authenticated)
* **Query Params**: `category` (optional, e.g. `coe`, `placement`, `academic`, `events`), `search` (optional), `page`, `limit`
* **Success Response (`200 OK`)**:
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "ann-001",
        "category": "coe",
        "reference_number": "CIR/SCE/2024-25/089",
        "title": "Revaluation & Paper Viewing Window - June/July Session",
        "heading": "Revaluation & Answer Script Verification Window for UG Sem II & IV",
        "department": "Controller of Examinations",
        "date": "18 Oct 2024",
        "tag": "Autonomous",
        "badge": "CoE",
        "badge_type": "blue",
        "content": "Candidates interested in script xerox copies and subsequent revaluation are requested to register through their student portal before October 26, 2024. Nominal fee of ₹400 per course applies.",
        "footer_icon": "verified",
        "footer": "Signed by Dr. K. Ramanathan",
        "publish_date": "2024-10-18",
        "expires_at": "2024-10-26T23:59:59Z"
      }
    ],
    "pagination": { "page": 1, "limit": 20, "total_items": 1, "total_pages": 1, "has_next": false, "has_prev": false }
  },
  "message": "Announcements retrieved successfully"
}
```

### 9.2. Create Campus Announcement (Admin / HOD)
* **Endpoint**: `POST /api/v1/announcements`
* **Access**: `ADMIN`
* **Request Body**:
```json
{
  "title": "Internal Assessment II Schedule",
  "heading": "Schedule for CIA-II Examinations",
  "content": "Assessments will commence from Nov 3rd for all UG batches.",
  "category": "academic",
  "target_role": "ALL",
  "reference_number": "ACAD/REG/2024/119",
  "tag": "Dean Academics",
  "badge": "ACD",
  "publish_date": "2024-10-20",
  "expires_at": "2024-11-10T18:00:00Z",
  "target_recipients": {
    "department_ids": [],
    "batch_ids": [],
    "section_ids": []
  }
}
```
* **Success Response (`201 Created`)**

### 9.3. Delete / Expire Announcement
* **Endpoint**: `DELETE /api/v1/announcements/{id}`
* **Access**: `ADMIN`
* **Success Response (`200 OK`)**
