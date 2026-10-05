# CMS Role-Based Access Control (RBAC) & Authorization Matrix

---

## 1. User Roles & Identity Hierarchy
The CMS enforces 3 distinct roles verified server-side through JWT claims (`role`):
1. `STUDENT`: Enrolled student belonging to a specific batch and section.
2. `STAFF`: Teaching faculty member assigned to specific courses and sections.
3. `ADMIN`: Department Head (HOD) or Academic Administrator with full departmental governance.

---

## 2. Comprehensive Resource Authorization Matrix

| Resource / Action | Public / Unauth | STUDENT | STAFF / FACULTY | ADMIN / HOD | Enforcement Rule & Constraints |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Authentication & Tokens** | | | | | |
| `POST /auth/login` | ✅ | ✅ | ✅ | ✅ | Public login gateway with identifier + role check. |
| `POST /auth/refresh` | ✅ | ✅ | ✅ | ✅ | Requires valid unexpired Refresh Token. |
| `POST /auth/logout` | ❌ | ✅ | ✅ | ✅ | Revokes active user session token. |
| **Public Showcase** | | | | | |
| `GET /public/department/showcase` | ✅ | ✅ | ✅ | ✅ | Read-only department showcase. |
| **Profile Management** | | | | | |
| `GET /profiles/me` | ❌ | ✅ | ✅ | ✅ | Returns authenticated user's own profile. |
| `PUT /profiles/me` | ❌ | ✅ (Self) | ✅ (Self) | ✅ (Self) | Only editable non-protected fields (Phone, Email, Bio, Address). |
| `GET /profiles/student/{id}` | ❌ | ❌ | ✅ (Assigned) | ✅ (Full) | Staff can only view students in their assigned sections. |
| `GET /profiles/staff/{id}` | ❌ | ✅ (Directory) | ✅ | ✅ | Read-only directory view for students/peers. |
| `PUT /admin/users/{id}/role` | ❌ | ❌ | ❌ | ✅ (Admin only) | Super Admin/HOD permission only. |
| **Timetable System** | | | | | |
| `GET /timetable/student` | ❌ | ✅ (Own Section) | ❌ | ✅ | Student gets schedule for their enrolled section. |
| `GET /timetable/staff` | ❌ | ❌ | ✅ (Own Schedule) | ✅ | Staff gets their teaching periods + attendance status. |
| `GET /timetable/admin` | ❌ | ❌ | ❌ | ✅ | Master department grid by section. |
| `POST /timetable/entries` | ❌ | ❌ | ❌ | ✅ | Create timetable slots with automated conflict detection. |
| `PUT/DELETE /timetable/entries/{id}`| ❌ | ❌ | ❌ | ✅ | Edit/delete timetable slots. |
| **Attendance Management** | | | | | |
| `GET /attendance/session/students` | ❌ | ❌ | ✅ (Assigned) | ✅ | Staff can only load students for their assigned classes. |
| `POST /attendance/submit` | ❌ | ❌ | ✅ (Assigned) | ✅ | Staff can only submit attendance for their assigned timetable slots. |
| `GET /attendance/student/summary` | ❌ | ✅ (Self) | ✅ (Assigned) | ✅ (Full) | Student gets own attendance metrics; staff gets for their class. |
| `GET /attendance/history` | ❌ | ❌ | ❌ | ✅ | Full historical audit records. |
| `PUT /attendance/records/{id}` | ❌ | ❌ | ❌ | ✅ (Audit logged) | Corrections require Admin role and trigger an audit entry. |
| **Study Materials** | | | | | |
| `GET /materials` | ❌ | ✅ (Enrolled) | ✅ | ✅ | Students see materials for their department courses. |
| `POST /materials/upload` | ❌ | ❌ | ✅ | ✅ | Staff can upload notes/QP for courses they teach. |
| `GET /materials/{id}/download` | ❌ | ✅ | ✅ | ✅ | Increments download tracking count. |
| `DELETE /materials/{id}` | ❌ | ❌ | ✅ (Own uploads) | ✅ (Any) | Staff can only delete files they uploaded themselves. |
| **Announcements & Circulars** | | | | | |
| `GET /announcements` | ✅ | ✅ | ✅ | ✅ | Public and authenticated circulars with targeted filtering. |
| `POST /announcements` | ❌ | ❌ | ❌ | ✅ | Admin/HOD creates official college/department circulars. |
| `DELETE /announcements/{id}` | ❌ | ❌ | ❌ | ✅ | Admin/HOD revokes/removes circular. |
| **Institutional Reports** | | | | | |
| `GET /reports/attendance/defaulters`| ❌ | ❌ | ❌ | ✅ | Attendance shortage (< 75%) lists. |
| `GET /reports/faculty/workload` | ❌ | ❌ | ❌ | ✅ | Faculty teaching hours and allocation. |
| `GET /reports/department/summary` | ❌ | ❌ | ❌ | ✅ | Departmental aggregated metrics. |
| **Security & Audit Logs** | | | | | |
| `GET /admin/audit-logs` | ❌ | ❌ | ❌ | ✅ | Administrator audit trail. |

---

## 3. Server-Side Security Enforcement Strategy

1. **Dependency Injection**:
   * `get_current_user`: Extracts and validates JWT signature, token expiration, and user `is_active` state.
   * `require_role(["STUDENT", "STAFF", "ADMIN"])`: Validates user role.
2. **Entity-Level Permission Checks**:
   * Even if a user has the `STAFF` role, the service layer explicitly verifies: `timetable_entry.staff_id == current_user.staff_id` before allowing attendance marking or material modification.
3. **Protected Field Immutability**:
   * Pydantic schemas enforce that client update payloads cannot alter primary keys, `user_id`, `department_id`, `register_number`, `role`, or `cgpa`.
