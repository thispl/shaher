# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, add_months,today,add_days,nowdate,flt
import datetime
from datetime import datetime


class SupplierEvaluationForm(Document):
	def on_submit(self):
		if self.approval_status == 'Approved':
			if frappe.db.exists('Supplier',self.external_provider):
				supplier = frappe.get_doc("Supplier", self.external_provider)
				supplier.approved_supplier = 1
				supplier.db_update()
