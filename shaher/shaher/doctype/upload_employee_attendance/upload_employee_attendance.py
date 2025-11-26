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
import requests
from frappe.utils import getdate
from datetime import datetime, timedelta
from frappe import _
from frappe.utils.file_manager import get_file
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import GradientFill, PatternFill

class UploadEmployeeAttendance(Document):
    
    def on_cancel(self):
        att_count = frappe.db.count("Attendance", {'custom_upload_attendance': self.name,'docstatus': 1})
        if att_count > 40:
            frappe.enqueue("shaher.shaher.doctype.upload_employee_attendance.upload_employee_attendance.cancel_attendance_records", 
                queue='long', 
                timeout=1000, 
                docname=self.name)
        else:
            cancel_attendance_records(self.name)


    def on_submit(self):
        file_url = frappe.db.get_value(
            "File",
            {"attached_to_doctype": "Upload Employee Attendance", "attached_to_name": self.name},
            "file_url"
        )
        if not file_url:
            frappe.throw(_("No file attached for this document."))

        try:
            in_memory_file = download_external_file_url(file_url)
            wb = openpyxl.load_workbook(in_memory_file)
            ws = wb.active
        except Exception as e:
            frappe.throw(f"Failed to read Excel file: {str(e)}")

        emp_count = get_employee_count(ws)

        if emp_count > 30:
            frappe.enqueue(
                method="shaher.shaher.doctype.upload_employee_attendance.upload_employee_attendance.process_attendance_from_excel_job",
                queue="default",
                timeout=1200,
                now=False,
                docname=self.name
            )
            frappe.msgprint("Attendance is updating in the background.Kindly check after few minutes.")
        else:
            self.create_attendance_from_excel(ws)

    
    def create_attendance_from_excel(self, ws):
        start_row = 6  
        max_row = ws.max_row
        max_col = ws.max_column

        try:
            dates = get_att_dates(self.from_date, self.to_date)
        except Exception as e:
            frappe.log_error("failed to get dates", "Attendance Upload")
            return

        usable_col_end = max_col - 4
        actual_cols = usable_col_end - 4 
        expected_cols = len(dates)

        if expected_cols != actual_cols:
            frappe.log_error(
                f"Column mismatch: expected {expected_cols} date columns for period {self.from_date} to {self.to_date}, but found {actual_cols} in Excel.",
                "Attendance Upload"
            )
            cols_to_process = min(expected_cols, actual_cols)
        else:
            cols_to_process = expected_cols

        row = start_row
        while row <= max_row:
            emp_code = ws.cell(row=row, column=2).value
            emp_name = ws.cell(row=row, column=3).value

            if not emp_code:
                row += 2
                continue
            
            b_count = ws.cell(row=row, column=max_col - 3).value or 0
            lunch = ws.cell(row=row, column=max_col - 2).value or 0
            dinner = ws.cell(row=row, column=max_col - 1).value or 0
            mobile_allowance = ws.cell(row=row, column=max_col).value or 0
            emp_status=frappe.db.get_value("Employee",{'name':emp_code},['status'])
            
            present_count = 0
            rd_count =0
            absent_count =0
            holiday_count = 0
            ww_count =0
            worked_days = 0
            total_ww_days =0
            total_hh_days =0
            for idx in range(cols_to_process):
                attendance_date = dates[idx]
                doj=frappe.db.get_value("Employee",{'name':emp_code},['date_of_joining'])
                rel=frappe.db.get_value("Employee",{'name':emp_code},['relieving_date'])
               
                if emp_status=='Active':
                    if getdate(attendance_date) < getdate(doj):
                        continue
                else:
                    if getdate(attendance_date) > getdate(rel):
                        continue
                col = 5 + idx 
                status = ws.cell(row=row, column=col).value
                ot = ws.cell(row=row + 1, column=col).value
                status = (str(status).strip().upper() if status else "A")
                ot = float(ot) if ot not in (None, '') else 0.0
                if status == "P":
                    att_status = "Present"
                    present_count +=1
                    rd_status = 0
                elif status == "HD":
                    att_status = "Half Day"
                    rd_status = 0
                    present_count +=0.5
                elif status == "RD":
                    att_status = "Absent"
                    rd_status = 1
                    rd_count +=1
                else:
                    att_status = "Absent"
                    rd_status = 0
                holiday_list = frappe.db.get_value('Employee', emp_code, 'holiday_list')
                if not holiday_list:
                    holiday_list = frappe.db.get_value('Company', self.company, 'default_holiday_list')
                if holiday_list and att_status !='Present' and rd_status ==0:
                    if check_holiday(attendance_date,holiday_list) =='WO':
                        if att_status == 'Half Day':
                            ww_count +=1
                        else:
                            ww_count +=0.5
                        total_ww_days +=1
                    elif check_holiday(attendance_date,holiday_list) =='HH':
                        if att_status == 'Half Day':
                            holiday_count +=1
                        else:
                            holiday_count +=0.5
                        total_hh_days +=1
                    else:
                        if att_status == 'Half Day':
                            absent_count +=1
                        else:
                            absent_count +=0.5


                if frappe.db.exists("Attendance", {
                    "employee": emp_code,
                    "attendance_date": attendance_date,
                    "docstatus": ["!=", 2]
                }):
                    try:
                        existing_att = frappe.get_doc("Attendance", {
                            "employee": emp_code,
                            "attendance_date": attendance_date
                        })
                        if existing_att.docstatus == 0:
                            existing_att.status = att_status
                            existing_att.custom_rest_day = rd_status
                            existing_att.custom_overtime_hours = ot
                            existing_att.save(ignore_permissions=True)
                            existing_att.submit()
                            frappe.db.commit()
                        else:
                            continue
                    except Exception as e:
                        frappe.log_error(
                            f"Failed to update existing attendance for {emp_code} on {attendance_date}: {str(e)}",
                            "Attendance Upload"
                        )
                else:
                    try:
                        att = frappe.new_doc("Attendance")
                        att.employee = emp_code
                        att.employee_name = emp_name
                        att.attendance_date = attendance_date
                        att.custom_upload_attendance = self.name
                        att.custom_overtime_hours = ot
                        att.status = att_status
                        att.custom_rest_day = rd_status
                        att.insert(ignore_permissions=True)
                        att.submit()
                        frappe.db.commit()
                    except Exception as e:
                        frappe.log_error(
                            f"Error creating attendance for {emp_code} on {attendance_date.strftime('%d-%m-%Y')}: {str(e)}",
                            "Attendance Upload"
                        )
            row += 2


            register_name = frappe.db.get_value(
                "Attendance and OT Register",
                {
                    'from_date': ('<=', self.to_date),
                    'to_date': ('>=', self.from_date),
                    'employee': emp_code,
                    'docstatus':['!=',2]
                },
                'name'
            )
            worked_days = present_count + rd_count + ww_count + holiday_count
            if register_name:
                try:
                    register_doc = frappe.get_doc("Attendance and OT Register", register_name)
                    register_doc.breakfast = float(b_count)
                    register_doc.lunch = float(lunch)
                    register_doc.dinner = float(dinner)
                    register_doc.mobile_allow = float(mobile_allowance)
                    register_doc.attendance_upload=self.name
                    register_doc.rest_days = rd_count
                    register_doc.present_days = present_count
                    register_doc.absent_days = absent_count
                    register_doc.total_weekly_holidays = total_ww_days
                    register_doc.holidays = total_hh_days
                    register_doc.no_of_days_worked = worked_days
                    register_doc.save(ignore_permissions=True)
                    frappe.db.commit()
                except Exception as e:
                    frappe.log_error(
                        f"Failed to update 'Attendance and OT Register' for {emp_code}: {str(e)}",
                        "Attendance Upload"
                    )
