import frappe
from frappe.utils import nowdate
from datetime import date
import frappe
from frappe.utils import getdate, nowdate, formatdate
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
