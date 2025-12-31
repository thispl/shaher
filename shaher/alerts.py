import frappe
from frappe.utils import nowdate
from datetime import date
import frappe
from frappe.utils import getdate, nowdate, formatdate
from datetime import datetime, timedelta
from erpnext.accounts.doctype.sales_invoice.sales_invoice import (
	check_if_return_invoice_linked_with_payment_entry,
	get_total_in_party_account_currency,
	is_overdue,
	unlink_inter_company_doc,
	update_linked_doc,
	validate_inter_company_party,
)
from frappe.utils import get_url
@frappe.whitelist()
def update_employee_certification_status():
    ec = frappe.get_all("Employee Certification",fields=['name','possibility_status','expiry_date'])
    for i in ec:
        if i['possibility_status'] == 'Renewable':
            next_renewal_date = i['expiry_date']
            days_left = (next_renewal_date - date.today()).days
            frappe.set_value('Employee Certification',i['name'],"days_left",days_left)
            if days_left <= 30:
                status = "Due for Renewal"
            else:
                status = "Valid"
            frappe.set_value('Employee Certification',i['name'],"status",status)

@frappe.whitelist()
def send_alert_notifications():
    send_expiry_notifications_for_driving_licence_number()
    send_expiry_notifications_for_passport()
    send_expiry_notifications_for_visa()

@frappe.whitelist()
def send_expiry_notifications_for_driving_licence_number():
    today = getdate(nowdate())
    companies = frappe.db.get_all("Company", ["name"], order_by="name")

    for company in companies:
        alert_rows_30 = []
        alert_rows_15 = []
        alert_rows_expired = []

        employees = frappe.get_all("Employee",{"status": "Active","company": company.name,"custom_driving_licence_number": ["is", "set"],"custom_driving_licence_expiry_date": ["is", "set"]},["name","employee_name","company","custom_driving_licence_number","custom_driving_licence_expiry_date"],order_by="name",)

        for emp in employees:
            expiry_date = getdate(emp.custom_driving_licence_expiry_date)
            days_diff = (expiry_date - today).days
            data = {
                "ID": emp.name,
                "employee": emp.employee_name,
                "company": emp.company,
                "driving_licence_number": emp.custom_driving_licence_number,
                "driving_licence_expiry_date": formatdate(expiry_date),
                "status": "Expired" if days_diff < 0 else f"Due in {days_diff} days",
            }
            if days_diff == 30:
                alert_rows_30.append(data)
            elif days_diff == 15:  
                alert_rows_15.append(data)
            elif 1 <= days_diff <= 0:        
                alert_rows_expired.append(data)

        if alert_rows_30:
            send_alert_email_for_driving_licence_expiry(alert_rows_30, "Upcoming Driving Licence Expiry – 30 Days Reminder")

        if alert_rows_15:
            send_alert_email_for_driving_licence_expiry(alert_rows_15, "Urgent Reminder: Driving Licence Expiry in 15 Days")

        if alert_rows_expired:
            send_alert_email_for_driving_licence_expiry(alert_rows_expired, "Critical Alert: Driving Licence Already Expired")

@frappe.whitelist()
def send_alert_email_for_driving_licence_expiry(rows, subject):
    if "30 Days" in subject:
        intro_message = "Please find below the Driving Licence records that will expire within the next 30 days. Kindly plan for timely renewal."
    elif "15 Days" in subject:
        intro_message = "Please find below the Driving Licence records that will expire within the next 15 days. Kindly plan for timely renewal."
    else:  
        intro_message = "Please find below the Driving Licence records that have already expired and require urgent renewal to maintain compliance."

    html = f"""
        <p>Dear Sir/Madam,</p>
        <p>{intro_message}</p>
        <table border=1 cellpadding=5 cellspacing=0 style="border:1px solid black; border-collapse:collapse; width:100%;">
            <thead>
                <tr style="background-color:#b81a0f; color:white; text-align:center; border:1px solid #000;">
                    <th>Employee ID</th>
                    <th>Employee Name</th>
                    <th>Company</th>
                    <th>Driving Licence Number</th>
                    <th>Expiry Date</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
    """

    for r in rows:
        html += f"""
            <tr>
                <td>{r.get('ID')}</td>
                <td>{r.get('employee')}</td>
                <td>{r.get('company')}</td>
                <td>{r.get('driving_licence_number')}</td>
                <td>{r.get('driving_licence_expiry_date')}</td>
                <td>{r.get('status')}</td>
            </tr>
        """

    html += """
            </tbody>
        </table>
        <p>Kindly take the necessary action to renew these documents in time.</p>
    """

    frappe.sendmail(
        recipients=["jothi.m@groupteampro.com"],  
        subject=subject,
        message=html,
    )


