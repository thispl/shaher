import frappe
from frappe.utils import getdate, nowdate
from frappe import _  # Importing the _ function for translations

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Sales Order"), "fieldname": "sales_order", "fieldtype": "Link", "options": "Sales Order", "width": 200},
        {"label": _("Sales Invoice"), "fieldname": "sales_invoice", "fieldtype": "Link", "options": "Sales Invoice", "width": 200},
        {"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 200},
        {"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"label": _("Posting Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 200},
        {"label": _("Order Amount"), "fieldname": "order_amount", "fieldtype": "Currency", "width": 200},
        {"label": _("Invoice Amount"), "fieldname": "invoice_amount", "fieldtype": "Currency", "width": 200},
        {"label": _("Outstanding Amount"), "fieldname": "out_amount", "fieldtype": "Currency", "width": 200},
    ]

# def get_data(filters):
#     data = []
#     if not filters:
#         return data

#     # Fetching Sales Orders based on filters
#     sales_orders = frappe.db.get_all(
#         "Sales Order", 
#         filters={
#             "company": filters.get("company"),
#             "docstatus": ("!=", 2),
#             "transaction_date": ["between", [filters.get("from_date"), filters.get("to_date")]]
#         }, 
#         fields=["name", "grand_total", "customer", "transaction_date"]
#     )

#     for sales_order in sales_orders:
#         # Fetching linked Sales Invoices
#         invoices = frappe.db.get_all(
#             "Sales Invoice", 
#             filters={
#                 "sales_order": sales_order.name, 
#                 "docstatus": ("!=", 2)
#             }, 
#             fields=["name", "customer", "posting_date", "grand_total"]
#         )

#         if invoices:
#             # If there are linked invoices, calculate the total invoice amount and outstanding amount
#             total_invoice_amount = sum(invoice.grand_total for invoice in invoices)
#             outstanding_amount = sales_order.grand_total - total_invoice_amount

#             # Add Sales Order data with the calculated outstanding amount
#             data.append({
#                 "sales_order": sales_order.name,
#                 "customer": sales_order.customer,
#                 "posting_date": sales_order.transaction_date,
#                 "order_amount": sales_order.grand_total,
#                 "invoice_amount": total_invoice_amount,
#                 "out_amount": outstanding_amount,
#                 "indent": 0  # Root level for Sales Order
#             })

#             # Add each linked Sales Invoice
#             for invoice in invoices:
#                 data.append({
#                     "sales_order": invoice.name,
#                     "customer": invoice.customer,
#                     "posting_date": invoice.posting_date,
#                     "order_amount": "",  # Leave blank for Sales Invoice rows
#                     "invoice_amount": invoice.grand_total,
#                     "out_amount": "",  # Leave blank for Sales Invoice rows
#                     "indent": 1  # Child level for Sales Invoice
#                 })
#         else:
#             # If there are no linked invoices, the outstanding amount is the Sales Order amount
#             data.append({
#                 "sales_order": sales_order.name,
#                 "customer": sales_order.customer,
#                 "posting_date": sales_order.transaction_date,
#                 "order_amount": sales_order.grand_total,
#                 "invoice_amount": "",  # No invoice amount
#                 "out_amount": sales_order.grand_total,  # Outstanding amount is the full order amount
#                 "indent": 0  # Root level for Sales Order
#             })

#     return data
@frappe.whitelist()
def get_data(filters):
    data = []

    if not filters:
        return data
    sales_order_filter = filters.get("sales_order")
    project_filter = filters.get("project")
    sales_invoice_filter = filters.get("sales_invoice")
    company_filter = filters.get("company")
    if sales_invoice_filter:
        invoices = frappe.db.get_all(
            "Sales Invoice",
            filters={
                "name": sales_invoice_filter,
                "docstatus": ("!=", 2),
                **({"company": company_filter} if company_filter else {})
            },
            fields=["name", "sales_order", "customer", "posting_date", "grand_total"]
        )

        for invoice in invoices:
            # Fetch related Sales Order if present
            sales_order = frappe.db.get_value(
                "Sales Order",
                {"name": invoice.sales_order} if invoice.sales_order else {},
                ["name", "grand_total", "project"],
                as_dict=True
            )

            data.append({
                "sales_order": invoice.sales_order if invoice.sales_order else "No Linked Sales Order",
                "sales_invoice": invoice.name,
                "project": sales_order.project if sales_order else "No Project",
                "customer": invoice.customer,
                "posting_date": invoice.posting_date,
                "order_amount": sales_order.grand_total if sales_order else "",
                "invoice_amount": invoice.grand_total,
                "out_amount": sales_order.grand_total - invoice.grand_total if sales_order else "",
            })

    else:
        sales_orders = frappe.db.get_all(
            "Sales Order",
            filters={
                "company": company_filter,
                "docstatus": ("!=", 2),
                **({"name": sales_order_filter} if sales_order_filter else {}),
                **({"project": project_filter} if project_filter else {})
            },
            fields=["name", "grand_total", "customer", "transaction_date", "project"]
        )

        for sales_order in sales_orders:
            invoices = frappe.db.get_all(
                "Sales Invoice",
                filters={
                    "sales_order": sales_order.name,
                    "docstatus": ("!=", 2),
                },
                fields=["name", "customer", "posting_date", "grand_total"]
            )

            if invoices:
                for invoice in invoices:
                    data.append({
                        "sales_order": sales_order.name,
                        "sales_invoice": invoice.name,
                        "project": sales_order.project,
                        "customer": invoice.customer,
                        "posting_date": invoice.posting_date,
                        "order_amount": "",
                        "invoice_amount": invoice.grand_total,
                        "out_amount": "",
                    })
            else:
                data.append({
                    "sales_order": sales_order.name,
                    "sales_invoice": "-",
                    "project": sales_order.project,
                    "customer": sales_order.customer,
                    "posting_date": sales_order.transaction_date,
                    "order_amount": sales_order.grand_total,
                    "invoice_amount": "",
                    "out_amount": sales_order.grand_total,
                })

    return data
