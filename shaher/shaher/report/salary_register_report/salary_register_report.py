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
	earnings = frappe.get_all("Salary Component", {'type': "Earning",'custom_sequence_id':['!=',0]}, ['name'], order_by='custom_sequence_id ASC')
	deductions = frappe.get_all("Salary Component", {'type': "Deduction",'custom_sequence_id':['!=',0]}, ['name'], order_by='custom_sequence_id ASC')
	columns = [
		_("Employee") + ":Link/Employee:200",
		_("Visa No") + ":Data:200",
		_("Employee Name") + ":Data:200",
		_("Department") + ":Link/Department:100",
		_("Days") + ":Data:100",
		_("OT Hours") + ":Data:100",
		_("Basic") + ":Currency:120",
		_("Earned Basic") + ":Currency:120"
	]
	for e in earnings:
		if e.name != "Basic":
			columns.append(_(e.name) + ":Currency:150")
	columns += [
		_("BR Earning") + ":Currency:120",
		_("Total Earning") + ":Currency:120"
	]
	for d in deductions:
		columns.append(_(d.name) + ":Currency:200")
	columns += [
		_("BR Deductions") + ":Currency:120",
		_("Total Deductions") + ":Currency:120",
		_("Net Pay") + ":Currency:120",
		_("Bank Account") + ":Data:150",
		_("Bank Swift Code") + ":Data:150",
		_("Bank Branch") + ":Data:150",
		_("Bank Account No") + ":Data:150",
		_("Net Pay") + ":Currency:120"
	]
	return columns

def get_data(filters):
	start_date = filters.get('from_date')
	end_date = filters.get('to_date')
	earnings = frappe.get_all("Salary Component", {'type': "Earning",'custom_sequence_id':['!=',0]}, ['name'], order_by='custom_sequence_id ASC')
	deductions = frappe.get_all("Salary Component", {'type': "Deduction",'custom_sequence_id':['!=',0]}, ['name'], order_by='custom_sequence_id ASC')
	data = []
	salary_slips = get_salary_slips(filters)
	for s in salary_slips:
		visa_no = frappe.db.get_value('Employee',{'name':s['employee']},['custom_visa_number']) or ''
		basic = frappe.db.get_value('Employee',{'name':s['employee']},['custom_basic']) or 0.0
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
		for e in earnings:
			earnings_details[e.name] = frappe.get_value("Salary Detail", {'parent': s['name'], 'salary_component': e.name}, 'amount') or 0.0

		for d in deductions:
			deductions_details[d.name] = frappe.get_value("Salary Detail", {'parent': s['name'], 'salary_component': d.name}, 'amount') or 0.0

		br_earnings =0.0
		br_deductions =0.0
		for e in earnings:
			if e.name != 'Basic':
				earning = earnings_details.get(e.name, 0.0)
				earning_values.append(earning)
				br_earnings += earnings_details.get(e.name, 0.0)
		for d in deductions:
			if d.name != 'Public Authority for Social Insurance':
				deduction =deductions_details.get(d.name, 0.0)
				deduction_values.append(deduction)
				br_deductions += deductions_details.get(d.name, 0.0)


		data.append([
			s['employee'],
			visa_no,
			s['employee_name'],
			s['department'],
			s['payment_days'],
			s['custom_overtime_hours'],
			basic,
			earnings_details.get('Basic', 0.0),
			*earning_values,
			br_earnings,
			s['gross_pay'],
			deductions_details.get('Public Authority for Social Insurance', 0.0),
			*deduction_values,
			br_deductions,
			s['total_deduction'],
			s['net_pay'],
			bank,
			iban,
			branch_name,
			bank_ac_no,
			s['net_pay']
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
	if filters.get('department'):
		conditions.append("department = %s")
		values.append(filters.get('department'))
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