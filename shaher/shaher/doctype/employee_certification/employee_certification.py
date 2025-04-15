# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, today, nowdate, add_days, formatdate


class EmployeeCertification(Document):
	def before_insert(self):
		existing_doc = frappe.db.get_value(
			"Employee Certification", 
			{"certification": self.certification, "employee": self.employee, "status": ["!=", "Expired"]}, 
			["employee", "certification", "name"]
		)

		# Check if a duplicate exists before unpacking
		if existing_doc:
			employee, certification, existing_doc_name = existing_doc  # Unpack only if found
			frappe.throw(
				f"A certification <b>{certification}</b> for <b>{employee}</b> already exists: <a href='/app/employee-certification/{existing_doc}'><b>{existing_doc_name}</b></a>.",
				title="Duplicate Certification"
			)
   
	def validate(self):
		if not frappe.db.exists("Item", self.certification):
			itm = frappe.new_doc("Item")
			itm.item_code = self.certification
			itm.is_stock_item = 0
			itm.item_group = "Services"
			itm.stock_uom = "Nos"
			itm.save(ignore_permissions=True)
			frappe.db.commit()

		if self.expiry_date and self.last_renewal_date:
			if self.expiry_date < self.last_renewal_date:
				frappe.throw("<b>Expiry Date</b> must be greater than the <b>Last Renewal Date</b>")
			frequency = date_diff(self.expiry_date,self.last_renewal_date)
			self.frequency_of_renewal_days = frequency
			diff = date_diff(self.expiry_date, today())
			self.days_left = diff
   
		if self.possibility_status == "Unlimited Validity":
			self.status = "Unlimited"
		elif self.possibility_status == "Non Renewable":
			self.status = "Not Renewable"
		elif self.possibility_status == "Renewable":
			if self.days_left < 0:
				self.status = "Expired"
			elif self.days_left < 31:
				self.status = "Expiring Soon"
			else:
				self.status = "Active"

	
@frappe.whitelist()
def update_days_left():
	value = frappe.get_all("Employee Certification",["expiry_date","name"])
	for i in value:
		ec = frappe.get_doc("Employee Certification", i.name)
		if ec.expiry_date:
			diff = date_diff(ec.expiry_date, today())
			ec.days_left = diff
			ec.save(ignore_permissions=True)
   
@frappe.whitelist()
def update_days_left_daily():
    job_name = "update_days_left_for_employee_certification"
    
    job = frappe.get_value("Scheduled Job Type", job_name, "name")
    
    if not job:
        emc = frappe.new_doc("Scheduled Job Type")
        emc.update({
            "name": job_name,
            "method": "shaher.shaher.doctype.employee_certification.employee_certification.update_days_left",
            "frequency": "Cron",
            "cron_format": "0 0 * * *",
            "is_enabled": 1 
        })
        emc.insert(ignore_permissions=True)
        frappe.db.commit()
        
@frappe.whitelist()
def monthly_expiry_doc_daily():
    job_name = "alert_mail_for_expiring_employee_certification"
    
    job = frappe.get_value("Scheduled Job Type", job_name, "name")
    
    if not job:
        emc = frappe.new_doc("Scheduled Job Type")
        emc.update({
            "name": job_name,
            "method": "shaher.shaher.doctype.employee_certification.employee_certification.monthly_expiry_doc",
            "frequency": "Cron",
            "cron_format": "0 0 * * *",
            "is_enabled": 1 
        })
        emc.insert(ignore_permissions=True)
        frappe.db.commit()

@frappe.whitelist()    
def monthly_expiry_doc():
	doc=frappe.get_all("Employee Certification",{'status': 'Expiring Soon'},['name','days_left','expiry_date'])
	documents = ''
	documents += '<table class = table table - bordered style=border-width:2px><tr><td colspan = 6><b>Employee Certification List</b></td></tr>'
	documents += '<tr><td colspan=2>Document Name</td><td colspan=2>Expiry Date</td><td colspan=2>Days Left</td>'
	for i in doc:
		ec = frappe.get_doc("Employee Certification", i.name)
		recipient = []
		for r in ec.alert_mail:
			recipient.append(r.user)
		frappe.sendmail(
				recipients=recipient,
				cc = ['amar.p@groupteampro.com'],
				subject=('Employee Certification'),
				message=f"""
						Dear Sir/Mam,<br>
						<p>The Ceritification <b>{ec.certification}</b> of the employee <b>{ec.employee}</b> is going to be expired in <b>{ec.days_left} days</b></p>
						%s
						"""
			) 
	
	return True
