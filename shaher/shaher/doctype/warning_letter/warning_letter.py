# Copyright (c) 2024, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WarningLetter(Document):
    pass

@frappe.whitelist()
def warning_letter_count(employee):
    if employee:
        count = frappe.db.count("Warning Letter", {"employee": employee})
        return count if count else 0
    
@frappe.whitelist()
def issue_type_count(employee, issue_type):
    if employee and issue_type:
        count = frappe.db.count("Warning Letter", {"employee": employee, "issue_type": issue_type})
        return count if count else 0
        

