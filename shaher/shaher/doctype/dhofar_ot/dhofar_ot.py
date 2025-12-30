# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DHOFAROT(Document):
    def validate(self):
        if self.name:
            exist_doc = frappe.db.get_value('DHOFAR OT',{'docstatus': ['!=', 2],'name': ['!=', self.name],'invoice_from': ['<=', self.invoice_upto],'invoice_upto': ['>=', self.invoice_from]},['name'])

            if exist_doc:
                frappe.throw(
                    f'DHOFAR OT document already exists for this Period: '
                    f'<a href="/app/dhofar-ot/{exist_doc}" target="_blank">{exist_doc}</a>.',
                    title='Warning'
                )
        
        previous_mis = frappe.get_all(
            'DHOFAR OT',
            filters={
                'docstatus': 1,
                'invoice_from': ['<=', self.invoice_from],
                'name':['!=',self.name]
            },
            fields=['name']
        )
        previous_mis_names = [d.name for d in previous_mis if d.name != self.name]

        if previous_mis_names:
            for row in self.overtime_details:
                if row.description:
                    total_prev = frappe.db.sql("""
                        SELECT SUM(pp.amount_to_be_paid)
                        FROM `tabOvertime Details` pp
                        JOIN `tabDHOFAR OT` mo ON mo.name = pp.parent
                        WHERE mo.name IN %(names)s AND mo.docstatus = 1 AND pp.description = %(desc)s AND pp.unit =%(unit)s
                    """, {
                        'names': previous_mis_names,
                        'desc': row.description,
                        'unit':row.unit
                    })[0][0] or 0

                    row.previous_claim = total_prev
                    if row.amount_to_be_paid > 0:
                        row.cumulative_amount = row.amount_to_be_paid + row.previous_claim
                    else:
                        row.cumulative_amount = 0
        tot_ot=0
        previous_overtime=0
        cumulative_ot=0
        for m in self.overtime_details:
            tot = m.total or 0
            m.amount_to_be_paid = tot
            tot_ot+=tot
            if len(previous_mis)==0:
                m.cumulative_amount=tot
                cumulative_ot += m.cumulative_amount
            else:
                if previous_mis_names and m.description:
                    prev_amt = frappe.db.sql("""
                        SELECT SUM(pp.amount_to_be_paid)
                        FROM `tabOvertime Details` pp
                        JOIN `tabDHOFAR OT` mo ON mo.name = pp.parent
                        WHERE mo.name IN %(names)s AND mo.docstatus = 1 AND pp.description = %(desc)s AND pp.unit =%(unit)s
                    """, {'names': previous_mis_names, 'desc': m.description,'unit':m.unit})[0][0] or 0
                    m.previous_claim = prev_amt
                    m.cumulative_amount = tot + prev_amt
                    cumulative_ot += m.cumulative_amount
                    previous_overtime += prev_amt
                else:
                    m.cumulative_amount=tot
                    cumulative_ot += m.cumulative_amount
        self.overtime_total=tot_ot
        self.previous_overtime=previous_overtime
        self.cumulative_overtime=cumulative_ot
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
        

        
            

        

                        

            
            
        