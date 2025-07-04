# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from dateutil.relativedelta import relativedelta
from frappe.utils import getdate, get_datetime
class EmployeeLoan(Document):
    def on_trash(self):
        for i in self.loan_details:
            if i.deducted==1:
                frappe.throw("Deductions already happened.Deletion not allowed.")
    def validate(self):
        doj=frappe.db.get_value("Employee",{'name':self.employee},['date_of_joining'])
        if getdate(doj)>getdate(self.date):
            frappe.throw("Loan cannot be given before Employee's joining date")
        if self.amount <= 0:
            frappe.throw("Loan amount cannot be 0")
        if self.count==0:
            frappe.throw("Count cannot be 0")
        amnt=0
        row=0
        from_dates = set()
        date_ranges=[]
        dedcount=0
        for i in self.loan_details:
            row+=1
            if i.deducted==1:
                dedcount+=1
            if i.deduction_amount:
                amnt+=i.deduction_amount
            
            if i.from_date < self.deduction_start_from and i.deducted==0:
                frappe.throw(f"Kindly check the date in row <b>{row}</b>.It cannot be less than Deduction start date")
            if i.from_date in from_dates:
                   frappe.throw(f"Duplicate Date found in row <b>{row}</b>: {i.from_date}. Please remove duplicates.")
            from_dates.add(i.from_date)
            date_ranges.append((i.from_date, i.to_date, row))
        for i in range(len(date_ranges)):
            for j in range(i + 1, len(date_ranges)):
                start1, end1, row1 = date_ranges[i]
                start2, end2, row2 = date_ranges[j]

                if start1 <= end2 and start2 <= end1:
                    frappe.throw(
                        f"Date ranges are overlapping between row <b>{row1}</b> and row <b>{row2}</b>."
                    )
        if self.amount!=amnt:
            frappe.throw("Loan Amount and Amount in deduction schedule are not matching.Kindly Check Once.")
        # if self.date_changed == 1 and self.reference:
        #     ded=0
        #     ref_doc = frappe.get_doc("Employee Loan", self.reference)
        #     for i in ref_doc.loan_details:
        #         if i.deducted==1:
        #             ded+=1
        #     if dedcount!=ded:
        #         frappe.throw()
    def on_submit(self):
        create_additional_salaries_for_loans()
import frappe
from datetime import datetime
from dateutil.relativedelta import relativedelta

@frappe.whitelist()
def calculate_loan_schedule(start_date, count, total_amount,extension,datecount):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    lencount = int(count)
    total_amount = float(total_amount)
    monthly_amount = round(total_amount / int(count), 2)
    # balance = total_amount
    schedule = []
    # frappe.errprint('lencountttt')
    for i in range(lencount):
        from_date = start_date + relativedelta(months=i)
        to_date = start_date + relativedelta(months=i+1) - relativedelta(days=1)
        # balance -= monthly_amount
        schedule.append({
            "from_date": from_date.strftime("%Y-%m-%d"),
            "to_date": to_date.strftime("%Y-%m-%d"),
            "deduction_amount": monthly_amount,
            # "balance": round(balance, 2)
        })

    return schedule

@frappe.whitelist()
def calculate_loan_schedule_len(start_date, count, total_amount,datecount):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    lencount=int(count)-int(datecount)
    
    total_amount = float(total_amount)
    monthly_amount = round(total_amount / int(count), 2)
    # balance = total_amount
    schedule = []
    # frappe.errprint('lencount')
    for i in range(lencount):
        from_date = start_date + relativedelta(months=i)
        to_date = start_date + relativedelta(months=i+1) - relativedelta(days=1)
        # balance -= monthly_amount
        schedule.append({
            "from_date": from_date.strftime("%Y-%m-%d"),
            "to_date": to_date.strftime("%Y-%m-%d"),
            "deduction_amount": monthly_amount,
            # "balance": round(balance, 2)
        })

    return schedule
@frappe.whitelist()
def create_additional_salaries_for_loans():
    today = datetime.today().date()
    employee_loans=frappe.get_all("Employee Loan", {"docstatus": 1}, ["name", "employee"])
    for loan in employee_loans:
        loan_doc=frappe.get_doc("Employee Loan", loan.name)
        for detail in loan_doc.loan_details:
            if detail.from_date==today:
                existing = frappe.get_all("Additional Salary", {
                    "employee": loan_doc.employee,
                    "payroll_date": detail.from_date,
                    "salary_component": "Loan",
                    "docstatus": ("!=", 2)  
                })
                if not existing:
                    additional_salary = frappe.new_doc("Additional Salary")
                    additional_salary.employee = loan_doc.employee
                    additional_salary.salary_component = "Loan"
                    additional_salary.payroll_date = detail.from_date
                    additional_salary.amount = detail.deduction_amount
                    additional_salary.overwrite_salary_structure_amount = 1
                    additional_salary.custom_loan_reference=loan.name
                    additional_salary.insert(ignore_permissions=True)
                    additional_salary.submit()
                    frappe.db.commit()

@frappe.whitelist()
def update_slip_id(doc,method):
    slip=frappe.get_doc("Salary Slip",doc.name)
    for s in slip.deductions:
        if s.salary_component=='Loan':
            additional_salary=frappe.db.get_value("Additional Salary",{'payroll_date':('between',(doc.start_date,doc.end_date)),'salary_component':"Loan",'custom_loan_reference':['!=',''],'docstatus':1},['custom_loan_reference'])
            if additional_salary:
                payroll_date=frappe.db.get_value("Additional Salary",{'payroll_date':('between',(doc.start_date,doc.end_date)),'salary_component':"Loan",'custom_loan_reference':['!=',''],'docstatus':1},['payroll_date'])
                loan=frappe.get_doc("Employee Loan",additional_salary)
                for i in loan.loan_details:
                    if i.from_date==payroll_date:
                        i.salary_slip=doc.name
                        i.deducted=1
                loan.save(ignore_permissions=True)
                frappe.db.commit()
                
@frappe.whitelist()
def clear_slip_id(doc, method):
    slip = frappe.get_doc("Salary Slip", doc.name)
    for s in slip.deductions:
        if s.salary_component == 'Loan':
            loans = frappe.get_all("Employee Loan", filters={'employee': slip.employee}, fields=['name'])
            for loan_doc in loans:
                loan = frappe.get_doc("Employee Loan", loan_doc.name)
                updated = False
                for i in loan.loan_details:
                    if i.salary_slip == doc.name:
                        i.salary_slip = ""
                        i.deducted = 0
                        updated = True
                if updated:
                    loan.save(ignore_permissions=True)
    frappe.db.commit()


@frappe.whitelist()
def create_hooks_event():
	job = frappe.db.exists('Scheduled Job Type', 'create_events')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")
		sjt.update({
			"method": 'shaher.shaher.doctype.employee_loan.employee_loan.create_additional_salaries_for_loans',
			"frequency": 'Cron',
			"cron_format": '0 0 * * *'
		})
		sjt.save(ignore_permissions=True)