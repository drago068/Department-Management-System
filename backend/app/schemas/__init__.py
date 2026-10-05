from app.schemas.common import (
    StandardResponse,
    ErrorDetail,
    ErrorResponse,
    PaginationMetadata,
    PaginatedData,
    PaginatedResponse,
)
from app.schemas.auth import (
    LoginRequest,
    TokenResponseData,
    RefreshTokenRequest,
    UserAuthResponse,
    UserProfileSummary,
)
from app.schemas.profile import (
    StudentProfileData,
    StaffProfileData,
    AdminProfileData,
    StudentProfileUpdate,
    StaffProfileUpdate,
    AdminProfileUpdate,
)
from app.schemas.academic import (
    DepartmentResponse,
    AcademicYearResponse,
    SemesterResponse,
    BatchResponse,
    SectionResponse,
    CourseResponse,
    RoomResponse,
    PeriodResponse,
)
from app.schemas.timetable import (
    TimetableSlotItem,
    TimetableScheduleResponse,
    TimetableEntryCreate,
    TimetableEntryUpdate,
)
from app.schemas.attendance import (
    StudentRosterItem,
    TimetableSlotInfo,
    SessionRosterResponse,
    AttendanceRecordInput,
    AttendanceSubmitRequest,
    AttendanceSubmitResponse,
    SubjectAttendanceItem,
    StudentAttendanceSummaryResponse,
    AttendanceHistoryItem,
)
from app.schemas.materials import MaterialItemResponse
from app.schemas.announcements import AnnouncementItemResponse, AnnouncementCreateRequest
from app.schemas.reports import (
    DefaulterStudentItem,
    DefaulterReportResponse,
    FacultyWorkloadItem,
    FacultyWorkloadResponse,
    DepartmentKpiResponse,
)
