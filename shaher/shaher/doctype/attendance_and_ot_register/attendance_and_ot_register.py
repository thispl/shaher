# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import calendar
from datetime import datetime
from frappe.utils import getdate, date_diff, add_days
from frappe import _, msgprint
class AttendanceandOTRegister(Document):
	def validate(self):
		# if self.name:
		# 	exist_doc = frappe.db.get_value('Attendance and OT Register',{'name': ['!=', self.name],'from_date': ['<=', self.to_date],'to_date': ['>=', self.from_date],'employee': self.employee,'docstatus': ["!=", 2]},['name'])
		# 	if exist_doc:
		# 		frappe.throw(
		# 			f'Attendance and OT Register already exists for this Period: '
		# 			f'<a href="/app/attendance-and-ot-register/{exist_doc}" target="_blank">{exist_doc}</a>.'
		# 		)
		if self.from_date and self.to_date and self.to_date < self.from_date:
			frappe.throw("To Date cannot be earlier than From Date.")

		date_of_joining = frappe.db.get_value('Employee', {'name': self.employee}, 'date_of_joining')
		relieving_date = frappe.db.get_value('Employee', {'name': self.employee}, 'relieving_date')
		if not frappe.db.get_value('Employee', {'name': self.employee}, 'name'):
			frappe.throw(_("Employee {0} does not exist").format(frappe.bold(self.employee_name)))

		if not date_of_joining:
			frappe.throw(
				_("Please set the Date Of Joining for employee {0}").format(frappe.bold(self.employee_name))
			)
		
		# if date_diff(getdate(self.to_date), getdate(date_of_joining)) < 0:
		# 	frappe.throw(_("Cannot create Attendance and OT Register for Employee joining after Payroll Period"))

		if relieving_date and date_diff(getdate(relieving_date), getdate(self.from_date)) < 0:
			frappe.throw(_("Cannot create Attendance and OT Register for Employee who has left before Payroll Period"))

	def on_submit(self):
		salary_components=[]
		if self.food_allowance and self.food_allowance !=0:
			salary_components.append('Food Allowance')
		if self.salary_advance_deduction and self.salary_advance_deduction != 0.0:
			salary_components.append('Salary Advance')
		if self.other_earnings and self.other_earnings != 0.0:
			salary_components.append('Other Allowance')
		if self.other_deduction and self.other_deduction != 0.0:
			salary_components.append('Other Deductions')
		if (self.ot_hours and self.ot_hours != 0.0):
			salary_components.append('Normal Overtime Amount')
		if self.night_ot and self.night_ot != 0.0:
			salary_components.append('Night Overtime Amount')
		if self.wo_nh and self.wo_nh != 0.0:
			salary_components.append('Holiday Overtime Amount')


		

		for sal in salary_components:
			add_sal=frappe.new_doc("Additional Salary")
			add_sal.employee = self.employee
			add_sal.payroll_date = self.from_date
			add_sal.company = self.company
			add_sal.custom_attendance_and_ot_register = self.name
			if sal == 'Food Allowance':
				add_sal.salary_component = sal
				add_sal.amount = self.food_allowance
				add_sal.overwrite_salary_structure_amount = 1
			if sal == 'Salary Advance':
				add_sal.salary_component = sal
				add_sal.amount = self.salary_advance_deduction
			if sal == 'Other Allowance':
				add_sal.salary_component = sal
				add_sal.amount = self.other_earnings
			if sal == 'Other Deductions':
				add_sal.salary_component = sal
				add_sal.amount = self.other_deduction
			if sal in ['Holiday Overtime Amount','Normal Overtime Amount','Night Overtime Amount']:
				add_sal.salary_component = sal
				overtime_amount=0
				holiday_overtime_amount  =0
				night_overtime_amount =0
				basic = frappe.db.get_value("Employee",{'name':self.employee},"custom_basic")
				today = self.from_date
				year = getdate(today).year
				month = getdate(today).month

				
				if month == 1:
					previous_month = 12
					year -= 1
				else:
					previous_month = month - 1

				
				days_in_prev_month = calendar.monthrange(year, previous_month)[1]
				if self.company in ['ALPHA ENGINEERING & CONTRACTING LLC','TAKE OFF UNITED TRADING LLC']:
					days_in_prev_month =30
					if self.ot_hours:
						overtime_amount += (basic/days_in_prev_month/8)*1.25*self.ot_hours
					if self.night_ot:
						night_overtime_amount += (basic/days_in_prev_month/8)*1.5*self.night_ot
					if self.wo_nh:
						holiday_overtime_amount += (basic/days_in_prev_month/8)*2*self.wo_nh
				elif self.company =='THE PALACE HOTEL':
					days_in_prev_month =30
					if self.ot_hours:
						overtime_amount += (basic/days_in_prev_month/10)*1.25*self.ot_hours
					if self.night_ot:
						night_overtime_amount += (basic/days_in_prev_month/10)*1.5*self.night_ot
					if self.wo_nh:
						holiday_overtime_amount += (basic/days_in_prev_month/10)*2*self.wo_nh

				else:
					days_in_prev_month =30
					if self.ot_hours:
						# nationality = frappe.db.get_value('Employee',self.employee,'custom_nationality')
						# if nationality and nationality =='Oman' and self.company =="SHAHER UNITED TRADING & CONTRACTING COMPANY":
						# 	ot_rate =1
						# else:
						ot_rate =1.25
						overtime_amount += (basic/days_in_prev_month/8)*ot_rate*self.ot_hours
					if self.night_ot:
						night_overtime_amount += (basic/days_in_prev_month/8)*1.5*self.night_ot
					if self.wo_nh:
						holiday_overtime_amount += (basic/days_in_prev_month/8)*2*self.wo_nh
				if sal =="Holiday Overtime Amount":
					add_sal.amount = holiday_overtime_amount
				if sal =="Night Overtime Amount":
					add_sal.amount = night_overtime_amount
				if sal =="Normal Overtime Amount":
					add_sal.amount = overtime_amount
					
				
				
			add_sal.save(ignore_permissions=True)
			add_sal.submit()
	
	def on_cancel(self):
		add_sals=frappe.get_all("Additional Salary",{'custom_attendance_and_ot_register':self.name},['name'])
		if add_sals:
			for ads in add_sals:
				ad_sal = frappe.get_doc("Additional Salary",ads.name)
				ad_sal.cancel()
				ad_sal.delete()
	
	
	
