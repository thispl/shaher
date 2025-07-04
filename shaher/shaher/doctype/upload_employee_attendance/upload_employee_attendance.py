# Copyright (c) 2025, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date, datetime, timedelta
import openpyxl
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from six import BytesIO
from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr
from frappe.utils.file_manager import get_file
import csv
import io
from datetime import datetime, timedelta
from frappe import _
from frappe.utils import getdate, get_site_path
from frappe.utils.file_manager import get_file
from frappe.utils import getdate
from frappe import _

class UploadEmployeeAttendance(Document):
    
    def on_cancel(self):
        att=frappe.db.get_all("Attendance",{'custom_upload_attendance':self.name,'docstatus':1},['name'])
        for a in att:
            doc = frappe.get_doc('Attendance', {'name':a.name})
            doc.cancel()
            frappe.db.commit()
    def on_submit(self):
        if not self.upload_attendance:
            frappe.throw(_("Please upload an attendance file."))

        try:
            filename, file_content = get_file(self.upload_attendance)
            file_text = file_content.decode('utf-8') if isinstance(file_content, bytes) else file_content
            file_obj = io.StringIO(file_text)
            self.create_attendance_from_csv(file_obj)
        except Exception as e:
            import traceback
            traceback.print_exc()
            frappe.throw(_("Error reading or processing the uploaded CSV file: {0}").format(str(e)))

    def create_attendance_from_csv(self, file_obj):
        reader = csv.reader(file_obj)
        rows = list(reader)
        if len(rows) < 3:
            frappe.throw(_("The uploaded CSV doesn't have enough rows."))
        dates = get_dates(self.from_date, self.to_date)  
        for row in rows[2:]: 
            employee_id = row[1].strip() if len(row) > 1 else ""
            employee_name = row[2].strip() if len(row) > 2 else ""

            if not employee_id:
                continue

            col_idx = 2 
            for date in dates:
                if col_idx + 1 >= len(row):
                    break
                status = row[col_idx].strip()
                overtime = row[col_idx + 1].strip()
                col_idx += 2
                if not status:
                    status='A'
                if not frappe.db.exists("Attendance", {
                    "employee": employee_id,
                    "attendance_date": date,
                    "docstatus": ["!=", 2]
                }):
                    doc = frappe.new_doc("Attendance")
                    doc.employee = employee_id
                    doc.employee_name = employee_name
                    doc.attendance_date = date
                    status_given = status.strip().upper()
                    if status_given == "P":
                        doc.status = "Present"
                    elif status_given == "A":
                        doc.status = "Absent"
                    elif status_given == "HD":
                        doc.status = "Half Day"
                    elif status_given == "RD":
                        doc.status = "Absent"
                        doc.custom_rest_day=1
                    else:
                        doc.status = "Absent"
                    doc.custom_upload_attendance=self.name
                    doc.custom_overtime_hours = float(overtime) if overtime else 0.0
                    doc.insert(ignore_permissions=True)
                    doc.submit()
                    frappe.db.commit()

@frappe.whitelist()
def get_template(from_date, to_date, department=None, designation=None, name=None):
    args = frappe.local.form_dict
    csv_file = make_csv(args)
    filename = "Attendance_Template"
    frappe.response['filename'] = filename + '.csv'
    frappe.response['filecontent'] = csv_file.getvalue()
    frappe.response['type'] = 'binary'

def make_csv(args):
    output = io.StringIO()
    writer = csv.writer(output)
    date_headers = get_dates(args['from_date'], args['to_date'])
    write_headers(writer, date_headers)
    employees = get_employees(args)
    sr_no = 1
    frappe.log_error(
            title="emmp Debug Log",
            message=f"emmp received: {employees}"
        )
    for emp in employees:
        frappe.log_error(
            title="emp Debug Log",
            message=f"emp received: {emp}"
        )
        row = [sr_no, emp.name]
        writer.writerow(row)
        sr_no += 1

    output.seek(0)
    return output

def get_dates(from_date, to_date):
    start_date = datetime.strptime(from_date, "%Y-%m-%d")
    end_date = datetime.strptime(to_date, "%Y-%m-%d")
    delta = end_date - start_date
    return [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(delta.days + 1)]

def write_headers(writer, date_headers):
    first_row = ['Sr No.', 'Employee']
    for date in date_headers:
        first_row.extend([datetime.strptime(date, "%Y-%m-%d").strftime("%d-%b"), ''])
    writer.writerow(first_row)
    second_row = ['', '']
    for _ in date_headers:
        second_row.extend(['Status', 'OT'])
    writer.writerow(second_row)

def get_employees(args):
    filters = {'status': 'Active'}
    dept=frappe.db.get_value("Upload Employee Attendance",{'name':args.name},['department'])
    desi=frappe.db.get_value("Upload Employee Attendance",{'name':args.name},['designation'])
    comp=frappe.db.get_value("Upload Employee Attendance",{'name':args.name},['company'])
    if args.department and args.department!='None':
        if dept:
            filters['department'] = dept
    if args.designation and args.designation!='None':
        if desi:
            filters['designation'] = desi
    if args.company and args.company!='None':
        if comp:
            filters['company'] = comp
    employees = frappe.db.get_all('Employee', filters=filters, fields=['name', 'employee_name'])
    
    
    return employees