@frappe.whitelist()
def send_expiry_notifications_for_passport():
    today = getdate(nowdate())
    companies = frappe.db.get_all("Company", ["name"], order_by="name")

    for company in companies:
        alert_rows_30 = []
        alert_rows_15 = []
        alert_rows_expired = []

        employees = frappe.get_all("Employee",{"status": "Active","company": company.name,"passport_number": ["is", "set"],"valid_upto": ["is", "set"]},["name","employee_name","company","passport_number","valid_upto"],order_by="name",)


        for emp in employees:
            expiry_date = getdate(emp.valid_upto)
            days_diff = (expiry_date - today).days
            data = {
                "ID": emp.name,
                "employee": emp.employee_name,
                "company": emp.company,
                "passport_number": emp.passport_number,
                "passport_expiry_date": formatdate(expiry_date),
                "status": "Expired" if days_diff < 0 else f"Due in {days_diff} days",
            }

            if days_diff == 180:
                alert_rows_30.append(data)
            elif days_diff == 90:  
                alert_rows_15.append(data)
            elif 1 <= days_diff <= 0:        
                alert_rows_expired.append(data)

        if alert_rows_30:
            send_alert_email_for_passport_expiry(
                alert_rows_30, "Upcoming Passport Expiry – Passport Expiry in 180 Days"
            )

        if alert_rows_15:
            send_alert_email_for_passport_expiry(
                alert_rows_15, "Urgent Reminder: Passport Expiry in 90 Days"
            )

        if alert_rows_expired:
            send_alert_email_for_passport_expiry(
                alert_rows_expired, "Critical Alert: Passport Already Expired"
            )


@frappe.whitelist()
def send_alert_email_for_passport_expiry(rows, subject):
    if "180 Days" in subject:
        intro_message = "Please find below the passport records that will expire within the next 180 days. Kindly plan for timely renewal."
    elif "90 Days" in subject:
        intro_message = "Please find below the passport records that will expire within the next 90 days. Kindly plan for timely renewal."
    else: 
        intro_message = "Please find below the passport records that have already expired and require urgent renewal to maintain compliance."

    html = f"""
        <p>Dear Sir/Madam,</p>
        <p>{intro_message}</p>
        <table border=1 cellpadding=5 cellspacing=0 style="border:1px solid black; border-collapse:collapse; width:100%;">
            <thead>
                <tr style="background-color:#b81a0f; color:white; text-align:center;">
                    <th>Employee ID</th>
                    <th>Employee Name</th>
                    <th>Company</th>
                    <th>Passport Number</th>
                    <th>Expiry Date</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
    """
    for r in rows:
        html += f"""
            <tr>
                <td>{r.get('ID')}</td>
                <td>{r.get('employee')}</td>
                <td>{r.get('company')}</td>
                <td>{r.get('passport_number')}</td>
                <td>{r.get('passport_expiry_date')}</td>
                <td>{r.get('status')}</td>
            </tr>
        """
    html += """
            </tbody>
        </table>
        <p>Kindly take the necessary action to renew these documents in time.</p>
    """

    frappe.sendmail(
        # recipients=["jothi.m@groupteampro.com"], 
        recipients=["jothi.m@groupteampro.com","ho@shaherunited.com","hr@shaherunited.com","hr.coordinator@shaherunited.com","chitarasu@shaherunited.com","cm@shaherunited.com","purchase@shaherunited.com","ahad@amalpetroleum.com","ahmed@shaherunited.com"],  

        subject=subject,
        message=html,
    )

    html = f"""
        <p>Dear Sir/Madam,</p>
        <p>{intro_message}</p>
        <table border=1 cellpadding=5 cellspacing=0 style="border:1px solid black; border-collapse:collapse; width:100%;">
            <thead>
                <tr style="background-color:#b81a0f; color:white; text-align:center;">
                    <th>Employee ID</th>
                    <th>Employee Name</th>
                    <th>Company</th>
                    <th>Passport Number</th>
                    <th>Expiry Date</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
    """
    for r in rows:
        html += f"""
            <tr>
                <td>{r.get('ID')}</td>
                <td>{r.get('employee')}</td>
                <td>{r.get('company')}</td>
                <td>{r.get('passport_number')}</td>
                <td>{r.get('passport_expiry_date')}</td>
                <td>{r.get('status')}</td>
            </tr>
        """
    html += """
            </tbody>
        </table>
    """

    frappe.sendmail(
        recipients=["jothi.m@groupteampro.com","ho@shaherunited.com","hr@shaherunited.com","hr.coordinator@shaherunited.com","chitarasu@shaherunited.com","cm@shaherunited.com","purchase@shaherunited.com","ahad@amalpetroleum.com","ahmed@shaherunited.com"],  
        subject=subject,
        message=html,
    )


