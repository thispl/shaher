# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now, getdate,date_diff,add_days
from datetime import timedelta
import datetime

class RejoiningForm(Document):
    # pass
    # update the passport status and rejjoining date in employee
    def on_submit(self):
        frappe.db.set_value("Employee",self.employee_id,"custom_rejoining_date",self.re_join)
        frappe.db.set_value("Employee",self.employee_id,"custom_passport_at",self.passport_at)
    def validate(self):
        self.extension_from_date=add_days(self.end, 1)
        self.extension_to_date=add_days(self.re_join, -1)

#Enable the hod checkbox in Rejoining form based on below condition
@frappe.whitelist()
def get_role(employee):
    user_id = frappe.get_value('Employee',{'employee':employee},['user_id'])
    hod = frappe.get_value('User',{'email':user_id},['name'])
    role = "HOD"
    hod = frappe.get_value('Has Role',{'role':role,'parent':hod})
    if hod:
        return  "HI"
    else:
        return "HII"

