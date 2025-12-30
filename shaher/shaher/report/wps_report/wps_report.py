# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from datetime import datetime
from frappe.utils.data import add_days, add_years, today,getdate

def execute(filters=None):
	data = get_data(filters)
	columns = get_columns()
	return columns, data

def get_columns():
	columns = [
		_("Employment Type") + ":Link/Employment Type:150",
		_("Employee") + ":Link/Employee:200",
		_("Employee Name") + ":Data:200",
		_("Bank Name") + ":Data:150",
		_("Account Number") + ":Data:150",
		_("Salary Frequency") + ":Data:150",
		_("No.of Working Days") + ":Data:180",
		_("Extra Hours") + ":Data:150",
		_("Basic Salary") + ":Currency:120",
		_("Extra Income") + ":Currency:160",
		_("Deductions") + ":Currency:120",
		_("Public Authority for Social Insurance") + ":Currency:250",
		_("Net Pay") + ":Currency:120",
		_("Notes / Comments") + ":Data:150",
		_("Status") + ":Data:150",
	]
	return columns

def get_data(filters):
	# frappe.errprint(filters)
	start_date = filters.get('from_date')
	end_date = filters.get('to_date')
	earnings = frappe.get_all("Salary Component", {'type': "Earning",'custom_sequence_id':['!=',0]}, ['name'], order_by='custom_sequence_id ASC')
	deductions = frappe.get_all("Salary Component", {'type': "Deduction",'custom_sequence_id':['!=',0]}, ['name'], order_by='custom_sequence_id ASC')
	data = []
	salary_slips = get_salary_slips(filters)
	for s in salary_slips:
		bank_ac_no = frappe.db.get_value('Employee',{'name':s['employee']},['bank_ac_no']) or ''
		bank = frappe.db.get_value('Employee',{'name':s['employee']},['bank_name']) or ''
		earnings_details = {}
		deductions_details = {}
		joining_date, relieving_date = frappe.get_cached_value(
			"Employee", s['employee'], ["date_of_joining", "relieving_date"]
		)
		# ot_hours = get_ot_hours(s['employee'],start_date, end_date) or 0.0
		# if relieving_date and (getdate(start_date) <= relieving_date < getdate(end_date)):
		# 	ot_hours = get_ot_hours(s['employee'], start_date, relieving_date) or 0.0
		# if joining_date and (getdate(start_date) < joining_date <= getdate(end_date)):
		# 	ot_hours = get_ot_hours(s['employee'], joining_date, end_date)  or 0.0
		for e in earnings:
			earnings_details[e.name] = frappe.get_value("Salary Detail", {'parent': s['name'], 'salary_component': e.name}, 'amount') or 0.0
		for d in deductions:
			deductions_details[d.name] = frappe.get_value("Salary Detail", {'parent': s['name'], 'salary_component': d.name}, 'amount') or 0.0
		br_earnings =0.0
		br_deductions =0.0
		for e in earnings:
			if e.name != 'Basic':
				br_earnings += earnings_details.get(e.name, 0.0)
		for d in deductions:
			if d.name != 'Public Authority for Social Insurance':
				br_deductions += deductions_details.get(d.name, 0.0)

		data.append([
			s['custom_employment_type'],
			s['employee'],
			s['employee_name'],
			bank,
			bank_ac_no,
			s['payroll_frequency'],
			s['payment_days'],
			s['custom_overtime_hours'],
			earnings_details.get('Basic', 0.0),
			br_earnings,
			br_deductions,
			deductions_details.get('Public Authority for Social Insurance', 0.0),
			s['net_pay'],
			'',
			'Completed' if s['status'] =='Submitted' else 'Processing' 
		])

	return data

def get_salary_slips(filters):
	conditions = ["docstatus != 2"]
	values = []
	if filters.get('from_date') and filters.get('to_date'):
		conditions.append("start_date >= %s AND end_date <= %s")
		values.extend([filters.get('from_date'), filters.get('to_date')])
	elif filters.get('from_date'):
		conditions.append("start_date >= %s")
		values.append(filters.get('from_date'))
	elif filters.get('to_date'):
		conditions.append("end_date <= %s")
		values.append(filters.get('to_date'))
	if filters.get('company'):
		conditions.append("company = %s")
		values.append(filters.get('company'))
	if filters.get('employee'):
		conditions.append("employee = %s")
		values.append(filters.get('employee'))
	if filters.get('employment_type'):
		conditions.append("custom_employment_type = %s")
		values.append(filters.get('employment_type'))
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