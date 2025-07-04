# Copyright (c) 2024, TEAMPRO and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.styles import GradientFill, PatternFill
from six import BytesIO
import io  # Add this import to resolve the NameError

from datetime import datetime
from datetime import datetime, timedelta
from frappe.utils import (getdate, cint, add_months, date_diff, add_days, format_date,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from openpyxl.drawing.image import Image as xlImage
import requests




@frappe.whitelist()
def download():
    filename = 'Salary Register Reports.xlsx'
    build_xlsx_response(filename)

def make_xlsx(sheet_name=None):
    args = frappe.local.form_dict
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name if sheet_name else 'Sheet1'

    data = get_data(args)
    if not data:
        frappe.throw("No data available to generate the report.")

    earnings_count = frappe.db.count("Salary Component", {'type': "Earning"})
    deductions_count = frappe.db.count("Salary Component", {'type': "Deduction"})
    total_column = 15 + earnings_count + deductions_count

    for row in data:
        if not isinstance(row, (list, tuple)):
            row = [row]
        ws.append(row)
    for row in range(1,6):
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=total_column)
    for col in range(1,total_column+1):
        ws.merge_cells(start_row=6, start_column=col, end_row=7, end_column=col)
    ws.merge_cells(start_row=ws.max_row, start_column=1, end_row=ws.max_row, end_column=5)
    apply_styles(ws,total_column)
    set_column_widths(ws,total_column)

    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    xlsx_file.seek(0)
    return xlsx_file


def apply_styles(ws, total_column):
    align_center = Alignment(horizontal='center', vertical='center', wrap_text=True)
    align_right = Alignment(horizontal='right', vertical='top', wrap_text=True)
    align_left = Alignment(horizontal='left', vertical='top', wrap_text=True)

    header_font = Font(bold=True, size=14,color="FFFFFF")
    sub_header_font = Font(bold=True, size=10, color="FFFFFF")
    text_font_data = Font(bold=False, size=9)

    border = Border(
        left=Side(border_style='thin'),
        right=Side(border_style='thin'),
        top=Side(border_style='thin'),
        bottom=Side(border_style='thin')
    )
    # Green

    header_fill = PatternFill(start_color="FF808000", end_color="FF808000", fill_type="solid")
    header_fill_1 = PatternFill(start_color="FF666699", end_color="FF666699", fill_type="solid")

    for row in ws.iter_rows(min_row=1, max_row=3, min_col=1, max_col=total_column):
        for cell in row:
            cell.font = header_font
            cell.alignment = align_center
            # cell.border = border
            cell.fill = header_fill
    for row in ws.iter_rows(min_row=6, max_row=7, min_col=1, max_col=total_column):
        for cell in row:
            cell.font = sub_header_font
            cell.alignment = align_center
            cell.border = border
            cell.fill = header_fill_1

    for row in ws.iter_rows(min_row=8, max_row=ws.max_row, min_col=1, max_col=total_column):
        for cell in row:
            cell.font = text_font_data
            cell.alignment = align_center
            cell.border = border
    for row in ws.iter_rows(min_row=ws.max_row, max_row=ws.max_row, min_col=1, max_col=total_column):
        for cell in row:
            cell.font = sub_header_font
            cell.alignment = align_center
            cell.border = border
            cell.fill = header_fill_1

