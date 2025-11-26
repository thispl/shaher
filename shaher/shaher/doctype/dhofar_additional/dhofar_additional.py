# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DHOFARADDITIONAL(Document):
	def validate(self):
		if frappe.db.exists('DHOFAR ADDITIONAL', {'docstatus': ['!=', 2], "invoice_from": self.invoice_from, 'name': ['!=', self.name]}):
			frappe.throw('Already another document present for this month')

		manpower_tot = vehicle_tot = per_trip_tot = tot_ac = tot_ff=0
		man_cumu = vehicle_cumu = per_trip_cum = ac_cumm = ff_cumm= 0
		prev_manpower = prev_vehicle = prev_per_trip =prev_ac = prev_ff= 0

		previous_mis = frappe.get_all(
			'DHOFAR ADDITIONAL',
			{
				'docstatus': 0,
				'invoice_from': ['<=', self.invoice_from],
				'name': ['!=', self.name]
			},['name']
		)
		previous_mis_names = [d.name for d in previous_mis]

		for row in self.base_manpower:
			current_amt = row.total_claim_this_month - float(row.total_deduction or 0)
			row.amount_to_be_paid = current_amt
			manpower_tot += current_amt

			prev_amt = 0
			if previous_mis_names and row.description:
				prev_amt = frappe.db.sql("""
					SELECT SUM(pp.amount_to_be_paid)
					FROM `tabPermanent Manpower` pp
					JOIN `tabDHOFAR ADDITIONAL` mo ON mo.name = pp.parent
					WHERE mo.name IN %(names)s AND pp.description = %(desc)s
				""", {'names': previous_mis_names, 'desc': row.description})[0][0] or 0

			row.previous_claim = prev_amt
			row.cumulative_amount = current_amt + prev_amt
			prev_manpower += prev_amt
			man_cumu += row.cumulative_amount

		for row in self.base_vehicle:
			current_amt = row.total_claim_this_month - float(row.total_deduction or 0)
			row.amount_to_be_paid = current_amt
			vehicle_tot += current_amt

			prev_amt = 0
			if previous_mis_names and row.description:
				prev_amt = frappe.db.sql("""
					SELECT SUM(pv.amount_to_be_paid)
					FROM `tabPermanent Vehicle` pv
					JOIN `tabDHOFAR ADDITIONAL` mo ON mo.name = pv.parent
					WHERE mo.name IN %(names)s AND pv.description = %(desc)s
				""", {'names': previous_mis_names, 'desc': row.description})[0][0] or 0

			row.previous_claim = prev_amt
			row.cumulative_amount = current_amt + prev_amt
			prev_vehicle += prev_amt
			vehicle_cumu += row.cumulative_amount

		for row in self.base_vehicle_cost_per_trip:
			current_amt = row.total_claim_this_month - float(row.total_deduction or 0)
			row.amount_to_be_paid = current_amt
			per_trip_tot += current_amt

			prev_amt = 0
			if previous_mis_names and row.description:
				prev_amt = frappe.db.sql("""
					SELECT SUM(at.amount_to_be_paid)
					FROM `tabBase Vehicle Cost Per Trip` at
					JOIN `tabDHOFAR ADDITIONAL` mo ON mo.name = at.parent
					WHERE mo.name IN %(names)s AND at.description = %(desc)s
				""", {'names': previous_mis_names, 'desc': row.description})[0][0] or 0

			row.previous_claim = prev_amt
			row.cumulative_amount = current_amt + prev_amt
			prev_per_trip += prev_amt
			per_trip_cum += row.cumulative_amount

		for row in self.airconditioning_system_spare_parts:
			current_amt = row.total_claim_this_month - float(row.total_deduction or 0)
			row.amount_to_be_paid = current_amt
			tot_ac += current_amt

			prev_amt = 0
			if previous_mis_names and row.description:
				prev_amt = frappe.db.sql("""
					SELECT SUM(at.amount_to_be_paid)
					FROM `tabAIRCONDITIONING SYSTEM SPARE PARTS` at
					JOIN `tabDHOFAR ADDITIONAL` mo ON mo.name = at.parent
					WHERE mo.name IN %(names)s AND at.description = %(desc)s
				""", {'names': previous_mis_names, 'desc': row.description})[0][0] or 0

			row.previous_claim = prev_amt
			row.cumulative_amount = current_amt + prev_amt
			prev_ac += prev_amt
			ac_cumm += row.cumulative_amount

		for row in self.ff_systems_spare_parts:
			current_amt = row.total_claim_this_month - float(row.total_deduction or 0)
			row.amount_to_be_paid = current_amt
			tot_ff += current_amt

			prev_amt = 0
			if previous_mis_names and row.description:
				prev_amt = frappe.db.sql("""
					SELECT SUM(at.amount_to_be_paid)
					FROM `tabFF Systems Spare Parts` at
					JOIN `tabDHOFAR ADDITIONAL` mo ON mo.name = at.parent
					WHERE mo.name IN %(names)s AND at.description = %(desc)s
				""", {'names': previous_mis_names, 'desc': row.description})[0][0] or 0

			row.previous_claim = prev_amt
			row.cumulative_amount = current_amt + prev_amt
			prev_ff += prev_amt
			ff_cumm += row.cumulative_amount


		self.manpower_total = manpower_tot
		self.vehicle_total = vehicle_tot
		self.vehicle_cost_per_trip_total = per_trip_tot
		self.previous_ac_spare_parts=prev_ac
		self.previous_fire_fighting_parts=prev_ff
		self.previous_manpower = prev_manpower
		self.previous_vehicle = prev_vehicle
		self.previous_vehicle_cost_per_trip = prev_per_trip
		self.ac_spare_parts_total=tot_ac
		self.fire_fighting_parts_total=tot_ff
		self.cumulative_manpower = man_cumu
		self.cumulative_vehicle = vehicle_cumu
		self.cumulative_previous_vehicle_cost_per_trip = per_trip_cum
		self.cumulative_ac_spare_parts=ac_cumm
		self.cumulative_fire_fighting_parts=ff_cumm

		previous_total = frappe.db.sql("""
			SELECT SUM(additional_total)
			FROM `tabADDITIONAL WORK`
			WHERE
				invoice_from < %s AND
				docstatus = 1 AND
				additional_work_against = 'DHOFAR'
		""", (self.invoice_from))[0][0] or 0
		self.previous_additional_work=previous_total
		if self.additional_work_total == 0:
			self.cumulative_additional_work=previous_total