@frappe.whitelist()
def process_attendance_from_excel_job(docname):
    doc = frappe.get_doc("Upload Employee Attendance", docname)

    file_url = frappe.db.get_value(
        "File",
        {"attached_to_doctype": "Upload Employee Attendance", "attached_to_name": doc.name},
        "file_url"
    )

    if not file_url:
        frappe.log_error("No file found", "Attendance Upload Background Job")
        return

    try:
        in_memory_file = download_external_file_url(file_url)
        wb = openpyxl.load_workbook(in_memory_file)
        ws = wb.active
        doc.create_attendance_from_excel(ws)
    except Exception as e:
        frappe.log_error(f"Failed to process attendance in background: {str(e)}", "Attendance Upload")


@frappe.whitelist()
def get_att_dates(from_date, to_date):
        no_of_days = date_diff(add_days(to_date, 1), from_date)
        dates = [add_days(from_date, i) for i in range(no_of_days)]
        return dates

def download_external_file_url(file_url):
    path = frappe.get_site_path("public", file_url.replace("/files/", ""))
    with open(path, "rb") as f:
        return BytesIO(f.read())


def get_employee_count(ws):
    # Count how many rows contain employee codes (assuming every 2nd row is OT)
    return sum(
        1 for r in range(6, ws.max_row + 1, 2)
        if ws.cell(row=r, column=2).value
    )

