import io
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


def generate_student_enrollment_template() -> io.BytesIO:
    """Generates an official styled Excel template (.xlsx) for bulk student enrollment."""
    wb = openpyxl.Workbook()

    # ─────────────────────────────────────────────────────────────
    # SHEET 1: Student Roster Template
    # ─────────────────────────────────────────────────────────────
    ws = wb.active
    ws.title = "Student_Roster"
    ws.views.sheetView[0].showGridLines = True

    headers = [
        "register_number",
        "full_name",
        "email",
        "phone",
        "gender",
        "date_of_birth",
        "blood_group",
        "address",
        "department_code",
        "batch_name",
        "section_name",
    ]

    header_labels = [
        "Register Number *",
        "Full Name *",
        "Email (Optional)",
        "Mobile Number",
        "Gender",
        "Date of Birth (YYYY-MM-DD)",
        "Blood Group",
        "Address",
        "Department Code",
        "Batch Name",
        "Section",
    ]

    # Color tokens
    header_fill = PatternFill(start_color="003FB1", end_color="003FB1", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    thin_border = Border(
        left=Side(style="thin", color="D1D5DB"),
        right=Side(style="thin", color="D1D5DB"),
        top=Side(style="thin", color="D1D5DB"),
        bottom=Side(style="thin", color="D1D5DB"),
    )
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")

    # Write Header Row
    ws.row_dimensions[1].height = 28
    for col_idx, (col_id, label) in enumerate(zip(headers, header_labels), start=1):
        cell = ws.cell(row=1, column=col_idx, value=col_id)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align
        cell.border = thin_border

    # Sample Data Rows
    sample_data = [
        [
            "714022AD001",
            "Arjun Patel",
            "arjun.p@suguna.edu",
            "+91 9876543210",
            "Male",
            "2004-05-14",
            "O+",
            "142, North Street, Coimbatore",
            "AIDS",
            "2024-2028",
            "A",
        ],
        [
            "714022AD002",
            "Bhavana S",
            "bhavana.s@suguna.edu",
            "+91 9876543211",
            "Female",
            "2004-08-22",
            "A+",
            "54, Gandhi Nagar, Coimbatore",
            "AIDS",
            "2024-2028",
            "A",
        ],
        [
            "714022AD003",
            "Rahul V",
            "rahul.v@suguna.edu",
            "+91 9876543212",
            "Male",
            "2004-11-10",
            "B+",
            "12, Crosscut Road, Coimbatore",
            "AIDS",
            "2024-2028",
            "A",
        ],
        [
            "24AD012",
            "Abishek R K",
            "abishek.24ad012@suguna.edu.in",
            "+91 9842177310",
            "Male",
            "2005-04-18",
            "O+",
            "42, Bharathi Park 7th Cross, Coimbatore",
            "AIDS",
            "2024-2028",
            "A",
        ],
    ]

    sample_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    data_font = Font(name="Calibri", size=10, color="1F2937")

    for row_idx, row_values in enumerate(sample_data, start=2):
        ws.row_dimensions[row_idx].height = 22
        for col_idx, val in enumerate(row_values, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = data_font
            cell.alignment = left_align
            cell.border = thin_border
            if row_idx % 2 == 1:
                cell.fill = sample_fill

    # Auto-adjust column widths
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or "")
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 15)

    # ─────────────────────────────────────────────────────────────
    # SHEET 2: Instructions & Predefined Password Rules
    # ─────────────────────────────────────────────────────────────
    ws_guide = wb.create_sheet(title="Instructions_&_Rules")
    ws_guide.views.sheetView[0].showGridLines = True

    title_font = Font(name="Calibri", size=14, bold=True, color="003FB1")
    subtitle_font = Font(name="Calibri", size=10, italic=True, color="4B5563")
    section_font = Font(name="Calibri", size=12, bold=True, color="111827")
    bold_font = Font(name="Calibri", size=10, bold=True, color="111827")
    normal_font = Font(name="Calibri", size=10, color="374151")
    highlight_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    highlight_font = Font(name="Calibri", size=11, bold=True, color="92400E")

    ws_guide.cell(row=1, column=1, value="NEXUS CMS — Student Bulk Enrollment Specification").font = title_font
    ws_guide.cell(row=2, column=1, value="Suguna College of Engineering • Academic Governance & Enrollment Hub").font = subtitle_font

    ws_guide.cell(row=4, column=1, value="⭐ PREDEFINED PASSWORD FORMULA ENFORCEMENT").font = section_font
    ws_guide.merge_cells("A5:F5")
    rule_cell = ws_guide.cell(
        row=5,
        column=1,
        value="Default Password Rule: First 3 characters of student's name (lowercase only) + last 3 digits of register number.",
    )
    rule_cell.fill = highlight_fill
    rule_cell.font = highlight_font
    rule_cell.alignment = left_align
    ws_guide.row_dimensions[5].height = 26

    examples = [
        ("Student Name", "Register Number", "Name Prefix (3 chars lower)", "Reg Suffix (3 nums)", "Generated Default Password"),
        ("Arjun Patel", "714022AD001", "arj", "001", "arj001"),
        ("Abishek R K", "24AD012", "abi", "012", "abi012"),
        ("Bhavana S", "714022AD002", "bha", "002", "bha002"),
        ("Sneha K", "714022AD004", "sne", "004", "sne004"),
    ]

    for r_idx, row_data in enumerate(examples, start=7):
        ws_guide.row_dimensions[r_idx].height = 20
        for c_idx, val in enumerate(row_data, start=1):
            c = ws_guide.cell(row=r_idx, column=c_idx, value=val)
            c.border = thin_border
            if r_idx == 7:
                c.fill = PatternFill(start_color="E5E7EB", end_color="E5E7EB", fill_type="solid")
                c.font = bold_font
                c.alignment = center_align
            else:
                c.font = normal_font
                c.alignment = center_align
                if c_idx == 5:
                    c.font = Font(name="Calibri", size=10, bold=True, color="003FB1")
                    c.fill = PatternFill(start_color="EEF2FF", end_color="EEF2FF", fill_type="solid")

    ws_guide.cell(row=14, column=1, value="COLUMN SPECIFICATIONS & RULES").font = section_font

    col_specs = [
        ("Column Name", "Required?", "Data Type", "Description & Rules"),
        ("register_number", "YES", "String", "Unique college registration/roll number (e.g. 714022AD001, 24AD012)"),
        ("full_name", "YES", "String", "Official student full name as per mark-sheet"),
        ("email", "Optional", "Email", "Institutional email. If omitted, generated as first_name.reg_no@suguna.edu.in"),
        ("phone", "Optional", "String", "Student active mobile phone number with +91 country code"),
        ("gender", "Optional", "String", "Male / Female / Other"),
        ("date_of_birth", "Optional", "Date", "Format YYYY-MM-DD (e.g. 2005-04-18)"),
        ("blood_group", "Optional", "String", "O+, A+, B+, AB+, O-, A-, B-, AB-"),
        ("address", "Optional", "Text", "Permanent residential address"),
        ("department_code", "Optional", "String", "e.g. AIDS, CSE, ECE (Defaults to target department selected on screen)"),
        ("batch_name", "Optional", "String", "e.g. 2024-2028 (Defaults to target batch selected on screen)"),
        ("section_name", "Optional", "String", "e.g. A, B (Defaults to target section selected on screen)"),
    ]

    for r_idx, row_data in enumerate(col_specs, start=16):
        ws_guide.row_dimensions[r_idx].height = 20
        for c_idx, val in enumerate(row_data, start=1):
            c = ws_guide.cell(row=r_idx, column=c_idx, value=val)
            c.border = thin_border
            if r_idx == 16:
                c.fill = PatternFill(start_color="E5E7EB", end_color="E5E7EB", fill_type="solid")
                c.font = bold_font
                c.alignment = center_align
            else:
                c.font = normal_font
                if c_idx == 2 and val == "YES":
                    c.font = Font(name="Calibri", size=10, bold=True, color="B91C1C")
                c.alignment = left_align

    ws_guide.column_dimensions["A"].width = 22
    ws_guide.column_dimensions["B"].width = 24
    ws_guide.column_dimensions["C"].width = 26
    ws_guide.column_dimensions["D"].width = 24
    ws_guide.column_dimensions["E"].width = 30
    ws_guide.column_dimensions["F"].width = 24

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output


