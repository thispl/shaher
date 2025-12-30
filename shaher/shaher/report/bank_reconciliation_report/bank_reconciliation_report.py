# custom_bank_reco.py

import frappe
from frappe import _
from frappe.utils import formatdate

def execute(filters=None):
    columns, data = [], []
    
    # 1. Get the Inputs
    account = filters.get("account")
    report_date = filters.get("to_date")
    
    # 2. Get GL Balance (Row 28)
    gl_balance = frappe.db.sql("""
        SELECT sum(debit) - sum(credit) FROM `tabGL Entry` 
        WHERE account = %s AND posting_date <= %s AND is_cancelled=0
    """, (account, report_date))[0][0] or 0.0
    
    # 3. Get "Cheques issued not cleared" (Row 29)
    # Payments in system, but not reconciled in bank tool
    add_items = frappe.db.sql("""
        SELECT sum(paid_amount) FROM `tabPayment Entry`
        WHERE paid_from = %s AND posting_date <= %s 
        AND (clearance_date IS NULL OR clearance_date > %s) AND docstatus=1
    """, (account, report_date, report_date))[0][0] or 0.0

    # 4. Get "Direct Credits" (Row 31 - The Missing Link)
    # Transactions uploaded to bank tool, but not yet booked in system
    # This is the line standard ERPNext skips
    bank_account = frappe.db.get_value("Bank Account", {"account":account}, "name")
    direct_credits = frappe.db.sql("""
        SELECT sum(deposit) FROM `tabBank Transaction`
        WHERE bank_account = %s AND date <= %s 
        AND unallocated_amount > 0 AND docstatus=1
    """, (bank_account, report_date))[0][0] or 0.0

    direct_debits = frappe.db.sql("""
        SELECT sum(withdrawal) FROM `tabBank Transaction`
        WHERE bank_account = %s AND date <= %s 
        AND unallocated_amount > 0 AND docstatus=1
    """, (bank_account, report_date))[0][0] or 0.0

    # 5. Get "Cheques deposited not cleared" (Row 33)
    less_items = frappe.db.sql("""
        SELECT sum(paid_amount) FROM `tabPayment Entry`
        WHERE paid_to = %s AND posting_date <= %s 
        AND (clearance_date IS NULL OR clearance_date > %s) AND docstatus=1
    """, (account, report_date, report_date))[0][0] or 0.0

    # 6. Build the Data Rows exactly like the image
    data.append({"description": f"<b>Balance as per GL as on {formatdate(report_date)}</b>", "amount": gl_balance})
    data.append({"description": "Add: Cheques issued not cleared", "amount": add_items})
    data.append({"description": "Add: Direct Credit (Not in books)", "amount": direct_credits})
    
    # Subtotal
    subtotal = gl_balance + add_items + direct_credits
    data.append({"description": "<i>Subtotal</i>", "amount": subtotal})

    data.append({"description": "Less: Direct Debits (Not in books)", "amount": -direct_debits})
    data.append({"description": "Less: Cheques deposited not cleared", "amount": -less_items})

    # Final Bank Balance
    final_bank_balance = subtotal - less_items - direct_debits
    data.append({"description": f"<b>Balance as per Bank as on {formatdate(report_date)}</b>", "amount": final_bank_balance})

    # Define Columns
    columns = [
        {"fieldname": "description", "label": "Description", "fieldtype": "Data", "width": 400},
        {"fieldname": "amount", "label": "Amount", "fieldtype": "Currency", "width": 150}
    ]

    return columns, data