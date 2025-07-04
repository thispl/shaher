# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import date_diff, today, add_days, nowdate, unique, cstr
from frappe.utils import (
	add_days,
	cint,
	cstr,
	date_diff,
	flt,
	formatdate,
	get_fullname,
	get_link_to_form,
	getdate,
	nowdate,
)
from frappe.utils import (
	formatdate,
	get_link_to_form,
	
)

class FinancialMonitorDocument(Document):
	def validate(self):
		if self.reference_number:
			if frappe.db.exists('Financial Monitor Document',{'document_type':self.document_type,'reference_number':self.reference_number,'name':['!=',self.name]}):
				doc=frappe.db.get_value('Financial Monitor Document',{'document_type':self.document_type,'reference_number':self.reference_number,'name':['!=',self.name]},['name'])
				form_link = get_link_to_form('Financial Monitor Document', doc)
				msg = _("Document already found with the same reference number. <b>{0}</b>").format(
				form_link
				)
				frappe.throw(msg)
		if self.status=='Cleared':
			if self.document_type not in ['Security Cheque','Cheque']:
				frappe.throw('Document type should be <b>Cheque / Security Cheque</b> to mark status as cleared.')
		if self.status=='Expired':
			if self.valid_upto:
				if getdate(self.valid_upto) > getdate(today()):
					days=date_diff(self.valid_upto,today())
					frappe.throw(f'For Expiry date {days} more day(s) are there. ')