from frappe.utils import get_url
@frappe.whitelist()
def download_external_file_url(file_url):
    if not file_url.startswith("http"):
        file_url = get_url() + file_url
    response = requests.get(file_url, stream=True)
    if response.status_code != 200:
        frappe.throw(_("Failed to download file from external storage."))

    return BytesIO(response.content)

@frappe.whitelist()
def get_template(from_date, to_date, department=None, designation=None, site_location=None, name=None):
    filename = 'Attendance Template'
    test = build_xlsx_response(filename)

@frappe.whitelist()
def build_xlsx_response(filename):
    xlsx_file = make_xlsx(filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file.getvalue()
    frappe.response['type'] = 'binary'

@frappe.whitelist()
def make_xlsx(data, sheet_name=None, wb=None, column_widths=None):
    args = frappe.local.form_dict
    column_widths = column_widths or []
    if wb is None:
        wb = openpyxl.Workbook()
    ws = wb.create_sheet(sheet_name, 0)

    dates = get_dates(args.from_date, args.to_date)
    comp=frappe.db.get_value("Upload Employee Attendance",{'name':args.name},['company'])
    header1=[comp]
    ws.append(header1)
    site_location=frappe.db.get_value("Upload Employee Attendance",{'name':args.name},['site_location'])
    if not site_location:
        header12=[]
    else:
        header12=[site_location]
    ws.append(header12)
    from_date_str = datetime.strptime(args.from_date, '%Y-%m-%d').strftime('%d/%m/%Y')
    to_date_str = datetime.strptime(args.to_date, '%Y-%m-%d').strftime('%d/%m/%Y')
    date_str=f"TIME SHEET {from_date_str} to {to_date_str}"
    header2=[date_str]
    ws.append(header2)
    header3 = ['SI No.','Emp. Code','Employee Name','Designation']
    header3.extend([d[0] for d in dates])  
    header3.extend(['Food','','','Mobile Allowance'])
    header4 = ['', '', '', '']  
    header4.extend([d[1] for d in dates]) 
    header4.extend(['B','L','D'])
    ws.append(header3)
    ws.append(header4)

    emp_data = get_employees(args)
    row_num = 1
    start_row = 6
    for emp in emp_data:
        emp_row = [row_num,emp.get("name"),emp.get("employee_name"),emp.get("designation")]
        empty_line=[]
        empty_line.extend([''] * len(dates)) 

        ws.append(emp_row)
        ws.append(empty_line)
        for col in range(1, 5):
            ws.merge_cells(start_row=start_row, start_column=col,end_row=start_row + 1, end_column=col)
        row_num += 1
        start_row+=2
    
    merge_length=date_diff(args.to_date,args.from_date)
    merge_length+=5
    
    if not site_location:
        ws.merge_cells(start_row=1, start_column=1, end_row=2, end_column=merge_length+4)
    else:
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=merge_length+4)
        ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=merge_length+4)
    ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=merge_length+4)
    ws.merge_cells(start_row=4, start_column=merge_length+1, end_row=4, end_column=merge_length+3)
    for i in range(1,5):
        ws.merge_cells(start_row=4,start_column=i,end_row=5,end_column=i)
    header_fill = PatternFill(start_color="E6B8B7", end_color="E6B8B7", fill_type="solid")
    bold_font = Font(bold=True)
    center_alignment = Alignment(horizontal="center", vertical="center")
    for row in [4, 5]:
        for col in range(1, len(header3) + 1):
            cell = ws.cell(row=row, column=col)
            cell.fill = header_fill
            cell.font = bold_font
            cell.alignment = center_alignment
    friday_fill = PatternFill(start_color='92D050', end_color='92D050', fill_type="solid")  
    for col_idx, cell in enumerate(ws[5], start=1): 
        if cell.value == 'Fr':
            ws.cell(row=5, column=col_idx).fill = friday_fill
    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 43
    ws.column_dimensions['D'].width = 18
    last_col_index = ws.max_column
    last_col_letter = get_column_letter(last_col_index)
    ws.column_dimensions[last_col_letter].width = 18
    for i in range(1, 4): 
        col_letter = get_column_letter(last_col_index - i)
        ws.column_dimensions[col_letter].width = 6
    for row in range(4, ws.max_row + 1, 2):
        ws.merge_cells(
            start_row=row,
            start_column=last_col_index,
            end_row=row + 1,
            end_column=last_col_index
        )
    for col_offset in range(1, 4):  # 1 to 3
        col_idx = last_col_index - col_offset
        for row in range(6, ws.max_row + 1, 2):
            ws.merge_cells(
                start_row=row,
                start_column=col_idx,
                end_row=row + 1,
                end_column=col_idx
            )

    border = Border(left=Side(border_style='thin', color='000000'),
        right=Side(border_style='thin', color='000000'),
        top=Side(border_style='thin', color='000000'),
        bottom=Side(border_style='thin', color='000000'))

    for rows in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1,max_col=ws.max_column):
        for cell in rows:
            cell.border = border
    for rows in ws.iter_rows(min_row=1, max_row=3, min_col=1,max_col=ws.max_column):
        for cell in rows:
            cell.alignment = center_alignment
            cell.font = bold_font
    for col in range(5, merge_length + 1):
        col_letter = get_column_letter(col)
        ws.column_dimensions[col_letter].width = 6

    xlsx_file=BytesIO()
    wb.save(xlsx_file)
    return xlsx_file