import csv
import re
from datetime import date, datetime
from typing import Any, Dict, List


def generate_predefined_password(name: str, reg_no: str) -> str:
    cleaned_name = "".join(c for c in (name or "") if c.isalpha()).lower()
    prefix = (cleaned_name[:3] if len(cleaned_name) >= 3 else (cleaned_name + "stu")[:3]).lower()
    digits = re.sub(r"\D", "", reg_no or "")
    suffix = digits[-3:] if len(digits) >= 3 else (digits.zfill(3) if digits else "001")
    return f"{prefix}{suffix}"


def parse_student_upload_file(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    """Parses an uploaded student roster Excel (.xlsx, .xls) or CSV file.
    
    Returns structured list of validated student objects with auto-generated passwords.
    """
    raw_rows: List[List[Any]] = []
    lower_fn = filename.lower()

    if lower_fn.endswith((".xlsx", ".xlsm", ".xltx", ".xltm")):
        wb = openpyxl.load_workbook(io.BytesIO(file_bytes), data_only=True)
        ws = wb["Student_Roster"] if "Student_Roster" in wb.sheetnames else wb.active
        for row in ws.iter_rows(values_only=True):
            raw_rows.append(list(row))
    elif lower_fn.endswith(".csv"):
        for encoding in ["utf-8-sig", "utf-8", "latin-1"]:
            try:
                text = file_bytes.decode(encoding)
                reader = csv.reader(io.StringIO(text))
                raw_rows = [list(r) for r in reader]
                break
            except Exception:
                continue
    else:
        try:
            wb = openpyxl.load_workbook(io.BytesIO(file_bytes), data_only=True)
            ws = wb["Student_Roster"] if "Student_Roster" in wb.sheetnames else wb.active
            for row in ws.iter_rows(values_only=True):
                raw_rows.append(list(row))
        except Exception:
            text = file_bytes.decode("utf-8-sig", errors="ignore")
            reader = csv.reader(io.StringIO(text))
            raw_rows = [list(r) for r in reader]

    if not raw_rows:
        return {
            "filename": filename,
            "total_records": 0,
            "valid_count": 0,
            "error_count": 0,
            "students": [],
            "errors": ["Uploaded file is empty or could not be parsed."],
        }

    # Normalize header mapping
    header_raw = raw_rows[0]
    col_mapping: Dict[int, str] = {}

    canonical_aliases = {
        "register_number": ["register_number", "reg_no", "regno", "reg_number", "roll_number", "roll_no", "registration_number", "reg", "roll"],
        "full_name": ["full_name", "student_name", "studentname", "name", "candidate_name"],
        "email": ["email", "email_id", "email_address", "student_email", "mail"],
        "phone": ["phone", "mobile", "mobile_number", "phone_number", "contact", "student_phone"],
        "gender": ["gender", "sex"],
        "date_of_birth": ["date_of_birth", "dob", "birth_date", "birthdate"],
        "blood_group": ["blood_group", "blood", "bloodgroup", "bg"],
        "address": ["address", "permanent_address", "residential_address", "residence"],
        "department_code": ["department_code", "dept_code", "department", "dept", "branch"],
        "batch_name": ["batch_name", "batch", "batch_year", "intake_batch"],
        "section_name": ["section_name", "section", "sec"],
    }

    for idx, cell_val in enumerate(header_raw):
        if cell_val is None:
            continue
        cleaned = re.sub(r"[^a-zA-Z0-9_]", "", str(cell_val).strip().lower().replace(" ", "_").replace("-", "_"))
        # Strictly ignore legacy parent fields if an older template or sheet is uploaded
        if "parent" in cleaned:
            continue
        # Exact match first
        matched = False
        for field, aliases in canonical_aliases.items():
            if cleaned in aliases:
                col_mapping[idx] = field
                matched = True
                break
        if not matched:
            for field, aliases in canonical_aliases.items():
                if any(alias in cleaned for alias in aliases):
                    col_mapping[idx] = field
                    break

    valid_students: List[Dict[str, Any]] = []
    errors: List[str] = []

    for row_num, row in enumerate(raw_rows[1:], start=2):
        # Skip completely empty rows
        if not any(c is not None and str(c).strip() != "" for c in row):
            continue

        item_dict: Dict[str, Any] = {}
        for col_idx, field_name in col_mapping.items():
            if col_idx < len(row):
                val = row[col_idx]
                if val is not None:
                    if isinstance(val, (datetime, date)):
                        item_dict[field_name] = val.strftime("%Y-%m-%d")
                    elif isinstance(val, float) and val.is_integer():
                        item_dict[field_name] = str(int(val))
                    else:
                        item_dict[field_name] = str(val).strip()
                else:
                    item_dict[field_name] = None

        reg = str(item_dict.get("register_number") or "").strip().upper()
        name = str(item_dict.get("full_name") or "").strip()

        if not reg or not name:
            errors.append(f"Row {row_num}: Missing required field (Register Number or Full Name).")
            continue

        pwd = generate_predefined_password(name, reg)
        first_token = name.split()[0].lower() if name.split() else "student"
        email = item_dict.get("email") or f"{first_token}.{reg.lower()}@suguna.edu.in"

        student_data = {
            "register_number": reg,
            "full_name": name,
            "email": email,
            "phone": item_dict.get("phone") or "",
            "gender": item_dict.get("gender") or "Male",
            "date_of_birth": item_dict.get("date_of_birth") or None,
            "blood_group": item_dict.get("blood_group") or None,
            "address": item_dict.get("address") or "",
            "department_code": item_dict.get("department_code") or None,
            "batch_name": item_dict.get("batch_name") or None,
            "section_name": item_dict.get("section_name") or None,
            "generated_password": pwd,
        }
        valid_students.append(student_data)

    return {
        "filename": filename,
        "total_records": len(raw_rows) - 1,
        "valid_count": len(valid_students),
        "error_count": len(errors),
        "students": valid_students,
        "errors": errors,
    }


def generate_staff_enrollment_template() -> io.BytesIO:
    """Generates an official styled Excel template (.xlsx) for bulk staff onboarding."""
    wb = openpyxl.Workbook()

    ws = wb.active
    ws.title = "Staff_Roster"
    ws.views.sheetView[0].showGridLines = True

    headers = [
        "faculty_id",
        "full_name",
        "email",
        "department_code",
        "designation",
        "phone",
        "cabin_number",
        "qualifications",
        "experience",
    ]

    header_labels = [
        "Faculty ID *",
        "Full Name *",
        "Email *",
        "Department Code *",
        "Designation *",
        "Phone Number",
        "Cabin Number",
        "Highest Qualification",
        "Experience",
    ]

    header_fill = PatternFill(start_color="003FB1", end_color="003FB1", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    thin_border = Border(
        left=Side(style="thin", color="D1D5DB"),
        right=Side(style="thin", color="D1D5DB"),
        top=Side(style="thin", color="D1D5DB"),
        bottom=Side(style="thin", color="D1D5DB"),
    )
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")

    ws.row_dimensions[1].height = 28
    for col_idx, col_id in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx, value=col_id)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align
        cell.border = thin_border

    sample_data = [
        [
            "FAC-CSE-102",
            "Dr. Sarah Jenkins",
            "s.jenkins@suguna.edu.in",
            "CSE",
            "Associate Professor",
            "+91 98452 10839",
            "Cabin 304, Turing Block",
            "Ph.D. in Computer Science & AI, M.Tech",
            "8 Years Teaching & Research",
        ],
        [
            "FAC-AIDS-105",
            "Prof. Ramesh Kumar",
            "r.kumar@suguna.edu.in",
            "AIDS",
            "Assistant Professor",
            "+91 98452 10840",
            "Cabin 201, Ramanujan Wing",
            "M.Tech AI, B.Tech CSE",
            "5 Years",
        ],
        [
            "FAC-ECE-201",
            "Dr. Meenakshi S",
            "m.s@suguna.edu.in",
            "ECE",
            "Professor & HOD",
            "+91 98452 10841",
            "Cabin 101, Admin Block",
            "Ph.D. VLSI Design",
            "15 Years",
        ],
    ]

    zebra_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

    for row_idx, row_values in enumerate(sample_data, start=2):
        ws.row_dimensions[row_idx].height = 22
        current_fill = zebra_fill if row_idx % 2 == 0 else white_fill
        for col_idx, val in enumerate(row_values, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.fill = current_fill
            cell.font = Font(name="Calibri", size=10)
            cell.border = thin_border
            cell.alignment = left_align

    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            v_str = str(cell.value or "")
            if len(v_str) > max_len:
                max_len = len(v_str)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 16)

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output


def parse_staff_upload_file(file_bytes: bytes, filename: str) -> dict:
    """Parses an uploaded staff Excel (.xlsx, .xls) or CSV roster."""
    import csv

    lower_name = filename.lower()
    raw_rows = []

    if lower_name.endswith(".csv"):
        text = file_bytes.decode("utf-8-sig", errors="replace")
        csv_reader = csv.reader(io.StringIO(text))
        raw_rows = [row for row in csv_reader if any(cell.strip() for cell in row)]
    else:
        wb = openpyxl.load_workbook(io.BytesIO(file_bytes), data_only=True)
        sheet = wb.active
        for row in sheet.iter_rows(values_only=True):
            if any(cell is not None and str(cell).strip() for cell in row):
                raw_rows.append([str(cell).strip() if cell is not None else "" for cell in row])

    if not raw_rows:
        return {"filename": filename, "total_records": 0, "valid_count": 0, "error_count": 1, "staff": [], "errors": ["File is empty"]}

    header_row = [str(c).strip().lower().replace(" ", "_").replace("*", "").replace(".", "_") for c in raw_rows[0]]

    # Map aliases
    alias_map = {
        "faculty_id": ["faculty_id", "facultyid", "employee_id", "emp_id", "id", "users_identifier", "identifier"],
        "full_name": ["full_name", "fullname", "name", "faculty_name", "staff_full_name"],
        "email": ["email", "email_address", "institutional_email", "staff_email"],
        "department_code": ["department_code", "department", "dept", "dept_code", "staff_department_id"],
        "designation": ["designation", "role", "title", "staff_designation"],
        "phone": ["phone", "mobile", "contact", "phone_number"],
        "cabin_number": ["cabin_number", "cabin", "office", "room"],
        "qualifications": ["qualifications", "qualification", "degree"],
        "experience": ["experience", "exp", "years_experience"],
    }

    col_index_map = {}
    for standard_col, aliases in alias_map.items():
        for idx, h_val in enumerate(header_row):
            if h_val in aliases:
                col_index_map[standard_col] = idx
                break

    valid_staff = []
    errors = []

    for row_num, row in enumerate(raw_rows[1:], start=2):
        if not any(str(c).strip() for c in row):
            continue

        item_dict = {}
        for std_col, col_idx in col_index_map.items():
            if col_idx < len(row):
                item_dict[std_col] = str(row[col_idx]).strip()

        fid = str(item_dict.get("faculty_id") or "").strip().upper()
        name = str(item_dict.get("full_name") or "").strip()

        if not fid or not name:
            errors.append(f"Row {row_num}: Missing required field (Faculty ID or Full Name).")
            continue

        pwd = generate_predefined_password(name, fid)
        email = item_dict.get("email")
        if not email:
            clean_name = name.lower().replace("dr.", "").replace("prof.", "").strip().split()[0]
            email = f"{clean_name}.{fid.lower()}@suguna.edu.in"

        staff_data = {
            "faculty_id": fid,
            "full_name": name,
            "email": email,
            "department_code": item_dict.get("department_code") or "AIDS",
            "designation": item_dict.get("designation") or "Assistant Professor",
            "phone": item_dict.get("phone") or "",
            "cabin_number": item_dict.get("cabin_number") or "",
            "qualifications": item_dict.get("qualifications") or "",
            "experience": item_dict.get("experience") or "",
            "generated_password": pwd,
        }
        valid_staff.append(staff_data)

    return {
        "filename": filename,
        "total_records": len(raw_rows) - 1,
        "valid_count": len(valid_staff),
        "error_count": len(errors),
        "staff": valid_staff,
        "errors": errors,
    }

