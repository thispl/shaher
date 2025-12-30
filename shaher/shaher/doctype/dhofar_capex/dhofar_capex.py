# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DHOFARCAPEX(Document):
    def validate(self):
        if self.name:
            exist_doc = frappe.db.get_value('DHOFAR CAPEX',{'docstatus': ['!=', 2],'name': ['!=', self.name],'invoice_from': ['<=', self.invoice_upto],'invoice_upto': ['>=', self.invoice_from]},['name'])

            if exist_doc:
                frappe.throw(
                    f'DHOFAR CAPEX document already exists for this Period: '
                    f'<a href="/app/dhofar-capex/{exist_doc}" target="_blank">{exist_doc}</a>.',
                    title='Warning'
                )



        manpower_tot = vehicle_tot = acc_tot = 0
        man_cumu = vehicle_cumu = accom_cumu = 0
        prev_manpower = prev_vehicle = prev_accom = 0

        previous_mis = frappe.get_all(
            'DHOFAR CAPEX',
            {
                'docstatus': 1,
                'invoice_from': ['<=', self.invoice_from],
                'name': ['!=', self.name]
            },['name']
        )
        previous_mis_names = [d.name for d in previous_mis]

        for row in self.permanent_manpower:
            current_amt = current_amt = row.total_claim_this_month - (float(row.total_deduction) if row.total_deduction else 0)

            row.amount_to_be_paid = current_amt
            manpower_tot += current_amt

            prev_amt = 0
            if previous_mis_names and row.description:
                prev_amt = frappe.db.sql("""
                    SELECT SUM(pp.amount_to_be_paid)
                    FROM `tabPermanent Manpower` pp
                    JOIN `tabDHOFAR CAPEX` mo ON mo.name = pp.parent
                    WHERE mo.name IN %(names)s AND pp.description = %(desc)s
                """, {'names': previous_mis_names, 'desc': row.description})[0][0] or 0

            row.previous_claim = prev_amt
            row.cumulative_amount = current_amt + prev_amt
            prev_manpower += prev_amt
            man_cumu += row.cumulative_amount

        for row in self.permanent_vehicle:
            current_amt = float(row.total_claim_this_month) - (float(row.total_deduction) if row.total_deduction else 0)

            row.amount_to_be_paid = current_amt
            vehicle_tot += current_amt

            prev_amt = 0
            if previous_mis_names and row.description:
                prev_amt = frappe.db.sql("""
                    SELECT SUM(pv.amount_to_be_paid)
                    FROM `tabPermanent Vehicle` pv
                    JOIN `tabDHOFAR CAPEX` mo ON mo.name = pv.parent
                    WHERE mo.name IN %(names)s AND pv.description = %(desc)s
                """, {'names': previous_mis_names, 'desc': row.description})[0][0] or 0

            row.previous_claim = prev_amt
            row.cumulative_amount = current_amt + prev_amt
            prev_vehicle += prev_amt
            vehicle_cumu += row.cumulative_amount

        self.manpower_total = manpower_tot
        self.vehicle_total = vehicle_tot
        self.accommodation_total = acc_tot
        self.previous_manpower = prev_manpower
        self.previous_vehicle = prev_vehicle
        self.previous_accommodation = prev_accom
        self.cumulative_manpower = man_cumu
        self.cumulative_vehicle = vehicle_cumu
        self.cumulative_accommodation = accom_cumu
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
        # First  pass — accumulate values from all non-total rows
        for row in self.permanent_manpower:
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

        # Second pass — set totals on the Total row
        for row in self.permanent_manpower:
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

        for row in self.permanent_vehicle:
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

        for row in self.permanent_vehicle:
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

        self.month_total  = self.manpower_total + self.vehicle_total + self.accommodation_total