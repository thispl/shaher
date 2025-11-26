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
        

        
            

        

                        

            