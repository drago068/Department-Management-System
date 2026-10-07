from datetime import date
from typing import Any, Dict, List, Optional
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
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
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
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    parent_phone: Optional[str] = None
    blood_group: Optional[str] = None
    date_of_birth: Optional[date] = None
    avatar_url: Optional[str] = None


class StaffProfileUpdate(BaseModel):
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    cabin_number: Optional[str] = None
    qualifications: Optional[str] = None
    avatar_url: Optional[str] = None


class AdminProfileUpdate(BaseModel):
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
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
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
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    gender: Optional[str] = None
    user_id: Optional[str] = None


class BulkStudentEnrollRequest(BaseModel):
    students: List[BulkStudentItem]
    default_department_id: Optional[str] = None
    default_batch_id: Optional[str] = None
    default_section_id: Optional[str] = None


class BulkStudentEnrollResponse(BaseModel):
    total_processed: int
    enrolled_count: int
    skipped_count: int
    results: List[Dict[str, Any]]
