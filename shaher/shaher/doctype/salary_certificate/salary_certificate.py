# Copyright (c) 2024, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SalaryCertificate(Document):
		def after_insert(self):
			from datetime import datetime
			from frappe.utils import formatdate  

			posting_date = formatdate(self.date, "dd-MM-yyyy")
			hod=frappe.db.get_value("Employee",{"name":self.reference},["reports_to"])
			user_id=frappe.db.get_value("Employee",{"name":hod},["user_id"])
			frappe.sendmail(
				recipients=[user_id],
				subject=f'New Salary Certificate Request-{self.name}  is Raised',
				message=f"""
				<b>Dear Sir/Mam,</b><br><br>
				A new Salary Certificate Request{self.name}has been created.<br><br>
				<br>
				Employee:{self.reference}<br>
				Employee Name:{self.name1}<br>
				Department:{self.deapartment}<br>
				Designation:{self.designation}
				<i>This email has been automatically generated. Please do not reply</i>
				"""
		)
			
		def on_submit(self):
			user_id=frappe.db.get_value("Employee",{"name":self.reference},["user_id"])
			frappe.sendmail(
				recipients=[user_id],
				subject=f'Salary Certificate Request-{self.name}  is Approved',
				message=f"""
				<b>Dear Sir/Mam,</b><br><br>
				Your Salary Certificate Request{self.name}has been Approved.<br><br>
				<br>
				<i>This email has been automatically generated. Please do not reply</i>
				"""
		)

		def on_update(self):
			ws = ''
			if self.workflow_state == "Rejected":
				current_user = frappe.session.user
				user_role = frappe.get_roles(current_user)
				if "HR User" in user_role:
						ws = "Pending for HR Department"
				elif "HOD" in user_role:
					ws = "Pending for HOD"
				elif "HR Manager" in user_role:
					ws = "Pending for HR Manager"
				if not self.rejection_remark:
						frappe.db.sql("""
									UPDATE `tabSalary Certificate`
									SET docstatus = 0, workflow_state = %s
									WHERE name = %s
							""",(ws, self.name),as_dict=True)
						self.reload()
				if self.rejection_remark:
					frappe.db.sql("""
								UPDATE `tabSalary Certificate`
				   				SET docstatus = 1, workflow_state = 'Rejected'
				   				WHERE name = %s
								""", (self.name), as_dict=True)