@frappe.whitelist()
def send_expiry_notifications_for_visa():
    today = getdate(nowdate())
    companies = frappe.db.get_all("Company", ["name"], order_by="name")

    for company in companies:
        alert_rows_30 = []
        alert_rows_15 = []
        alert_rows_expired = []

        employees = frappe.get_all("Employee",{"status": "Active","company": company.name,"custom_visa_number": ["is", "set"],"custom_visa_expiry_date": ["is", "set"],},["name", "employee_name", "company", "custom_visa_number", "custom_visa_expiry_date"],order_by="name",)

        for emp in employees:
            expiry_date = getdate(emp.custom_visa_expiry_date)
            days_diff = (expiry_date - today).days

            data = {
                "ID": emp.name,
                "employee": emp.employee_name,
                "company": emp.company,
                "visa_number": emp.custom_visa_number,
                "visa_expiry_date": formatdate(expiry_date),
                "status": "Expired" if days_diff < 0 else f"Due in {days_diff} days",
            }

            if days_diff == 45:
                alert_rows_30.append(data)
            elif days_diff == 30:  
                alert_rows_15.append(data)
            elif 1 <= days_diff <= 0:        
                alert_rows_expired.append(data)

        if alert_rows_30:
            send_alert_email_for_visa_expiry(alert_rows_30, "Upcoming Visa Expiry – 45 Days Reminder")

        if alert_rows_15:
            send_alert_email_for_visa_expiry(alert_rows_15, "Urgent Reminder: Visa Expiry in 30 Days")

        if alert_rows_expired:
            send_alert_email_for_visa_expiry(alert_rows_expired, "Critical Alert: Visa Already Expired")


@frappe.whitelist()
def send_alert_email_for_visa_expiry(rows, subject):
    if "45 Days" in subject:
        intro_message = "Please find below the Visa records that will expire within the next 45 days. Kindly plan for timely renewal."
    elif "30 Days" in subject:
        intro_message = "Please find below the Visa records that will expire within the next 30 days. Kindly plan for timely renewal."
    else: 
        intro_message = "Please find below the Visa records that have already expired and require urgent renewal to maintain compliance."

    html = f"""
        <p>Dear Sir/Madam,</p>
        <p>{intro_message}</p>
        <table border=1 cellpadding=5 cellspacing=0 style="border:1px solid black; border-collapse:collapse; width:100%;">
            <thead>
                <tr style="background-color:#b81a0f; color:white; text-align:center; border:1px solid #000;">
                    <th>Employee ID</th>
                    <th>Employee Name</th>
                    <th>Company</th>
                    <th>Visa Number</th>
                    <th>Expiry Date</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
    """

    for r in rows:
        html += f"""
            <tr>
                <td>{r.get('ID')}</td>
                <td>{r.get('employee')}</td>
                <td>{r.get('company')}</td>
                <td>{r.get('visa_number')}</td>
                <td>{r.get('visa_expiry_date')}</td>
                <td>{r.get('status')}</td>
            </tr>
        """

    html += """
            </tbody>
        </table>
    """

    frappe.sendmail(
        # recipients=["jothi.m@groupteampro.com"],
        recipients=["jothi.m@groupteampro.com","ho@shaherunited.com","hr@shaherunited.com","hr.coordinator@shaherunited.com","chitarasu@shaherunited.com","cm@shaherunited.com","purchase@shaherunited.com","ahad@amalpetroleum.com","ahmed@shaherunited.com"],  
        subject=subject,
        message=html,
    )
