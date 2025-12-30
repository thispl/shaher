# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MISOT(Document):
    def validate(self):
        if frappe.db.exists('MIS OT',{'docstatus':['!=',2],"invoice_from":self.invoice_from,'name':['!=',self.name]}):
            frappe.throw('Already another document present for this month')
        ot_tot = prev_ot = cumm_ot= 0

        previous_mis = frappe.get_all(
            'MIS OT',
            {
                'docstatus': 1,
                'invoice_from': ['<=', self.invoice_from],
                'name': ['!=', self.name]
            },['name']
        )
        previous_mis_names = [d.name for d in previous_mis]

        for row in self.overtime_details:
            current_amt = row.total or 0
            row.amount_to_be_paid = current_amt
            ot_tot += current_amt

            prev_amt = 0
            if previous_mis_names and row.description:
                prev_amt = frappe.db.sql("""
                    SELECT SUM(pp.amount_to_be_paid)
                    FROM `tabOvertime Details` pp
                    JOIN `tabMIS OT` mo ON mo.name = pp.parent
                    WHERE mo.name IN %(names)s AND pp.description = %(desc)s AND pp.unit = %(unit)s
                """, {'names': previous_mis_names, 'desc': row.description, 'unit':row.unit})[0][0] or 0

            row.previous_claim = prev_amt
            row.cumulative_amount = current_amt + prev_amt
            prev_ot += prev_amt
            cumm_ot += row.cumulative_amount

    
        self.previous_overtime = prev_ot
        self.overtime_total = ot_tot
        self.cumulative_overtime = cumm_ot
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
                monthly_unit_rate += (row.monthly_unit_rate or 0)
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
        

        
            

        

                        

            