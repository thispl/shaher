# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MISOpex(Document):
    def validate(self):
        if frappe.db.exists('MIS Opex', {'docstatus': ['!=', 2], "invoice_from": self.invoice_from, 'name': ['!=', self.name]}):
            frappe.throw('Already another document present for this month')

        manpower_tot = vehicle_tot = acc_tot = 0
        man_cumu = vehicle_cumu = accom_cumu = 0
        prev_manpower = prev_vehicle = prev_accom = 0

        previous_mis = frappe.get_all(
            'MIS Opex',
            {
                'docstatus': 1,
                'invoice_from': ['<=', self.invoice_from],
                'name': ['!=', self.name]
            },['name']
        )
        previous_mis_names = [d.name for d in previous_mis]

        for row in self.permanent_manpower:
            current_amt = row.total_claim_this_month - (row.total_deduction or 0)
            row.amount_to_be_paid = current_amt
            manpower_tot += current_amt

            prev_amt = 0
            if previous_mis_names and row.description:
                prev_amt = frappe.db.sql("""
                    SELECT SUM(pp.amount_to_be_paid)
                    FROM `tabPermanent Manpower` pp
                    JOIN `tabMIS Opex` mo ON mo.name = pp.parent
                    WHERE mo.name IN %(names)s AND pp.description = %(desc)s AND pp.employee_type= %(etype)s
                """, {'names': previous_mis_names, 'desc': row.description,'etype':row.employee_type})[0][0] or 0

            row.previous_claim = prev_amt
            row.cumulative_amount = current_amt + prev_amt
            prev_manpower += prev_amt
            man_cumu += row.cumulative_amount

        for row in self.permanent_vehicle:
            current_amt = row.total_claim_this_month - (row.total_deduction or 0)
            row.amount_to_be_paid = current_amt
            vehicle_tot += current_amt

            prev_amt = 0
            if previous_mis_names and row.description:
                prev_amt = frappe.db.sql("""
                    SELECT SUM(pv.amount_to_be_paid)
                    FROM `tabPermanent Vehicle` pv
                    JOIN `tabMIS Opex` mo ON mo.name = pv.parent
                    WHERE mo.name IN %(names)s AND pv.description = %(desc)s AND pv.region=%(reg)s
                """, {'names': previous_mis_names, 'desc': row.description, 'reg':row.region})[0][0] or 0

            row.previous_claim = prev_amt
            row.cumulative_amount = current_amt + prev_amt
            prev_vehicle += prev_amt
            vehicle_cumu += row.cumulative_amount

        for row in self.accommodation_table:
            current_amt = row.total_claim_this_month - (row.total_deduction or 0)
            row.amount_to_be_paid = current_amt
            acc_tot += current_amt

            prev_amt = 0
            if previous_mis_names and row.tools:
                prev_amt = frappe.db.sql("""
                    SELECT SUM(at.amount_to_be_paid)
                    FROM `tabAccommodation Table` at
                    JOIN `tabMIS Opex` mo ON mo.name = at.parent
                    WHERE mo.name IN %(names)s AND at.tools = %(desc)s
                """, {'names': previous_mis_names, 'desc': row.tools})[0][0] or 0

            row.previous_claim = prev_amt
            row.cumulative_amount = current_amt + prev_amt
            prev_accom += prev_amt
            accom_cumu += row.cumulative_amount

        self.manpower_total = manpower_tot
        self.vehicle_total = vehicle_tot
        self.accommodation_total = acc_tot
        self.previous_manpower = prev_manpower
        self.previous_vehicle = prev_vehicle
        self.previous_accommodation = prev_accom
        self.cumulative_manpower = man_cumu
        self.cumulative_vehicle = vehicle_cumu
        self.cumulative_accommodation = accom_cumu