import frappe
from frappe.utils import getdate, nowdate, formatdate
import frappe
from frappe.utils import getdate, nowdate, formatdate
@frappe.whitelist()
def send_expiry_notifications_for_visa_on_december_1st():
    today = getdate(nowdate())
    next_year = today.year + 1
    if today.month != 12 or today.day != 1:
        return
    fiscal_year = frappe.db.get_value(
        "Fiscal Year", {"name": str(next_year)},
        ["year_start_date", "year_end_date"], as_dict=True
    )

    if not fiscal_year:
        fiscal_year_start_date = getdate(f"{next_year}-01-01")
        fiscal_year_end_date = getdate(f"{next_year}-12-31")
    else:
        fiscal_year_start_date = fiscal_year.year_start_date
        fiscal_year_end_date = fiscal_year.year_end_date

    companies = frappe.db.get_all("Company", ["name"], order_by="name")

    for company in companies:
        data = False
        company_total_cost = 0

        visa_sponsors = frappe.db.get_all(
            "Employee",
            filters={
                "status": "Active",
                "company": company.name,
                "custom_visa_number": ["is", "set"],
                "custom_visa_expiry_date": ["between", [fiscal_year_start_date, fiscal_year_end_date]],
            },
            distinct=True,
            pluck="custom_visa_sponsor",
        )

        html = f"""
        <p style="font-size:14px;">Dear Sir/Madam,</p>
        <p style="font-size:14px;">
            Below are the employees of <b>{company.name}</b> whose visas are expiring in the next fiscal year.
        </p>
        """

        if visa_sponsors:
            for sponsor in visa_sponsors:
                sponsor_doc = frappe.get_value(
                    "Visa Sponsor", sponsor,
                    ["name", "visa_expense_per_employee"],
                    as_dict=True
                )

                sponsor_name = sponsor_doc.name if sponsor_doc else "Unknown Sponsor"
                visa_cost_per_employee = sponsor_doc.visa_expense_per_employee if sponsor_doc else 0

                employees = frappe.get_all(
                    "Employee",
                    filters={
                        "status": "Active",
                        "company": company.name,
                        "custom_visa_sponsor": sponsor,
                        "custom_visa_expiry_date": ["between", [fiscal_year_start_date, fiscal_year_end_date]],
                    },
                    fields=["name", "employee_name", "custom_visa_number", "custom_visa_expiry_date"],
                    order_by="employee_name",
                )

                if not employees:
                    continue

                data = True
                sponsor_total_cost = 0

                html += f"""
                <h4 style="margin-top:30px;font-size:14px;">Visa Sponsor: {sponsor_name}</h4>
                <table border="1" cellpadding="5" cellspacing="0" style="border:1px solid black; border-collapse:collapse; width:100%;font-size:14px;">
                    <thead>
                        <tr style="background-color:#b81a0f; color:white; text-align:center;">
                            <th>Employee ID</th>
                            <th>Employee Name</th>
                            <th>Visa Number</th>
                            <th>Expiry Date</th>
                            <th>Status</th>
                            <th>Visa Cost</th>
                        </tr>
                    </thead>
                    <tbody>
                """

                for emp in employees:
                    expiry_date = getdate(emp.custom_visa_expiry_date)
                    days_diff = (expiry_date - fiscal_year_start_date).days
                    visa_cost = visa_cost_per_employee
                    sponsor_total_cost += visa_cost

                    html += f"""
                        <tr>
                            <td>{emp.name}</td>
                            <td>{emp.employee_name}</td>
                            <td>{emp.custom_visa_number}</td>
                            <td>{formatdate(expiry_date)}</td>
                            <td>{"Expired" if days_diff < 0 else f"Due in {days_diff} days"}</td>
                            <td>{visa_cost}</td>
                        </tr>
                    """

                html += f"""
                    </tbody>
                </table>
                <p style="font-size:14px;"><b>Total Estimated Visa Renewal Cost for {sponsor_name}:</b> {sponsor_total_cost}</p>
                <hr>
                """

                company_total_cost += sponsor_total_cost

                # Update sponsor doc
                existing_doc = frappe.db.exists("Visa Sponsor", {"name": sponsor_name})
                if existing_doc:
                    visa_doc = frappe.get_doc("Visa Sponsor", existing_doc)
                    visa_doc.append("expense_cost_details", {
                        "visa_expense_per_employee": visa_cost_per_employee,
                        "no_of_employees": len(employees),
                        "visa_expense": sponsor_total_cost,
                        "company": company.name,
                        "fiscal_year": next_year,
                        "fiscal_year_start_date": fiscal_year_start_date,
                        "fiscal_year_end_date": fiscal_year_end_date,
                    })
                    visa_doc.total_company_cost = company_total_cost
                    visa_doc.save(ignore_permissions=True)
                    frappe.db.commit()

        # ✅ Move this OUTSIDE the sponsor loop
        html += f"""
        <p style="font-size:14px;"><b>Overall Estimated Renewal Cost for {company.name}:</b> {company_total_cost}</p>
        """

        recipients = frappe.db.get_all(
            "Recipient Directory",
            filters={"company": company.name},
            pluck="user"
        )

        if recipients and data:
            recipients = recipients  # static for now
            subject = f"Visa Expiry Notification - {company.name} - Fiscal Year {next_year}"
            frappe.sendmail(
                recipients=recipients,
                subject=subject,
                message=html,
            )

