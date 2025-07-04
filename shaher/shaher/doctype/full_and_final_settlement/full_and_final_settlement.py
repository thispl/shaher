# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class FullandFinalSettlement(Document):
	pass
	
@frappe.whitelist()
def get_years(employee):
	emp = frappe.get_doc("Employee", employee)
	doj = emp.date_of_joining
	dor = emp.relieving_date
	if doj and dor:
		diff_in_days = (dor - doj).days
		years = round(diff_in_days / 365.0, 2)
	else:
		years=0
	return years

import frappe
from frappe.utils import getdate

@frappe.whitelist()
def calculate_balance_amount(employee, from_date, to_date):
    from_date = getdate(from_date)
    to_date = getdate(to_date)
    
    diff_days = (to_date - from_date).days
    
    if diff_days < 0:
        frappe.throw("To date cannot be earlier than from date.")    
    employee_data = frappe.get_doc("Employee", employee)    
    basic_salary =employee_data.custom_basic
    special_allowance = employee_data.custom_special_allowance
    balance_amount = ((basic_salary + special_allowance) / 31) * diff_days
    
    return balance_amount