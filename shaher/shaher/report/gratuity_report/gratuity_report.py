# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import date_diff,today,cstr
from dateutil.relativedelta import relativedelta
import datetime
from datetime import date,timedelta
from frappe.utils import date_diff, add_months,today,add_days,add_years,nowdate,flt
import math


def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = calculate_gratuity(filters)
	return columns, data

def get_columns(filters):
	columns = []
	columns += [_("Employee ID") + ":Link/Employee:180", _("Employee Name") + ":Data/:250",_("DoJ") + ":Date/:120",_("Year of Service") + ":Data/:300",_("Total Gratuity") + ":Currency/:160",]
	return columns

def calculate_gratuity(filters):
	
	row = []
	data = []
	employees = frappe.get_all('Employee',{'status':'Active'},['name','employee_name','date_of_joining'],order_by='name ASC')
	for emp in employees:
		from datetime import datetime
		from dateutil import relativedelta
		date_2 = datetime.now()
		absent_days = 0
		absent_days += frappe.db.get_value("Employee",{"name":emp.name},['custom_absent_days'])
			
		attendance = frappe.get_all(
		"Attendance",
			filters={
				"employee": emp.name,
				"attendance_date": ["between", (emp.date_of_joining, nowdate())],
				"docstatus": ["=", 1],
				"leave_application":'' 
			},
			fields=["status"]
		)

		for i in attendance:
			if i.status =="Absent":
				absent_days +=1
			if i.status =="Half Day":
				absent_days+=0.5
		
		
		diff = relativedelta.relativedelta(date_2, emp.date_of_joining)
		yos = cstr(diff.years) + ' years, ' + cstr(diff.months) +' months and ' + cstr(diff.days) + ' days'
		basic_salary = frappe.db.get_value('Employee',emp.name,'custom_basic')
		current_yoe_days = date_diff(nowdate(),emp.date_of_joining) + 1
		current_yoe = round((current_yoe_days / 365),3)
		if(1 <= diff.years <= 3):
			# total_gratuity = (basic_salary * .5) * diff.years
			gratuity_per_year = (basic_salary * .5)
			total_gratuity = math.ceil(gratuity_per_year/365*(current_yoe_days-absent_days))
			row = [emp.name,emp.employee_name,emp.date_of_joining,yos,total_gratuity]
			data.append(row)
			
		elif(diff.years > 3):
			gratuity_per_year = basic_salary
			# total_gratuity = basic_salary * diff.years
			total_gratuity = math.ceil(gratuity_per_year/365*(current_yoe_days-absent_days))
			row = [emp.name,emp.employee_name,emp.date_of_joining,yos,total_gratuity]
			data.append(row)

	return data