import frappe
from frappe.utils import today
@frappe.whitelist()
def send_notifications_for_se_number_update_pending():
    from_date = today()
    to_date = today()

    companies = frappe.get_all("Company", pluck="name")

    for company in companies:
        filters = {
            "from_date": from_date,
            "to_date": to_date,
            "company": company
        }

        sql_data = get_raw_data(filters)

        # If no data for this company, move to next company
        if not sql_data:
            continue

        grouped = {}
        final_data = []

        for row in sql_data:
            key = (row.sales_order, row.delivery_note)
            grouped.setdefault(key, []).append(row)

        total_qty_all = 0
        total_amount_all = 0

        for (so, dn), items in grouped.items():
            total_qty = sum(item.qty or 0 for item in items)
            total_amount = sum(item.amount or 0 for item in items)

            total_qty_all += total_qty
            total_amount_all += total_amount

            parent_row = {
                "sales_order": so,
                "so_date": items[0].so_date,
                "customer": items[0].customer,
                "status": items[0].status,
                "delivery_note": dn,
                "dn_date": items[0].dn_date,
                "qty": total_qty,
                "amount": total_amount,
            }

            final_data.append(parent_row)

        # Add total row
        final_data.append({
            "sales_order": "Total",
            "so_date": "",
            "customer": "",
            "status": "",
            "delivery_note": "",
            "dn_date": "",
            "qty": total_qty_all,
            "amount": total_amount_all,
        })

        # Build HTML table
        html = """
            <table border="1" cellpadding="5" cellspacing="0" 
                style="border:1px solid black; border-collapse:collapse; width:100%; font-size:14px;">
                <thead>
                    <tr style="background-color:#b81a0f; color:white; text-align:center;">
                        <th>Sales Order</th>
                        <th>Order Date</th>
                        <th>Delivery Note</th>
                        <th>DN Date</th>
                        <th>Customer</th>
                        <th>Status</th>
                        <th>Qty</th>
                        <th>Amount</th>
                    </tr>
                </thead>
                <tbody>
        """
        frappe.errprint(final_data)
        for row in final_data:
            html += f"""
                <tr>
                    <td>{row['sales_order']}</td>
                    <td>{row['so_date'] or ''}</td>
                    <td>{row['delivery_note']}</td>
                    <td>{row['dn_date'] or ''}</td>
                    <td>{row['customer']}</td>
                    <td>{row['status']}</td>
                    <td style="text-align:right;">{row['qty']}</td>
                    <td style="text-align:right;">{row['amount']}</td>
                </tr>
            """

        html += "</tbody></table>"

        # Get recipients
        recipients = frappe.db.get_all(
            "Recipient Directory",
            filters={"company": company, "parent": company},
            pluck="user"
        )

        # Only send email if there are recipients
        if recipients:
            subject = f"Service Entry Number Update Pending – {company}"
            frappe.sendmail(
                recipients=recipients,
                subject=subject,
                message=html,
            )

@frappe.whitelist()
def get_raw_data(filters):
    so_conditions = [
        "dn_parent.docstatus = 1",
        "dn_parent.customer = 'Petroleum Development Oman LLC'",
        "dn_parent.company = %(company)s",
        "dn_parent.posting_date >= %(from_date)s",
        "dn_parent.posting_date <= %(to_date)s",
        "NOT dn_parent.service_entry_number"
    ]

    so_conditions_sql = " AND ".join(so_conditions)

    query = f"""
        SELECT
            so.name AS sales_order,
            so.transaction_date AS so_date,
            so.customer,
            so.status,

            dn.item_code,
            dn.item_name,
            dn_parent.name AS delivery_note,
            dn_parent.posting_date AS dn_date,

            item.item_group,
            item.custom_item_type AS item_type,
            dn.uom,
            dn.qty,
            dn.rate,
            dn.amount,

            (SELECT GROUP_CONCAT(DISTINCT si.name)
                FROM `tabSales Invoice Item` si
                WHERE si.delivery_note = dn_parent.name
                AND si.item_code = dn.item_code
                AND si.docstatus = 1
            ) AS actual_invoice_number,

            (SELECT MAX(si.posting_date)
                FROM `tabSales Invoice` si
                JOIN `tabSales Invoice Item` si_item 
                    ON si_item.parent = si.name
                WHERE si_item.delivery_note = dn_parent.name
                AND si_item.item_code = dn.item_code
                AND si.docstatus = 1
            ) AS invoice_date,

            dn_parent.service_entry_number

        FROM `tabSales Order` so
        LEFT JOIN `tabDelivery Note Item` dn 
            ON dn.against_sales_order = so.name
        LEFT JOIN `tabDelivery Note` dn_parent
            ON dn.parent = dn_parent.name 
        LEFT JOIN `tabItem` item 
            ON dn.item_code = item.name

        WHERE {so_conditions_sql}
        ORDER BY so.name, dn_parent.name, dn.idx
    """

    return frappe.db.sql(query, filters, as_dict=True)


import copy
from collections import OrderedDict

import frappe
from frappe import _, _dict
from frappe.query_builder import Criterion
from frappe.utils import cstr, getdate

from erpnext import get_company_currency, get_default_company
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
    get_accounting_dimensions,
    get_dimension_with_children,
)
from erpnext.accounts.report.financial_statements import get_cost_centers_with_children
from erpnext.accounts.report.utils import convert_to_presentation_currency, get_currency
from erpnext.accounts.utils import get_account_currency
from erpnext.accounts.report.general_ledger.general_ledger import validate_filters,validate_party,set_account_currency,get_result
import datetime

