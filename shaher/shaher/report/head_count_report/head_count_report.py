import frappe
from frappe import _

def execute(filters=None):
    filters = frappe._dict(filters or {})
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    can_view_salary = check_salary_visibility()

    columns = [
        {"label": _("Employee"), "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 150},
        {"label": _("Employee Type"), "fieldname": "employment_type", "fieldtype": "Data", "width": 150},
        {"label": _("Department"), "fieldname": "department", "fieldtype": "Link", "options": "Department", "width": 120},
        {"label": _("Company"), "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
        {"label": _("Attendance Date"), "fieldname": "attendance_date", "fieldtype": "Date", "width": 120},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]

    if can_view_salary:
        columns.append({"label": _("Salary"), "fieldname": "custom_basic", "fieldtype": "Currency", "width": 150})

    return columns

def get_data(filters):
    conditions, values = get_conditions(filters)

    
    can_view_salary = check_salary_visibility()

   
    query = """
        SELECT
            att.employee AS employee,
            emp.employee_name AS employee_name,
            emp.department AS department,
            emp.company AS company,
            emp.employment_type AS employment_type,
            att.attendance_date AS attendance_date,
            att.status AS status
    """

    
    if can_view_salary:
        query += ", emp.custom_basic AS custom_basic"

    query += """
        FROM `tabAttendance` att
        JOIN `tabEmployee` emp ON att.employee = emp.name
        WHERE emp.status = 'Active'
    """

    if conditions:
        query += " AND " + " AND ".join(conditions)

    query += " ORDER BY att.attendance_date DESC"

    return frappe.db.sql(query, values, as_dict=True)

def get_conditions(filters):
    conditions = []
    values = {}

    if filters.get("department"):
        conditions.append("emp.department = %(department)s")
        values["department"] = filters.get("department")

    if filters.get("company"):
        conditions.append("emp.company = %(company)s")
        values["company"] = filters.get("company")

    if filters.get("from_date") and filters.get("to_date"):
        conditions.append("att.attendance_date BETWEEN %(from_date)s AND %(to_date)s")
        values["from_date"] = filters.get("from_date")
        values["to_date"] = filters.get("to_date")

    return conditions, values

def check_salary_visibility():
    user_roles = frappe.get_roles(frappe.session.user)
    return "HR Manager" in user_roles or "System Manager" in user_roles
