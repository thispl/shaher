
import frappe
import json

from dateutil.relativedelta import relativedelta

import frappe
from frappe import _
from frappe.desk.reportview import get_match_cond
from frappe.model.document import Document
from frappe.query_builder.functions import Coalesce, Count
from frappe.utils import (
	DATE_FORMAT,
	add_days,
	add_to_date,
	cint,
	comma_and,
	date_diff,
	flt,
	get_link_to_form,
	getdate,
)

from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip
from hrms.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry
from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words, formatdate, get_first_day,today
from hrms.payroll.doctype.payroll_entry.payroll_entry import show_payroll_submission_status,log_payroll_failure

class CustomPayrollEntry(PayrollEntry):
    @frappe.whitelist()
    def submit_salary_slips(self):
        self.check_permission("write")
        salary_slips = self.get_sal_slip_list(ss_status=0)

        if len(salary_slips) > 30 or frappe.flags.enqueue_payroll_entry:
            self.db_set("status", "Queued")
            frappe.enqueue(
                submit_salary_slips_for_employees,
                timeout=3000,
                payroll_entry=self,
                salary_slips=salary_slips,
                publish_progress=False,
            )
            frappe.msgprint(
                _("Salary Slip submission is queued. It may take a few minutes"),
                alert=True,
                indicator="blue",
            )
        else:
            submit_salary_slips_for_employees(self, salary_slips, publish_progress=False)
                
def submit_salary_slips_for_employees(payroll_entry, salary_slips, publish_progress=True):
    try:
        submitted = []
        unsubmitted = []
        frappe.flags.via_payroll_entry = True
        count = 0

        for entry in salary_slips:
            salary_slip = frappe.get_doc("Salary Slip", entry[0])
            if salary_slip.custom_hold==1:
                unsubmitted.append(entry[0])
            elif salary_slip.net_pay < 0:
                unsubmitted.append(entry[0])
            else:
                try:
                    salary_slip.submit()
                    submitted.append(salary_slip)
                except frappe.ValidationError:
                    unsubmitted.append(entry[0])

            count += 1
            if publish_progress:
                frappe.publish_progress(
                    count * 100 / len(salary_slips), title=_("Submitting Salary Slips...")
                )

        if submitted:
            payroll_entry.make_accrual_jv_entry(submitted)
            payroll_entry.email_salary_slip(submitted)
            payroll_entry.db_set({"salary_slips_submitted": 1, "status": "Submitted", "error_message": ""})

        show_payroll_submission_status(submitted, unsubmitted, payroll_entry)

    except Exception as e:
        frappe.db.rollback()
        log_payroll_failure("submission", payroll_entry, e)

    finally:
        frappe.db.commit()  # nosemgrep
        frappe.publish_realtime("completed_salary_slip_submission", user=frappe.session.user)

    frappe.flags.via_payroll_entry = False

class CustomSalarySlip(SalarySlip):
    def get_date_details(self):
        no_of_days = frappe.db.sql(
            """
            SELECT no_of_days_worked, ot_hours 
            FROM `tabAttendance and OT Register` 
            WHERE from_date <= %s or to_date>= %s
            AND employee = %s 
            AND docstatus = 1
            """,
            (self.end_date,self.start_date, self.employee),
            as_dict=False
        )
        payment_days = no_of_days[0][0] if no_of_days and no_of_days[0][0] else 0
        ot_hours  = no_of_days[0][1] if no_of_days and no_of_days[0][1] else 0

        ot_amount = frappe.db.sql(
            """
            SELECT SUM(custom_overtime_amount) 
            FROM `tabAttendance` 
            WHERE attendance_date BETWEEN %s AND %s 
            AND employee = %s 
            AND docstatus = 1
            """,
            (self.start_date, self.end_date, self.employee),
            as_dict=False
        )
        ot_amount = ot_amount[0][0] if ot_amount and ot_amount[0][0] else 0
        self.custom_overtime_amount =ot_amount
        self.payment_days = frappe.db.get_value("Attendance and OT Register",{'from_date':('<=',self.end_date),'to_date':('>=',self.start_date),'employee':self.employee},['no_of_days_worked']) or 0
        self.custom_overtime_hours = frappe.db.get_value("Attendance and OT Register",{'from_date':('<=',self.end_date),'to_date':('>=',self.start_date),'employee':self.employee},['ot_hours']) or 0
        self.custom_night_ot_hours = frappe.db.get_value("Attendance and OT Register",{'from_date':('<=',self.end_date),'to_date':('>=',self.start_date),'employee':self.employee},['night_ot']) or 0
        self.custom_holiday_ot_hours = frappe.db.get_value("Attendance and OT Register",{'from_date':('<=',self.end_date),'to_date':('>=',self.start_date),'employee':self.employee},['wo_nh']) or 0

@frappe.whitelist()
def custom_round(value):
    integer_part = int(value)
    decimal_part = value - integer_part

    if decimal_part < 0.50:
        decimal_part = 0.00
    else:
        decimal_part = 0.50

    return integer_part + decimal_part