@frappe.whitelist()
def create_html_view_gl(filters=None):

    # MUST PARSE FILTERS HERE FIRST
    if isinstance(filters, str):
        filters = frappe.parse_json(filters)

    data = """
        <html>
        <head>
            <meta charset="utf-8">
            <title>General Ledger Report</title>

            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background: #f7f7f7;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    border:3px solid #f7f7f7;
                }
                tr{
                border:3px solid #f7f7f7;
                }
                th {
                    background: #e8e8e8;
                    padding: 8px;
                    border:3px solid #f7f7f7;
                }
                td {
                    padding: 8px;
                    border:3px solid #f7f7f7;
                }
            </style>
        </head>

        <body>
           
            <table>
                <thead>
                    <tr>
    """

    columns = get_gl_columns(filters)
    for col in columns:
        if not col.get("hidden"):
            data += f'<th>{col.get("label")}</th>'

    data += "</tr></thead><tbody>"

    rows = get_gl_data(filters)

    for row in rows:
        account_name = str(row.get("account", "")).replace("'", "")
        if account_name in ["Opening","Closing (Opening + Total)"]:
            continue 
        data += "<tr>"
        for col in columns:
            if not col.get("hidden"):
                field = col["fieldname"]
                value = row.get(field, "")
                if value is None:
                    value = ""

                if isinstance(value, (datetime.date, datetime.datetime)):
                    value = value.strftime("%d-%m-%Y")
                if col.get("fieldtype") in ["Currency", "Float"]:
                    precision = col.get("precision", 3)  # default 3
                    try:
                        value = f"{float(value):.{precision}f}"
                    except:
                        pass
                data += f"<td>{value}</td>"
        data += "</tr>"

    data += "</tbody></table></body></html>"

    return data

def get_gl_data(filters=None):

    if isinstance(filters, str):
        filters = frappe.parse_json(filters)

    if not filters:
        return [], []

    account_details = {}

    if filters and filters.get("print_in_account_currency") and not filters.get("account"):
        frappe.throw(_("Select an account to print in account currency"))

    for acc in frappe.db.sql("""select name, is_group from tabAccount""", as_dict=1):
        account_details.setdefault(acc.name, acc)

    if filters.get("party"):
        filters.party = frappe.parse_json(filters.get("party"))

    validate_filters(filters, account_details)

    validate_party(filters)

    filters = set_account_currency(filters)


    res = get_result(filters, account_details)
    return res

