import frappe
from frappe.utils import nowdate
from datetime import date

@frappe.whitelist()
def update_employee_certification_status():
    ec = frappe.get_all("Employee Certification",fields=['name','possibility_status','expiry_date'])
    for i in ec:
        if i['possibility_status'] == 'Renewable':
            next_renewal_date = i['expiry_date']
            days_left = (next_renewal_date - date.today()).days
            frappe.set_value('Employee Certification',i['name'],"days_left",days_left)
            if days_left <= 30:
                status = "Due for Renewal"
            else:
                status = "Valid"
            frappe.set_value('Employee Certification',i['name'],"status",status)