def set_column_widths(ws,total_column):
   # total_column = total number of columns in your report
    column_widths = [10, 15, 15, 20] + [10] * (total_column - 7) + [20, 20, 20, 20,10]

    for i, width in enumerate(column_widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width
    row_heights = [20, 20, 20,20,20,40] + [20] * (ws.max_row - 1) +[30]*1
    for i, height in enumerate(row_heights, start=1):
        ws.row_dimensions[i].height = height

def build_xlsx_response(filename):
    xlsx_file = make_xlsx(sheet_name=filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file.getvalue()
    frappe.response['type'] = 'binary'
      
def get_data(args):
    args = frappe.local.form_dict
    start_date = args.get('from_date')
    end_date = args.get('to_date')
    
    company = args.get('company') or 'All Companies'
    formatted_date =''
    if args.get('from_date'):
        formatted_date = frappe.utils.formatdate(start_date, 'dd-mm-yyyy')
    earnings = frappe.get_all("Salary Component", {'type': "Earning",'custom_sequence_id':['!=',0]}, ['name'], order_by='custom_sequence_id ASC')
    deductions = frappe.get_all("Salary Component", {'type': "Deduction",'custom_sequence_id':['!=',0]}, ['name'], order_by='custom_sequence_id ASC')

    earnings_count = len(earnings)
    deductions_count = len(deductions)
    total_column = 17 + earnings_count + deductions_count

    data = [
        [company] + [""] *total_column,
        ["Salary As of " + formatted_date],
        [""] *total_column,
        [""] *total_column,
        [""] *total_column,
        ["S.No", "Employee", "Visa No", "Name", "Div", "Days", "OT Hours", "Basic", 
         "Earned Basic"]
        + [e.name for e in earnings if e.name != 'Basic']
        + ["BR Earning"]
        + ["Total"]
        + [d.name for d in deductions]
        + ["BR Deductions","Total Deductions", "Net Pay","Bank Account","Bank Swift Code","Bank Branch","Bank Account No","Net Pay"],
        [""]
    ]

    row = []
    index = 0
    salary_slips = get_salary_slips(args)
    total = {
        "payment_days": 0.0,
        "br_earnings": 0.0,
        "br_deductions":0.0,
        "gross_pay": 0.0,
        "total_deduction": 0.0,
        "net_pay": 0.0,
    }
    for e in earnings:
        total[e.name] = 0.0
    for d in deductions:
        total[d.name] = 0.0
    total_row =[]
    total_basic =0
    total_ot_hours =0
    
    for s in salary_slips:
        
        index += 1
        
        visa_no = frappe.db.get_value('Employee',{'name':s['employee']},['custom_visa_number']) or ''
        basic = frappe.db.get_value('Employee',{'name':s['employee']},['custom_basic']) or 0.0
        total_basic +=basic
        division = frappe.db.get_value('Employee',{'name':s['employee']},['grade']) or ''
        bank_ac_no = frappe.db.get_value('Employee',{'name':s['employee']},['bank_ac_no']) or ''
        bank = frappe.db.get_value('Employee',{'name':s['employee']},['bank_name']) or ''
        iban = frappe.db.get_value('Employee',{'name':s['employee']},['iban']) or ''
        branch_name = frappe.db.get_value('Employee',{'name':s['employee']},['custom_branch_name']) or ''
        earnings_details = {}
        deductions_details = {}
        earning_values =[]
        deduction_values =[]
        joining_date, relieving_date = frappe.get_cached_value(
            "Employee", s['employee'], ["date_of_joining", "relieving_date"]
        )
        ot_hours = get_ot_hours(s['employee'],start_date, end_date) or 0.0
        if relieving_date and (getdate(start_date) <= relieving_date < getdate(end_date)):
            ot_hours = get_ot_hours(s['employee'], start_date, relieving_date) or 0.0
        if joining_date and (getdate(start_date) < joining_date <= getdate(end_date)):
            ot_hours = get_ot_hours(s['employee'], joining_date, end_date)  or 0.0
        total_ot_hours +=ot_hours     
        for e in earnings:
            earnings_details[e.name] = frappe.get_value("Salary Detail", {'parent': s['name'], 'salary_component': e.name}, 'amount') or 0.0
            total[e.name] += earnings_details[e.name]

        for d in deductions:
            deductions_details[d.name] = frappe.get_value("Salary Detail", {'parent': s['name'], 'salary_component': d.name}, 'amount') or 0.0
            total[d.name] += deductions_details[d.name]

        br_earnings =0.0
        br_deductions =0.0
        for e in earnings:
            if e.name != 'Basic':
                earning = format_currency(earnings_details.get(e.name, 0.0))
                earning_values.append(earning)
                br_earnings += earnings_details.get(e.name, 0.0)
        
        for d in deductions:
            deduction =format_currency(deductions_details.get(d.name, 0.0))
            deduction_values.append(deduction)
            br_deductions += deductions_details.get(d.name, 0.0)

        total['br_earnings'] += br_earnings
        total['payment_days'] += s['payment_days']
        total['br_deductions'] += br_deductions
        total['gross_pay'] += s['gross_pay']
        total['total_deduction'] += s['total_deduction']
        total['net_pay'] += s['net_pay']
        row = [
            index, s['employee'], visa_no, s['employee_name'], division, s['payment_days'],
            ot_hours, format_currency(basic), format_currency(earnings_details.get('Basic', 0.0))
        ] + earning_values + [
            format_currency(br_earnings), format_currency(s['gross_pay'])
        ] + deduction_values + [
            format_currency(br_deductions), format_currency(s['total_deduction']), format_currency(s['net_pay']), bank, iban, branch_name, bank_ac_no, format_currency(s['net_pay'])
        ]


        data.append(row)

        total_row = (
        ["TOTAL", "", "", ""] +
        [total["payment_days"], "", "", total_basic,format_currency(total.get("Basic", 0.0))] +
        [format_currency(total.get(e.name, 0.0)) for e in earnings if e.name != 'Basic'] +
        [format_currency(total["br_earnings"]), format_currency(total["gross_pay"])] +
        [format_currency(total.get(d.name, 0.0)) for d in deductions] +
        [format_currency(total["br_deductions"]), format_currency(total["total_deduction"]), format_currency(total["net_pay"]), "", "", "", "", format_currency(total["net_pay"])]
    )
    data.append(total_row)
    return data


def format_currency(value):
    if value is None:
        return "0"
    
    number_str = str(int(value))
    
    if len(number_str) > 3:
        last_three = number_str[-3:]  
        other_digits = number_str[:-3] 
        
        formatted_other = []
        while len(other_digits) > 2:
            formatted_other.append(other_digits[-2:])
            other_digits = other_digits[:-2]
        if other_digits:
            formatted_other.append(other_digits)        
        formatted_other.reverse()
        formatted_number = ','.join(formatted_other) + ',' + last_three
    else:
        formatted_number = number_str
    
    return formatted_number


def get_salary_slips(args):
    args = frappe.local.form_dict
    conditions = ["docstatus != 2"]
    values = []
    if args.get('from_date') and args.get('to_date'):
        conditions.append("start_date >= %s AND end_date <= %s")
        values.extend([args.get('from_date'), args.get('to_date')])
    elif args.get('from_date'):
        conditions.append("start_date >= %s")
        values.append(args.get('from_date'))
    elif args.get('to_date'):
        conditions.append("end_date <= %s")
        values.append(args.get('to_date'))
    if args.get('company'):
        conditions.append("company = %s")
        values.append(args.get('company'))
    condition_str = " AND ".join(conditions)
    salary_slips = frappe.db.sql(f"""
        SELECT * FROM `tabSalary Slip`
        WHERE {condition_str}
        ORDER BY employee
    """, values, as_dict=True)

    return salary_slips


def get_ot_hours(employee, from_date, to_date):

    result = frappe.db.sql("""
        SELECT SUM(custom_overtime_hours) AS ot
        FROM `tabAttendance`
        WHERE employee = %s 
        AND attendance_date BETWEEN %s AND %s 
        AND docstatus != 2
    """, (employee, from_date, to_date), as_dict=True)

    return result[0].get('ot', 0.0) if result else 0.0