def get_gl_columns(filters=None):

    if isinstance(filters, str):
        filters = frappe.parse_json(filters)

    if filters.get("presentation_currency"):
        currency = filters["presentation_currency"]
    else:
        if filters.get("company"):
            currency = get_company_currency(filters["company"])
        else:
            company = get_default_company()
            currency = get_company_currency(company)
    
    # if filters.get("voucher_no"):
    #     reversal_of = frappe.db.get_value('Journal Entry',filters.get("voucher_no"),'reversal_of')
    columns = [
        {
            "label": _("GL Entry"),
            "fieldname": "gl_entry",
            "fieldtype": "Link",
            "options": "GL Entry",
            "hidden": 1,
        },
        {"label": _("Posting Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {
            "label": _("Account"),
            "fieldname": "account",
            "fieldtype": "Link",
            "options": "Account",
            "width": 180,
        },
        {"label": _("Chart Classification"), "fieldname": "root_type", "fieldtype": "Data","width": 150,"align": "left"}
    ]
    if filters.get("include_dimensions"):
        columns += [
            {"label": _("Cost Center"), "options": "Cost Center", "fieldname": "cost_center", "width": 100}
        ]
    columns += [
        {
            "label": _("Debit ({0})").format(currency),
            "fieldname": "debit",
            "fieldtype": "Float",
            "width": 130,
            "precision": 3

        },
        {
            "label": _("Credit ({0})").format(currency),
            "fieldname": "credit",
            "fieldtype": "Float",
            "width": 130,
            "precision": 3

        },
        {
            "label": _("Balance ({0})").format(currency),
            "fieldname": "balance",
            "fieldtype": "Float",
            "width": 130,
            "precision": 3

        },
    ]

    if filters.get("add_values_in_transaction_currency"):
        columns += [
            {
                "label": _("Debit (Transaction)"),
                "fieldname": "debit_in_transaction_currency",
                "fieldtype": "Currency",
                "width": 130,
                "options": "transaction_currency",
            },
            {
                "label": _("Credit (Transaction)"),
                "fieldname": "credit_in_transaction_currency",
                "fieldtype": "Currency",
                "width": 130,
                "options": "transaction_currency",
            },
            {
                "label": "Transaction Currency",
                "fieldname": "transaction_currency",
                "fieldtype": "Link",
                "options": "Currency",
                "width": 70,
            },
        ]

    columns += [
        {"label": _("Voucher Type"), "fieldname": "voucher_type", "width": 120,"hidden": filters.get("voucher_no", "").startswith("ACC")},
        {
            "label": _("Voucher Subtype"),
            "fieldname": "voucher_subtype",
            "fieldtype": "Data",
            "width": 180,
            "hidden": filters.get("voucher_no", "").startswith("ACC")
        },
        {
            "label": _("Voucher No"),
            "fieldname": "voucher_no",
            "fieldtype": "Dynamic Link",
            "options": "voucher_type",
            "width": 180,
            "hidden": filters.get("voucher_no", "").startswith("ACC") 

        },
        {"label": _("Against Account"), "fieldname": "against", "width": 120,"hidden": filters.get("voucher_no", "").startswith("ACC")},
        
        {"label": _("Party Type"), "fieldname": "party_type", "width": 100,"hidden": filters.get("voucher_no", "").startswith("ACC")},
        {"label": _("Party"), "fieldname": "party", "width": 100, "hidden": filters.get("voucher_no", "").startswith("ACC")},
    ]

    if filters.get("include_dimensions"):
        columns.append({"label": _("Project"), "options": "Project", "fieldname": "project", "width": 100,})

        for dim in get_accounting_dimensions(as_list=False):
            columns.append(
                {"label": _(dim.label), "options": dim.label, "fieldname": dim.fieldname, "width": 100,"hidden": filters.get("voucher_no", "").startswith("ACC")}
            )
        # columns.append(
        # 	{"label": _("Cost Center"), "options": "Cost Center", "fieldname": "cost_center", "width": 100}
        # )

    columns.extend(
        [
            {"label": _("Against Voucher Type"), "fieldname": "against_voucher_type", "width": 100,"hidden": filters.get("voucher_no", "").startswith("ACC")},
            {
                "label": _("Against Voucher"),
                "fieldname": "against_voucher",
                "fieldtype": "Dynamic Link",
                "options": "against_voucher_type",
                "width": 100,
                "hidden": filters.get("voucher_no", "").startswith("ACC")
            },
            {"label": _("Supplier Invoice No"), "fieldname": "bill_no", "fieldtype": "Data", "width": 100,"hidden": filters.get("voucher_no", "").startswith("ACC")},
            
        ]
    )

    if filters.get("show_remarks"):
        columns.extend([{"label": _("Remarks"), "fieldname": "remarks", "width": 400,"hidden": filters.get("voucher_no", "").startswith("ACC") }])

    return columns


@frappe.whitelist()
def payment_due_alert_pi():
    yesterday = (datetime.today()).date()

    pis = frappe.db.sql("""
        SELECT
            pi.name, pi.supplier, pi.due_date, pi.outstanding_amount, pi.company
        FROM
            `tabPurchase Invoice` pi
        WHERE
            pi.docstatus = 1
            AND pi.status != 'Paid'
            AND pi.due_date = %s
            AND EXISTS (
                SELECT 1 FROM `tabPurchase Invoice Item` pii
                WHERE pii.parent = pi.name AND pii.sales_order IS NOT NULL AND pii.sales_order != ''
            )
    """, (yesterday,), as_dict=True)

    if not pis:
        return

    site = frappe.utils.get_url()

    for pi in pis:
        users = frappe.db.sql("""
            SELECT DISTINCT u.email
            FROM `tabUser` u
            INNER JOIN `tabEmployee` e ON u.name = e.user_id
            INNER JOIN `tabHas Role` hr ON hr.parent = u.name
            WHERE e.company = %s
              AND hr.role = 'Accounts User'
              AND u.enabled = 1
              AND u.email IS NOT NULL
        """, (pi.company,), as_dict=True)

        recipients = [u.email for u in users if u.email]
        if not recipients:
            continue

        link = f"{site}/app/purchase-invoice/{pi.name}"

        message = f"""
            <b>Purchase Invoice Payment Pending</b><br><br>
            <b>Invoice:</b> <a href="{link}" target="_blank">{pi.name}</a><br>
            <b>Company:</b> {pi.company}<br>
            <b>Supplier:</b> {pi.supplier}<br>
            <b>Outstanding:</b> {pi.outstanding_amount}<br>
            <b>Due Date:</b> {pi.due_date}<br><br>
            Please process the payment.
        """

        frappe.sendmail(
            recipients='pavithra.s@groupteampro.com',
            subject=f"Payment Due Alert - {pi.name}",
            message=message
        )

@frappe.whitelist()
def payment_due_alert_si():
    yesterday = (datetime.today() - timedelta(days=1)).date()
    site = frappe.utils.get_url()

    sis = frappe.db.sql("""
        SELECT
            si.name, si.customer, si.company, si.due_date, si.outstanding_amount
        FROM `tabSales Invoice` si
        WHERE si.docstatus = 1
          AND si.status != 'Paid'
          AND si.due_date = %s
          AND EXISTS (
                SELECT 1 FROM `tabSales Invoice Item` sii
                WHERE sii.parent = si.name
                  AND sii.sales_order IS NOT NULL AND sii.sales_order != ''
          )
    """, (yesterday,), as_dict=True)

    if not sis:
        return

    for si in sis:
        so_link = frappe.db.get_value(
            "Sales Invoice Item",
            {"parent": si.name, "sales_order": ["!=", ""]},
            "sales_order"
        )
        if not so_link:
            continue

        po_exists = frappe.db.get_value(
            "Purchase Order Item",
            {"sales_order": so_link},
            "parent"
        )
        if not po_exists:
            continue  

        users = frappe.db.sql("""
            SELECT DISTINCT u.email
            FROM `tabUser` u
            INNER JOIN `tabEmployee` e ON u.name = e.user_id
            INNER JOIN `tabHas Role` hr ON hr.parent = u.name
            WHERE e.company = %s
              AND hr.role = 'Accounts User'
              AND u.enabled = 1
              AND u.email IS NOT NULL
        """, (si.company,), as_dict=True)

        recipients = [u.email for u in users if u.email]
        if not recipients:
            continue

        link = f"{site}/app/sales-invoice/{si.name}"

        msg = f"""
            <b>Sales Invoice Payment Overdue</b><br><br>
            <b>Invoice:</b> <a href="{link}" target="_blank">{si.name}</a><br>
            <b>Company:</b> {si.company}<br>
            <b>Customer:</b> {si.customer}<br>
            <b>Outstanding:</b> {si.outstanding_amount}<br>
            <b>Due Date:</b> {si.due_date}<br><br>
            Please follow up and clear the payment.
        """

        frappe.sendmail(
            recipients='pavithra.s@groupteampro.com',
            subject=f"Overdue SI Payment Alert - {si.name}",
            message=msg
        )


def pi_paid_notification(doc, method):
    for ref in doc.references:
        if ref.reference_doctype != "Purchase Invoice":
            continue

        pi_name = ref.reference_name

        inv = frappe.db.get_value(
            "Purchase Invoice",
            pi_name,
            ["outstanding_amount", "supplier", "company", "status"],
            as_dict=True
        )
        if not inv:
            continue

        if inv.outstanding_amount > 0 or inv.status != "Paid":
            continue

        po_link = frappe.db.get_value(
            "Purchase Invoice Item",
            {"parent": pi_name, "purchase_order": ["!=", ""]},
            "purchase_order"
        )
        if not po_link:
            continue

        so_link = frappe.db.get_value(
            "Purchase Order Item",
            {"parent": po_link, "sales_order": ["!=", ""]},
            "sales_order"
        )
        if not so_link:
            continue

        users = frappe.db.sql("""
            SELECT DISTINCT u.email
            FROM `tabUser` u
            INNER JOIN `tabEmployee` e ON e.user_id = u.name
            INNER JOIN `tabHas Role` hr ON hr.parent = u.name
            WHERE e.company = %s
              AND hr.role = 'Accounts User'
              AND u.enabled = 1
              AND u.email IS NOT NULL
        """, (inv.company,), as_dict=True)

        emails = [u.email for u in users]
        if not emails:
            continue

        link = f"{get_url()}/app/purchase-invoice/{pi_name}"
        msg = f"""
            <b>Purchase Invoice Payment Completed</b><br><br>
            <b>Invoice:</b> <a href="{link}" target="_blank">{pi_name}</a><br>
            <b>Company:</b> {inv.company}<br>
            <b>Supplier:</b> {inv.supplier}<br>
            <b>Total Cleared:</b> {doc.paid_amount}<br><br>
            Payment completed. PO was created from a Sales Order.
        """

        frappe.sendmail(
            recipients='pavithra.s@groupteampro.com',
            subject=f"PI Payment Completed - {pi_name}",
            message=msg
        )

@frappe.whitelist()
def si_paid_notification(doc, method):
    for ref in doc.references:
        if ref.reference_doctype != "Sales Invoice":
            continue

        si_name = ref.reference_name

        si = frappe.db.get_value(
            "Sales Invoice",
            si_name,
            ["outstanding_amount", "customer", "company", "status","grand_total"],
            as_dict=True
        )
        if not si:
            continue

        if si.outstanding_amount > 0 or si.status != "Paid":
            continue

        so_link = frappe.db.get_value(
            "Sales Invoice Item",
            {"parent": si_name, "sales_order": ["!=", ""]},
            "sales_order"
        )
        if not so_link:
            continue 

        po_exists = frappe.db.get_value(
            "Purchase Order Item",
            {"sales_order": so_link},
            "parent"
        )
        if not po_exists:
            continue 

        users = frappe.db.sql("""
            SELECT DISTINCT u.email
            FROM `tabUser` u
            INNER JOIN `tabEmployee` e ON e.user_id = u.name
            INNER JOIN `tabHas Role` hr ON hr.parent = u.name
            WHERE e.company = %s
              AND hr.role = 'Accounts User'
              AND u.enabled = 1
              AND u.email IS NOT NULL
        """, (si.company,), as_dict=True)

        emails = [u.email for u in users]
        if not emails:
            continue

        link = f"{get_url()}/app/sales-invoice/{si_name}"
        cleared_amount = ref.allocated_amount  

        msg = f"""
            <b>Sales Invoice Payment Completed</b><br><br>
            <b>Invoice:</b> <a href="{link}" target="_blank">{si_name}</a><br>
            <b>Company:</b> {si.company}<br>
            <b>Customer:</b> {si.customer}<br>
            <b>Total Cleared:</b> {si.grand_total}<br><br>
        """

        frappe.sendmail(
            recipients='pavithra.s@groupteampro.com',
            subject=f"SI Payment Completed - {si_name}",
            message=msg
        )

