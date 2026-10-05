from datetime import date
from typing import Optional
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
    roll_number: str
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
