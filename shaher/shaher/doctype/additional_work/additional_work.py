# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ADDITIONALWORK(Document):
	def validate(self):
		tot=0
		for i in self.additional_work_details:
			tot+=i.amount_to_be_paid or 0
		self.additional_total=tot
	def on_submit(self):
		additional_doc=frappe.get_doc(self.against,self.reference_id)
		cum=additional_doc.cumulative_additional_work+self.additional_total
		additional_doc.additional_work_total+=self.additional_total
		additional_doc.cumulative_additional_work=cum
		additional_doc.save(ignore_permissions=True)
	def on_cancel(self):
		additional_doc=frappe.get_doc(self.against,self.reference_id)
		additional_doc.additional_work_total-=self.additional_total
		additional_doc.cumulative_additional_work-=self.additional_total
		additional_doc.save(ignore_permissions=True)