def get_dates(from_date, to_date):
    start_date = datetime.strptime(from_date, "%Y-%m-%d")
    end_date = datetime.strptime(to_date, "%Y-%m-%d")
    delta = end_date - start_date
    days = []
    for i in range(delta.days + 1):
        date = start_date + timedelta(days=i)
        day_num = date.strftime("%d")  
        weekday = date.strftime("%a")[:2]
        days.append((day_num, weekday))
    return days


def get_employees(args):
    filters = {'status': 'Active'}
    dept=frappe.db.get_value("Upload Employee Attendance",{'name':args.name},['department'])
    desi=frappe.db.get_value("Upload Employee Attendance",{'name':args.name},['designation'])
    comp=frappe.db.get_value("Upload Employee Attendance",{'name':args.name},['company'])
    location = frappe.db.get_value("Upload Employee Attendance",{'name':args.name},['site_location'])
    if args.department and args.department!='None':
        if dept:
            filters['department'] = dept
    if args.designation and args.designation!='None':
        if desi:
            filters['designation'] = desi
    if args.company and args.company!='None':
        if comp:
            filters['company'] = comp
    if args.site_location and args.site_location!='None':
        if location:
            filters['custom_site_location'] = location
    
    import re

    employees = frappe.db.get_all(
        'Employee',
        filters=filters,
        fields=['name', 'employee_name', 'designation']
    )

    def sort_key(emp):
        code = emp['name']
        match = re.match(r"([A-Za-z]+)(\d*)", code)

        prefix = match.group(1)
        number = match.group(2)

        number = int(number) if number.isdigit() else 0

        return (prefix, number)

    employees = sorted(employees, key=sort_key)
    
    
    return employees

import frappe

@frappe.whitelist()
def cancel_attendance_records(docname):
    att_list = frappe.db.get_all("Attendance", {
        'custom_upload_attendance': docname,
        'docstatus': 1
    }, ['name'])

    for a in att_list:
        try:
            att_doc = frappe.get_doc('Attendance', a.name)
            att_doc.cancel()
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"{a.name}: {e}", "Upload Employee Attendance Cancel")

    reg_list = frappe.db.get_all("Attendance and OT Register", {
        'attendance_upload': docname
    }, ['name'])

    for r in reg_list:
        try:
            reg_doc = frappe.get_doc('Attendance and OT Register', r.name)
            reg_doc.breakfast = 0
            reg_doc.lunch = 0
            reg_doc.dinner = 0
            reg_doc.mobile_allow = 0
            reg_doc.attendance_upload = docname
            reg_doc.save(ignore_permissions=True)
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"{r.name}: {e}", "Upload Employee Attendance Cancel")

@frappe.whitelist()
def check_holiday(date, holiday_list):
    query = """
        SELECT `tabHoliday`.holiday_date, `tabHoliday`.weekly_off
        FROM `tabHoliday List`
        LEFT JOIN `tabHoliday` ON `tabHoliday`.parent = `tabHoliday List`.name
        WHERE `tabHoliday List`.name = %s AND holiday_date = %s
    """
    holiday = frappe.db.sql(query, (holiday_list, date), as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WO"
        else:
            return "HO"
    return None
