from openpyxl import Workbook
from openpyxl.styles import Alignment, PatternFill, Border, Side, Font
from openpyxl.utils import get_column_letter
from io import BytesIO
import frappe


@frappe.whitelist()
def download():
    filename = "HSE Register"
    file = make_hse_xlsx(filename)
    frappe.response["filename"] = filename + ".xlsx"
    frappe.response["filecontent"] = file.getvalue()
    frappe.response["type"] = "binary"


def make_hse_xlsx(sheet_name):

    detail_fields = [
        "S No","Full Name","Designation","Employee No",
        "Site Location","Date of Birth","Resident Card No",
        "Email ID","Contact Number","Resident Card No Expiry Date",
        "ROP License Expiry Date","branch / Contract No",
        "HSE Passport Issued Institute Name","HSE Passport Number"
    ]

    # ------------------------------------
    # Collect Course Groups & Courses
    # ------------------------------------
    course_groups = frappe.get_all("Course Group", fields=["name"])
    group_courses = {}

    for grp in course_groups:
        courses = frappe.get_all(
            "Course",
            filters={"course_group": grp.name},
            fields=["course_name"],
            order_by="course_name asc"
        )
        group_courses[grp.name] = [c.course_name for c in courses]

    # ---- flat ordered course list (important for training map & row order)
    all_courses = []
    for group, courses in group_courses.items():
        all_courses.extend(courses)

    # ------------------------------------
    # Prepare Workbook
    # ------------------------------------
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name

    yellow   = PatternFill("solid", fgColor="FFC000")
    blue     = PatternFill("solid", fgColor="BDD7EE")
    border   = Border(left=Side(style='thin'), right=Side(style='thin'),
                      top=Side(style='thin'), bottom=Side(style='thin'))
    title_al = Alignment(horizontal='center', vertical='center')
    wrap_al  = Alignment(horizontal='center', vertical='center', wrap_text=True)

    total_cols = len(detail_fields) + len(all_courses)

    # ------------------------------------
    # ROW 1 — Title
    # ------------------------------------
    ws.append(["HSE TRAINING REGISTER"])
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=total_cols)
    ws["A1"].fill = yellow
    ws["A1"].font = Font(bold=True, size=14)
    ws["A1"].alignment = title_al

    # ------------------------------------
    # ROW 2 — DETAILS + Group Headers
    # ------------------------------------
    row2 = ["DETAILS"] + [""] * (len(detail_fields) - 1)

    for group, courses in group_courses.items():
        if courses:
            row2.append(group)
            row2.extend([""] * (len(courses) - 1))

    ws.append(row2)

    # merge DETAILS
    ws.merge_cells(start_row=2, start_column=1,
                   end_row=2, end_column=len(detail_fields))

    # merge groups
    col_start = len(detail_fields) + 1
    for group, courses in group_courses.items():
        if courses:
            col_end = col_start + len(courses) - 1
            ws.merge_cells(start_row=2, start_column=col_start,
                           end_row=2, end_column=col_end)
            col_start = col_end + 1

    # formatting row2
    for col in range(1, total_cols + 1):
        c = ws.cell(row=2, column=col)
        c.fill = yellow
        c.font = Font(bold=True)
        c.alignment = title_al
        c.border = border

    # ------------------------------------
    # ROW 3 — Column Headers (Details + Courses)
    # ------------------------------------
    row3 = detail_fields[:] + all_courses[:]
    ws.append(row3)

    for col in range(1, total_cols + 1):
        c = ws.cell(row=3, column=col)
        c.fill = blue
        c.font = Font(bold=True)
        c.alignment = wrap_al
        c.border = border
        ws.column_dimensions[get_column_letter(col)].width = 25

    # ------------------------------------
    # TRAINING MATRIX → latest expiry per employee & course
    # ------------------------------------
    training_map = get_training_matrix_latest()

    # ------------------------------------
    # EMPLOYEE ROWS
    # ------------------------------------
    employees = get_filtered_employees()
    serial_no = 1

    for emp in employees:
        row = [
            serial_no,
            emp.employee_name,
            emp.designation,
            emp.name,
            emp.custom_site_location,
            emp.date_of_birth,
            emp.custom_resident_id_numberqid_number,
            emp.user_id,
            emp.cell_number,
            emp.custom_resident_id_expiry_date,
            emp.custom_visa_expiry_date,
            emp.branch,
            emp.issued_institute_name,
            emp.hse_passport_number,
        ]

        # fill latest expiry date for each course
        for course in all_courses:
            key = (emp.name, course)
            expiry = training_map.get(key, "")
            row.append(expiry)

        ws.append(row)
        serial_no += 1

    ws.freeze_panes = "A4"
    ws.auto_filter.ref = ws.dimensions

    out = BytesIO()
    wb.save(out)
    out.seek(0)
    return out


# --------------------------------------------------
# DATA FETCHING METHODS
# --------------------------------------------------

def get_training_matrix_latest():

    rows = frappe.db.sql("""
        SELECT
            parent AS employee,
            course_name,
            MAX(STR_TO_DATE(expiry_date, '%Y-%m-%d')) AS latest_expiry
        FROM `tabHSE Training Matrix`
        GROUP BY employee, course_name
    """, as_dict=True)

    out = {}
    for r in rows:
        out[(r.employee, r.course_name)] = r.latest_expiry
    return out


def get_filtered_employees():
    """Return active employees who have an HSE document,
    filtered by company & division if provided."""

    company  = frappe.local.form_dict.get("company")
    division = frappe.local.form_dict.get("division")

    filters = []
    params  = []

    if company:
        filters.append("e.company = %s")
        params.append(company)

    if division:
        filters.append("e.custom_division = %s")
        params.append(division)

    where_clause = " AND ".join(filters) if filters else "1=1"

    return frappe.db.sql(f"""
        SELECT
            e.name,
            e.employee_name,
            e.designation,
            e.custom_site_location,
            e.date_of_birth,
            e.custom_resident_id_numberqid_number,
            e.user_id,
            e.cell_number,
            e.custom_resident_id_expiry_date,
            e.custom_visa_expiry_date,
            e.branch,
            ed.issued_institute_name,
            ed.hse_passport_number
        FROM `tabEmployee` e
        INNER JOIN `tabHSE` ed
            ON ed.employee = e.name
        WHERE
            e.status = 'Active'
            AND {where_clause}
        ORDER BY e.employee_name
    """, params, as_dict=True)
