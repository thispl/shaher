# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MISADDITIONAL(Document):
	def validate(self):
		if frappe.db.exists('MIS ADDITIONAL', {'docstatus': ['!=', 2], "invoice_from": self.invoice_from, 'name': ['!=', self.name]}):
			frappe.throw('Already another document present for this month')

		manpower_tot = vehicle_tot = per_trip_tot = tot_ac = tot_ff=tot_ot=tot_mp=0
		man_cumu = vehicle_cumu = per_trip_cum = ac_cumm = ff_cumm= ot_cumm = mp_cumm=0
		prev_manpower = prev_vehicle = prev_per_trip =prev_ac = prev_ff= prev_ot = prev_mp= 0

		previous_mis = frappe.get_all(
			'MIS ADDITIONAL',
			{
				'docstatus': 1,
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
					JOIN `tabMIS ADDITIONAL` mo ON mo.name = pp.parent
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
					JOIN `tabMIS ADDITIONAL` mo ON mo.name = pv.parent
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
					JOIN `tabMIS ADDITIONAL` mo ON mo.name = at.parent
					WHERE mo.name IN %(names)s AND at.description = %(desc)s
				""", {'names': previous_mis_names, 'desc': row.description})[0][0] or 0

			row.previous_claim = prev_amt
			row.cumulative_amount = current_amt + prev_amt
			prev_per_trip += prev_amt
			per_trip_cum += row.cumulative_amount

		for row in self.airconditioning_system_spare_parts:
			current_amt = row.total_claim_this_month -float(row.total_deduction or 0)
			row.amount_to_be_paid = current_amt
			tot_ac += current_amt

			prev_amt = 0
			if previous_mis_names and row.description:
				prev_amt = frappe.db.sql("""
					SELECT SUM(at.amount_to_be_paid)
					FROM `tabAIRCONDITIONING SYSTEM SPARE PARTS` at
					JOIN `tabMIS ADDITIONAL` mo ON mo.name = at.parent
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
					JOIN `tabMIS ADDITIONAL` mo ON mo.name = at.parent
					WHERE mo.name IN %(names)s AND at.description = %(desc)s
				""", {'names': previous_mis_names, 'desc': row.description})[0][0] or 0

			row.previous_claim = prev_amt
			row.cumulative_amount = current_amt + prev_amt
			prev_ff += prev_amt
			ff_cumm += row.cumulative_amount


		for row in self.overtime_details:
			current_amt = row.total or 0
			row.amount_to_be_paid = current_amt
			tot_ot += current_amt

			prev_amt = 0
			if previous_mis_names and row.description:
				prev_amt = frappe.db.sql("""
					SELECT SUM(pp.amount_to_be_paid)
					FROM `tabOvertime Details` pp
					JOIN `tabMIS ADDITIONAL` mo ON mo.name = pp.parent
					WHERE mo.name IN %(names)s AND pp.description = %(desc)s 
				""", {'names': previous_mis_names, 'desc': row.description})[0][0] or 0

			row.previous_claim = prev_amt
			row.cumulative_amount = current_amt + prev_amt
			prev_ot += prev_amt
			ot_cumm += row.cumulative_amount

		for row in self.additional_manpower:
			current_amt = row.total_claim_this_month - (row.total_deduction or 0)
			row.amount_to_be_paid = current_amt
			tot_mp += current_amt

			prev_amt = 0
			if previous_mis_names and row.description:
				prev_amt = frappe.db.sql("""
					SELECT SUM(at.amount_to_be_paid)
					FROM `tabAdditional Manpower Details` at
					JOIN `tabMIS ADDITIONAL` mo ON mo.name = at.parent
					WHERE mo.name IN %(names)s AND at.description = %(desc)s
				""", {'names': previous_mis_names, 'desc': row.description})[0][0] or 0

			row.previous_claim = prev_amt
			row.cumulative_amount = current_amt + prev_amt
			prev_mp += prev_amt
			mp_cumm += row.cumulative_amount


		self.previous_ot=prev_ot
		self.ot_total=tot_ot
		self.cumulative_ot=ot_cumm
		self.previous_additional_manpower=prev_mp
		self.additional_manpower_total=tot_mp
		self.cumulative_additional_manpower=mp_cumm
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
				additional_work_against = 'MIS'
		""", (self.invoice_from))[0][0] or 0
		self.previous_additional_work=previous_total

		total_employees = 0
		employees_provided = 0
		total_claim_this_month = 0
		no_of_days = 0
		no_of_absent = 0
		total_deduction = 0
		penalty_for_absent = 0
		previous_claim = 0
		amount_to_be_paid = 0
		cumulative_amount = 0
		unit_price = 0
		for row in self.base_manpower:
			if row.description != "Total":
				total_employees += (row.total_employees or 0)
				employees_provided += (row.employees_provided or 0)
				total_claim_this_month += (row.total_claim_this_month or 0)
				no_of_days += (row.no_of_days or 0)
				no_of_absent += (row.no_of_absent or 0)
				total_deduction += (row.total_deduction or 0)
				penalty_for_absent += (row.penalty_for_absent or 0)
				previous_claim += (row.previous_claim or 0)
				amount_to_be_paid += (row.amount_to_be_paid or 0)
				cumulative_amount += (row.cumulative_amount or 0)
				# unit_price += (row.unit_price or 0)

		for row in self.base_manpower:
			if row.description == "Total":
				row.total_employees = total_employees
				row.employees_provided = employees_provided
				row.total_claim_this_month = total_claim_this_month
				row.no_of_days = no_of_days
				row.no_of_absent = no_of_absent
				row.total_deduction = total_deduction
				row.penalty_for_absent = penalty_for_absent
				row.previous_claim = previous_claim
				row.amount_to_be_paid = amount_to_be_paid
				row.cumulative_amount = cumulative_amount
				row.unit_price = unit_price
		
		# Vehicle totals
		days_of_unavailability = 0
		total_no_of_days = 0
		penalty = 0
		total_total_claim = 0
		total_total_deduction = 0
		total_previous_claim = 0
		total_amount_to_be_paid = 0
		total_cumulative_amount = 0
		total_required = 0
		total_provided = 0
		unit_price = 0
		deduction = 0

		for row in self.base_vehicle:
			if row.description != "Total":

				total_required += float(row.total_required or 0)
				total_provided += float(row.total_provided or 0)
				# unit_price += (row.unit_price or 0)
				deduction += (row.deduction or 0)   

				days_of_unavailability += (row.days_of_unavailability or 0)
				total_no_of_days += (row.no_of_days or 0)
				penalty += (row.penalty or 0)
				total_total_claim += (row.total_claim_this_month or 0)
				total_total_deduction += (row.total_deduction or 0)
				total_previous_claim += (row.previous_claim or 0)
				total_amount_to_be_paid += (row.amount_to_be_paid or 0)
				total_cumulative_amount += (row.cumulative_amount or 0)

		for row in self.base_vehicle:
			if row.description == "Total":
				row.total_required = total_required
				row.total_provided = total_provided
				row.unit_price = unit_price
				row.deduction = deduction

				row.days_of_unavailability = days_of_unavailability
				row.no_of_days = total_no_of_days
				row.penalty = penalty                     
				row.total_claim_this_month = total_total_claim
				row.total_deduction = total_total_deduction
				row.previous_claim = total_previous_claim
				row.amount_to_be_paid = total_amount_to_be_paid
				row.cumulative_amount = total_cumulative_amount



		total_employees = 0
		employees_provided = 0
		total_claim_this_month = 0
		no_of_days = 0
		no_of_absent = 0
		total_deduction = 0
		penalty_for_absent = 0
		previous_claim = 0
		amount_to_be_paid = 0
		cumulative_amount = 0
		unit_price = 0
		for row in self.additional_manpower:
			if row.description != "Total":
				total_employees += (row.total_employees or 0)
				employees_provided += (row.employees_provided or 0)
				total_claim_this_month += (row.total_claim_this_month or 0)
				no_of_days += (row.no_of_days or 0)
				no_of_absent += (row.no_of_absent or 0)
				total_deduction += (row.total_deduction or 0)
				penalty_for_absent += (row.penalty_for_absent or 0)
				previous_claim += (row.previous_claim or 0)
				amount_to_be_paid += (row.amount_to_be_paid or 0)
				cumulative_amount += (row.cumulative_amount or 0)
				# unit_price += (row.unit_price or 0)

		for row in self.additional_manpower:
			if row.description == "Total":
				row.total_employees = total_employees
				row.employees_provided = employees_provided
				row.total_claim_this_month = total_claim_this_month
				row.no_of_days = no_of_days
				row.no_of_absent = no_of_absent
				row.total_deduction = total_deduction
				row.penalty_for_absent = penalty_for_absent
				row.previous_claim = previous_claim
				row.amount_to_be_paid = amount_to_be_paid
				row.cumulative_amount = cumulative_amount
				row.unit_price = unit_price
		monthly_unit_rate = 0
		basic_salary = 0
		total_claim_this_month = 0
		ot_hourly_rate = 0
		qty = 0
		total = 0
		allowances = 0
		previous_claim = 0
		amount_to_be_paid = 0
		cumulative_amount = 0
		unit = 0
		# First  pass — accumulate values from all non-total rows
		for row in self.overtime_details:
			if row.description != "Total":
				# monthly_unit_rate += (row.monthly_unit_rate or 0)
				basic_salary += (row.basic_salary or 0)
				ot_hourly_rate += (row.ot_hourly_rate or 0)
				qty += (row.qty or 0)
				total += (row.total or 0)
				allowances += (row.allowances or 0)
				previous_claim += (row.previous_claim or 0)
				amount_to_be_paid += (row.amount_to_be_paid or 0)
				cumulative_amount += (row.cumulative_amount or 0)

		# Second pass — set totals on the Total row
		for row in self.overtime_details:
			if row.description == "Total":
				row.monthly_unit_rate = monthly_unit_rate
				row.basic_salary = basic_salary
				row.ot_hourly_rate = ot_hourly_rate
				row.qty = qty
				row.total = total
				row.allowances = allowances
				row.previous_claim = previous_claim
				row.amount_to_be_paid = amount_to_be_paid
				row.cumulative_amount = cumulative_amount
		unit_price = 0
		no_of_trip = 0
		total_claim_this_month = 0
		total_deduction = 0
		previous_claim = 0
		amount_to_be_paid = 0
		cumulative_amount = 0
		for row in self.base_vehicle_cost_per_trip:
			if row.description != "Total":
				# unit_price += (row.unit_price or 0)
				no_of_trip += (row.no_of_trip or 0)
				total_deduction += (row.total_deduction or 0)
				previous_claim += (row.previous_claim or 0)
				amount_to_be_paid += (row.amount_to_be_paid or 0)
				cumulative_amount += (row.cumulative_amount or 0)

		for row in self.base_vehicle_cost_per_trip:
			if row.description == "Total":
				row.unit_price = unit_price
				row.no_of_trip = no_of_trip
				row.total_deduction = total_deduction
				row.previous_claim = previous_claim
				row.amount_to_be_paid = amount_to_be_paid
				row.cumulative_amount = cumulative_amount
		
		unit_price = 0
		unit_qty = 0
		total_claim_this_month = 0
		total_deduction = 0
		previous_claim = 0
		amount_to_be_paid = 0
		cumulative_amount = 0
		for row in self.airconditioning_system_spare_parts:
			if row.description != "Total":
				# unit_price += (row.unit_price or 0)
				unit_qty += (row.unit_qty or 0)
				total_deduction += (row.total_deduction or 0)
				previous_claim += (row.previous_claim or 0)
				amount_to_be_paid += (row.amount_to_be_paid or 0)
				cumulative_amount += (row.cumulative_amount or 0)

		for row in self.airconditioning_system_spare_parts:
			if row.description == "Total":
				row.unit_price = unit_price
				row.unit_qty = unit_qty
				row.total_deduction = total_deduction
				row.previous_claim = previous_claim
				row.amount_to_be_paid = amount_to_be_paid
				row.cumulative_amount = cumulative_amount
		unit_price = 0
		unit_qty = 0
		total_claim_this_month = 0
		total_deduction = 0
		previous_claim = 0
		amount_to_be_paid = 0
		cumulative_amount = 0
		for row in self.ff_systems_spare_parts:
			if row.description != "Total":
				# unit_price += (row.unit_price or 0)
				unit_qty += (row.unit_qty or 0)
				total_deduction += (row.total_deduction or 0)
				previous_claim += (row.previous_claim or 0)
				amount_to_be_paid += (row.amount_to_be_paid or 0)
				cumulative_amount += (row.cumulative_amount or 0)

		for row in self.ff_systems_spare_parts:
			if row.description == "Total":
				row.unit_price = unit_price
				row.unit_qty = unit_qty
				row.total_deduction = total_deduction
				row.previous_claim = previous_claim
				row.amount_to_be_paid = amount_to_be_paid
				row.cumulative_amount = cumulative_amount
		self.month_total  = self.manpower_total + self.vehicle_total + self.vehicle_cost_per_trip_total + self.ac_spare_parts_total + self.fire_fighting_parts_total + self.ot_total + self.additional_manpower_total +self.additional_work_total

		
			

		

						

			

		
			

		

		
			

		

						

			

		
			

		

						

			