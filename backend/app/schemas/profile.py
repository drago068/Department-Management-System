from datetime import date
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, EmailStr


class DepartmentMini(BaseModel):
    id: str
    code: str
    name: str


class MentorMini(BaseModel):
    id: str
    full_name: str
    designation: str
    email: str
    cabin_number: Optional[str] = None


class StudentProfileData(BaseModel):
    role: str = "STUDENT"
    id: str
    register_number: str
    full_name: str
    department: DepartmentMini
    batch: str
    section: str
    semester: int
    cgpa: float
    phone: Optional[str] = None
    email: str
    date_of_birth: Optional[date] = None
    blood_group: Optional[str] = None
    address: Optional[str] = None
    avatar_url: Optional[str] = None
    faculty_mentor: Optional[MentorMini] = None


class StaffProfileData(BaseModel):
    role: str = "STAFF"
    id: str
    faculty_id: str
    full_name: str
    designation: str
    department: DepartmentMini
    email: str
    phone: Optional[str] = None
    cabin_number: Optional[str] = None
    qualifications: Optional[str] = None
    experience: Optional[str] = None
    avatar_url: Optional[str] = None


class AdminProfileData(BaseModel):
    role: str = "ADMIN"
    id: str
    full_name: str
    designation: str
    email: str
    phone: Optional[str] = None
    office_location: Optional[str] = None
    avatar_url: Optional[str] = None
    department: Optional[DepartmentMini] = None


class StudentProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None
    date_of_birth: Optional[Union[date, str]] = None
    avatar_url: Optional[str] = None


class StaffProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    cabin_number: Optional[str] = None
    qualifications: Optional[str] = None
    avatar_url: Optional[str] = None


class AdminProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    office_location: Optional[str] = None
    avatar_url: Optional[str] = None


class StudentEnrollRequest(BaseModel):
    full_name: str
    register_number: str
    department_id: Optional[str] = None
    department_code: Optional[str] = None
    batch_id: Optional[str] = None
    batch_name: Optional[str] = None
    section_id: Optional[str] = None
    section_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    blood_group: Optional[str] = None
    address: Optional[str] = None
    faculty_mentor_id: Optional[str] = None
    admission_category: Optional[str] = "Regular"
    lab_batch: Optional[str] = "A1"


class StudentEnrollResponse(BaseModel):
    id: str
    user_id: str
    register_number: str
    full_name: str
    email: str
    generated_password: str
    department_name: Optional[str] = None
    batch_name: Optional[str] = None
    section_name: Optional[str] = None
    message: str


class BulkStudentItem(BaseModel):
    register_number: str
    full_name: str
    email: Optional[str] = None
    department_code: Optional[str] = None
    department_id: Optional[str] = None
    batch_name: Optional[str] = None
    batch_id: Optional[str] = None
    section_name: Optional[str] = None
    section_id: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[Union[date, str]] = None
    blood_group: Optional[str] = None
    address: Optional[str] = None
    generated_password: Optional[str] = None
    user_id: Optional[str] = None


class BulkStudentEnrollRequest(BaseModel):
    students: List[BulkStudentItem]
    default_department_id: Optional[str] = None
    default_department_code: Optional[str] = None
    default_batch_id: Optional[str] = None
    default_batch_name: Optional[str] = None
    default_section_id: Optional[str] = None
    default_section_name: Optional[str] = None
    conflict_strategy: Optional[str] = "skip"  # "skip" or "update"


class BulkStudentEnrollResponse(BaseModel):
    total_processed: int
    enrolled_count: int
    skipped_count: int
    results: List[Dict[str, Any]]


# ─────────────────────────────────────────────────────────────
# Staff Onboarding Schemas
# ─────────────────────────────────────────────────────────────
class StaffEnrollRequest(BaseModel):
    faculty_id: str
    full_name: str
    email: str
    department_name: Optional[str] = None
    department_code: Optional[str] = None
    department_id: Optional[str] = None
    designation: Optional[str] = "Assistant Professor"
    phone: Optional[str] = None
    cabin_number: Optional[str] = None
    qualifications: Optional[str] = None
    experience: Optional[str] = None
    custom_password: Optional[str] = None


class StaffEnrollResponse(BaseModel):
    id: str
    user_id: str
    faculty_id: str
    full_name: str
    email: str
    generated_password: str
    designation: str
    department_name: Optional[str] = None
    message: str


class BulkStaffItem(BaseModel):
    faculty_id: str
    full_name: str
    email: Optional[str] = None
    department_code: Optional[str] = None
    department_name: Optional[str] = None
    designation: Optional[str] = "Assistant Professor"
    phone: Optional[str] = None
    cabin_number: Optional[str] = None
    qualifications: Optional[str] = None
    experience: Optional[str] = None
    generated_password: Optional[str] = None


class BulkStaffEnrollRequest(BaseModel):
    staff_members: List[BulkStaffItem]
    default_department_code: Optional[str] = None
    conflict_strategy: Optional[str] = "skip"  # "skip" or "update"


class BulkStaffEnrollResponse(BaseModel):
    total_processed: int
    enrolled_count: int
    skipped_count: int
    results: List[Dict[str, Any]]


# ─────────────────────────────────────────────────────────────
# Mentor & Proctor Allocation Schemas
# ─────────────────────────────────────────────────────────────
class FacultyMentorItem(BaseModel):
    id: str
    faculty_id: str
    name: str
    title: str
    department: str
    assigned: int
    capacity: int = 20


class StudentAllocationItem(BaseModel):
    id: str
    register_number: str
    name: str
    section: str
    department: Optional[str] = None
    batch: Optional[str] = None
    mentor: Optional[str] = None
    mentor_id: Optional[str] = None
    initials: Optional[str] = None
    avatar: Optional[str] = None


class StudentAllocationResponse(BaseModel):
    students: List[StudentAllocationItem]
    total_count: int
    unassigned_count: int
    assigned_count: int


class AssignMentorRequest(BaseModel):
    student_ids: List[str]
    faculty_mentor_id: Optional[str] = None  # staff UUID or faculty_id or faculty name


class UnassignMentorRequest(BaseModel):
    student_ids: List[str]


class AutoDistributeMentorsRequest(BaseModel):
    department_name: Optional[str] = None
    batch_name: Optional[str] = None
    section_name: Optional[str] = None
    student_ids: Optional[List[str]] = None
    faculty_ids: Optional[List[str]] = None

