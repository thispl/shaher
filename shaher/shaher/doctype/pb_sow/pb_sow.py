# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PBSOW(Document):
	def validate(self):
		self.total_overheads = (self.business_promotion_amount or 0) + (self.overhead_amount or 0) + (self.contigency_amount or 0) + (self.gross_profit_amount or 0)
		self.total_cost = get_total_cost(self) # To get total amount from all the Project Materials table
		self.bidding_amount = (self.total_cost or 0) + (self.total_overheads or 0)
		self.bidding_amount_difference = (self.lpo_amount or 0) - (self.bidding_amount or 0)
	
@frappe.whitelist()
def get_total_cost(self):
	total_amount = 0
	for row in self.design:
		total_amount += row.amount
	for row in self.materials:
		total_amount += row.amount
	for row in self.raw_materials:
		total_amount += row.amount
	for row in self.finishing_work:
		total_amount += row.amount
	for row in self.accessories:
		total_amount += row.amount
	for row in self.installation:
		total_amount += row.amount
	for row in self.heavy_equipments:
		total_amount += row.amount
	for row in self.subcontract:
		total_amount += row.amount
	for row in self.finished_goods:
		total_amount += row.amount
	return total_amount

