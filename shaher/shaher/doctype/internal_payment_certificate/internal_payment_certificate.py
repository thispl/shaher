# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import fmt_money
from erpnext.setup.utils import get_exchange_rate

from frappe.model.document import Document


class InternalPaymentCertificate(Document):
	pass

@frappe.whitelist()
def get_report_data(sales_order_filter=None, purchase_order_filter=None, purchase_invoice_filter=None, supplier_filter=None):
	html = """
		<style>
			td {
				padding-right: 8px;
				padding-left: 8px;
				padding-top: 4px;
				padding-bottom: 4px;
			}
		</style>
			<div style="overflow-x: auto; color: white;">
				<table class="text-center" style="overflow: hidden; white-space: nowrap; margin-bottom: 50px;">
					<tr style="background-color: #e8262e; font-weight: 500; color: white;">
						<td class="border border-1 border-light" style="min-width: 100px;">S.No.</td>
						<td class="border border-1 border-light" style="min-width: 100px;">PDO PO</td>
						<td class="border border-1 border-light" style="min-width: 100px;">Item Code</td>
						<td class="border border-1 border-light" style="min-width: 100px;">Service Entry</td>
						<td class="border border-1 border-light" style="min-width: 100px;">SUTC Amount</td>
						<td class="border border-1 border-light" style="min-width: 100px;">Supplier Name</td>
						<td class="border border-1 border-light" style="min-width: 100px;">Supplier Order Number</td>
						<td class="border border-1 border-light" style="min-width: 100px;">Supplier Invoice Number</td>
						<td class="border border-1 border-light" style="min-width: 100px;">Supplier Invoice Date</td>
						<td class="border border-1 border-light" style="min-width: 100px;">Supplier Invoice Amount</td>
						<td class="border border-1 border-light" style="min-width: 100px;">Payment Status (Payables)</td>
						<td class="border border-1 border-light" style="min-width: 100px;">Payment Entry (Payables)</td>
						<td class="border border-1 border-light" style="min-width: 100px;">Paid Amount (Payables)</td>
						<td class="border border-1 border-light" style="min-width: 100px;">SUTC LPO</td>
						<td class="border border-1 border-light" style="min-width: 100px;">VAT Amount</td>
						<td class="border border-1 border-light" style="min-width: 100px;">Profit Margin</td>
						<td class="border border-1 border-light" style="min-width: 100px;">SUTC Invoice</td>
						<td class="border border-1 border-light" style="min-width: 100px;">Date of Invoice</td>
						<td class="border border-1 border-light" style="min-width: 100px;">Amount</td>
						<td class="border border-1 border-light" style="min-width: 100px;">Payment Status (Receivables)</td>
						<td class="border border-1 border-light" style="min-width: 100px;">Payment Entry (Receivables)</td>
						<td class="border border-1 border-light" style="min-width: 100px;">Paid Amount (Receivables)</td>
					</tr>
	"""	

	total_purchase_invoice_amount = 0
	total_sales_invoice_amount = 0
	total_profit_margin = 0
	total_supplier_paid_amount = 0
	total_customer_paid_amount = 0
	total_vat_amount = 0
	
	if sales_order_filter:
		sales_order = sales_order_filter
		so = frappe.get_doc("Sales Order", sales_order)
		pdo_po = so.po_no
		idx = 1
		for row in so.items:
			sales_order_item = row.name
			item_code = row.item_code
			purchase_order, purchase_order_item = get_purchase_order_details(row.name, sales_order)
			supplier_po = frappe.db.get_value("Purchase Order", purchase_order, "custom_supplier_reference_number")
			supplier = frappe.db.get_value("Purchase Order", purchase_order, "supplier")
			service_entry = get_service_entry(sales_order_item, sales_order)
			sales_invoice, sales_invoice_amount, sales_invoice_date, return_sales_invoice = get_sales_invoice_details(sales_order_item, sales_order)
			purchase_invoice, purchase_invoice_amount, purchase_invoice_date, return_purchase_invoice  = get_purchase_invoice_details(purchase_order_item, purchase_order)
			vat_amount = get_vat_amount(purchase_invoice)
			customer_payment_entry, customer_paid_amount, customer_payment_status = "", 0, "Pending"
			supplier_payment_entry, supplier_paid_amount, supplier_payment_status = "", 0, "Pending"
			if sales_invoice:
				customer_payment_entry, customer_paid_amount, customer_payment_status = get_payment_details(sales_invoice, sales_invoice_amount)
			if purchase_invoice:
				supplier_payment_entry, supplier_paid_amount, supplier_payment_status = get_payment_details(purchase_invoice, purchase_invoice_amount+vat_amount)
			profit_margin =  (sales_invoice_amount or 0) - (purchase_invoice_amount or 0)
			if not return_sales_invoice and not return_purchase_invoice:
				if not supplier_filter or supplier_filter == supplier:
					html += f"""
							<tr style="color: black;">
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{idx}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{pdo_po or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="/app/item/{item_code}">{item_code or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{service_entry or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(sales_invoice_amount, currency = so.currency) or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="/app/supplier/{supplier}">{supplier or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="/app/purchase-order/{purchase_order}">{purchase_order or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="#">{purchase_invoice or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{purchase_invoice_date or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(purchase_invoice_amount, currency = so.currency) or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{supplier_payment_status or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="/app/payment-entry/{supplier_payment_entry}">{supplier_payment_entry or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(supplier_paid_amount, currency = so.currency) or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{supplier_po or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(vat_amount, currency = so.currency) or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(profit_margin, currency = so.currency) or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="/app/sales-invoice/{sales_invoice}">{sales_invoice or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{sales_invoice_date or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(sales_invoice_amount, currency = so.currency) or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{customer_payment_status or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="/app/payment-entry/{customer_payment_entry}">{customer_payment_entry or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(customer_paid_amount, currency = so.currency) or ''}</td>
							</tr>
					"""
					currency = so.currency
					total_purchase_invoice_amount += purchase_invoice_amount or 0
					total_sales_invoice_amount += sales_invoice_amount or 0
					total_profit_margin += profit_margin or 0
					total_supplier_paid_amount += supplier_paid_amount or 0
					total_customer_paid_amount += customer_paid_amount or 0
					total_vat_amount += vat_amount or 0
					idx += 1

	if purchase_order_filter:
		purchase_order = purchase_order_filter
		po = frappe.get_doc("Purchase Order", purchase_order)
		supplier = po.supplier
		idx = 1
		for row in po.items:
			item_code = row.item_code
			sales_order = row.sales_order or po.custom_supplier_reference_number
			pdo_po = frappe.db.get_value("Sales Order", sales_order, "po_no")
			sales_order_item = row.sales_order_item

			service_entry = get_service_entry(sales_order_item, sales_order)
			sales_invoice, sales_invoice_amount, sales_invoice_date, return_sales_invoice = get_sales_invoice_details(sales_order_item, sales_order)
			purchase_invoice, purchase_invoice_amount, purchase_invoice_date, return_purchase_invoice  = get_purchase_invoice_details(row.name, purchase_order)
			vat_amount = get_vat_amount(purchase_invoice)
			customer_payment_entry, customer_paid_amount, customer_payment_status = "", 0, "Pending"
			supplier_payment_entry, supplier_paid_amount, supplier_payment_status = "", 0, "Pending"
			if sales_invoice:
				customer_payment_entry, customer_paid_amount, customer_payment_status = get_payment_details(sales_invoice, sales_invoice_amount)
			if purchase_invoice:
				supplier_payment_entry, supplier_paid_amount, supplier_payment_status = get_payment_details(purchase_invoice, purchase_invoice_amount+vat_amount)
			profit_margin =  (sales_invoice_amount or 0) - (purchase_invoice_amount or 0)
			if not return_purchase_invoice and not return_sales_invoice:
				if not supplier_filter or supplier_filter == supplier:
					html += f""""
							<tr style="color: black;">
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{idx}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{pdo_po or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="/app/item/{item_code}">{item_code or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{service_entry or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(sales_invoice_amount, currency = po.currency) or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="/app/supplier/{supplier}">{supplier or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="/app/purchase-order/{purchase_order}">{purchase_order or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="#">{purchase_invoice or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{purchase_invoice_date or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(purchase_invoice_amount, currency = po.currency) or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{supplier_payment_status or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="/app/payment-entry/{supplier_payment_entry}">{supplier_payment_entry or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(supplier_paid_amount, currency = po.currency) or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{po.custom_supplier_reference_number or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(vat_amount, currency = po.currency) or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(profit_margin, currency = po.currency) or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="/app/sales-invoice/{sales_invoice}">{sales_invoice or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{sales_invoice_date or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(sales_invoice_amount, currency = po.currency) or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{customer_payment_status or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="/app/payment-entry/{customer_payment_entry}">{customer_payment_entry or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(customer_paid_amount, currency = po.currency) or ''}</td>
							</tr>
					"""
					currency = po.currency
					total_purchase_invoice_amount += purchase_invoice_amount or 0
					total_sales_invoice_amount += sales_invoice_amount or 0
					total_profit_margin += profit_margin or 0
					total_supplier_paid_amount += supplier_paid_amount or 0
					total_customer_paid_amount += customer_paid_amount or 0
					total_vat_amount += vat_amount or 0
					idx += 1

	if purchase_invoice_filter:
		purchase_invoice = purchase_invoice_filter
		pi = frappe.get_doc("Purchase Invoice", purchase_invoice)
		idx = 1
		for row in pi.items:
			item_code = row.item_code
			purchase_order = row.purchase_order
			purchase_order_item = row.po_detail
			supplier_po = frappe.db.get_value("Purchase Order", purchase_order, "custom_supplier_reference_number")
			supplier = frappe.db.get_value("Purchase Order", purchase_order, "supplier")
			sales_order = frappe.db.get_value("Purchase Order Item", purchase_order_item, "sales_order")
			pdo_po = frappe.db.get_value("Sales Order", sales_order, "po_no")
			sales_order_item = frappe.db.get_value("Purchase Order Item", purchase_order_item, "sales_order_item")

			service_entry = get_service_entry(sales_order_item, sales_order)
			sales_invoice, sales_invoice_amount, sales_invoice_date, return_sales_invoice, = get_sales_invoice_details(sales_order_item, sales_order)
			purchase_invoice, purchase_invoice_amount, purchase_invoice_date  = pi.name, pi.grand_total, pi.posting_date
			vat_amount = get_vat_amount(purchase_invoice)
			customer_payment_entry, customer_paid_amount, customer_payment_status = "", 0, "Pending"
			supplier_payment_entry, supplier_paid_amount, supplier_payment_status = "", 0, "Pending"
			if sales_invoice:
				customer_payment_entry, customer_paid_amount, customer_payment_status = get_payment_details(sales_invoice, sales_invoice_amount)
			if purchase_invoice:
				supplier_payment_entry, supplier_paid_amount, supplier_payment_status = get_payment_details(purchase_invoice, purchase_invoice_amount)
			profit_margin =  (sales_invoice_amount or 0) - (purchase_invoice_amount or 0)
			if not return_sales_invoice and not pi.is_return:
				if not supplier_filter or supplier_filter == supplier:
					html += f""""
							<tr style="color: black;">
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{idx}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{pdo_po or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="/app/item/{item_code}">{item_code or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{service_entry or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(sales_invoice_amount, currency = pi.currency) or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="/app/supplier/{supplier}">{supplier or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="/app/purchase-order/{purchase_order}">{purchase_order or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="#">{purchase_invoice or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{purchase_invoice_date or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(purchase_invoice_amount, currency = pi.currency) or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{supplier_payment_status or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="/app/payment-entry/{supplier_payment_entry}">{supplier_payment_entry or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(supplier_paid_amount, currency = pi.currency) or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{supplier_po or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(vat_amount, currency = pi.currency) or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(profit_margin, currency = pi.currency) or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="/app/sales-invoice/{sales_invoice}">{sales_invoice or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{sales_invoice_date or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(sales_invoice_amount, currency = pi.currency) or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{customer_payment_status or ''}</td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"><a href="/app/payment-entry/{customer_payment_entry}">{customer_payment_entry or ''}</a></td>
								<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(customer_paid_amount, currency = pi.currency) or ''}</td>
							</tr>
					"""
					currency = pi.currency
					total_purchase_invoice_amount += purchase_invoice_amount or 0
					total_sales_invoice_amount += sales_invoice_amount or 0
					total_profit_margin += profit_margin or 0
					total_supplier_paid_amount += supplier_paid_amount or 0
					total_customer_paid_amount += customer_paid_amount or 0
					total_vat_amount += vat_amount or 0
					idx += 1
	if idx > 1:
		html += f"""
				<tr style="color: black; font-weight: 700;">
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;"></td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">Total</td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;"></td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"></td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(total_sales_invoice_amount, currency = currency) or ''}</td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"></td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;"></td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"></td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"></td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(total_purchase_invoice_amount, currency = currency) or ''}</td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"></td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"></td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(total_supplier_paid_amount, currency = currency) or ''}</td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"></td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;">{fmt_money(total_vat_amount, currency = currency) or ''}</td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(total_profit_margin, currency = currency) or ''}</td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"></td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"></td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(total_sales_invoice_amount, currency = currency) or ''}</td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"></td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: left;"></td>
					<td class="border border-1 border-danger" style="min-width: 100px; text-align: right;">{fmt_money(total_customer_paid_amount, currency = currency) or ''}</td>
				</tr>
			</table>
		</div>
		"""
	else:
		html = """<div style="min-height: 80%; max-height: 80%; display: flex; align-items: center; justify-content: center;">
                        <p style="text-align: center; font-size: 16px; color: #6c757d;">
                            Nothing to show
                        </p>
                    </div>"""
	return html

@frappe.whitelist()
def get_service_entry(sales_order_item, sales_order):
	delivery_note = frappe.db.sql("""
				SELECT 
					dn.service_entry_number as service_entry
				FROM
					`tabDelivery Note` dn
				INNER JOIN
					`tabDelivery Note Item` dni ON dni.parent = dn.name
				WHERE
					dn.docstatus = 1
					AND dni.so_detail = %s
					AND dni.against_sales_order = %s
				LIMIT 1
			""", (sales_order_item, sales_order), as_dict=True)

	service_entry = delivery_note[0]['service_entry'] if delivery_note else None
	return service_entry

@frappe.whitelist()
def get_sales_invoice_details(sales_order_item, sales_order):
	sales_invoice = frappe.db.sql("""
				SELECT 
					si.name as sales_invoice,
					sii.amount as amount,
					si.posting_date as date,
					si.is_return

				FROM
					`tabSales Invoice` si
				INNER JOIN
					`tabSales Invoice Item` sii ON sii.parent = si.name
				WHERE
					si.docstatus = 1
					AND sii.so_detail = %s
					AND sii.sales_order = %s
				LIMIT 1
			""", (sales_order_item, sales_order), as_dict=True)
	
	name = sales_invoice[0]['sales_invoice'] if sales_invoice else None
	amount = sales_invoice[0]['amount'] if sales_invoice else None
	date = sales_invoice[0]['date'].strftime('%d-%m-%Y') if sales_invoice else None
	is_return = sales_invoice[0]['is_return'] if sales_invoice else 0
	return name, amount, date, is_return

@frappe.whitelist()
def get_purchase_invoice_details(purchase_order_item, purchase_order):
	purchase_invoice = frappe.db.sql("""
		SELECT 
			pi.name as purchase_invoice,
			pii.amount as amount,
			pi.posting_date as date,
			pi.is_return,
			pi.supplier
		FROM
			`tabPurchase Invoice` pi
		LEFT JOIN
			`tabPurchase Invoice Item` pii ON pii.parent = pi.name
		WHERE
			pi.docstatus = 1
			AND pii.po_detail = %s
			AND pii.purchase_order = %s
	""", (purchase_order_item, purchase_order), as_dict=True)

	if purchase_invoice:
		
		# Combine names
		name = ", ".join(row['purchase_invoice'] for row in purchase_invoice if row['purchase_invoice'])
		
		# Sum amounts
		amount = sum(row['amount'] or 0 for row in purchase_invoice)
		
		# Combine dates
		date = ", ".join(row['date'].strftime('%d-%m-%Y') for row in purchase_invoice if row['date'])
		
		# Take is_return and supplier from the first row
		is_return = purchase_invoice[0]['is_return'] if purchase_invoice else 0
		supplier = purchase_invoice[0]['supplier'] if purchase_invoice else None
	else:
		name = None
		amount = None
		date = None
		is_return = 0
		supplier = None

	return name, amount, date, is_return

@frappe.whitelist()
def get_payment_details(invoice, invoice_amount):
	payment_entry = frappe.db.sql("""
					SELECT 
						pe.name as payment_entry,
						pe.paid_amount as paid_amount
					FROM
						`tabPayment Entry` pe
					INNER JOIN
						`tabPayment Entry Reference` per ON per.parent = pe.name
					WHERE
						pe.docstatus = 1
						AND per.reference_name = %s
					LIMIT 1
				""", (invoice), as_dict=True)
		
	name = payment_entry[0]['payment_entry'] if payment_entry else None
	amount = payment_entry[0]['paid_amount'] if payment_entry else None
	status = "Pending"
	if payment_entry:
		if amount == invoice_amount:
			status = "Paid"
		else:
			status = "Partly Paid"
	return name, amount, status

@frappe.whitelist()
def get_purchase_order_details(sales_order_item, sales_order):
	purchase_order = frappe.db.sql("""
					SELECT 
						po.name as purchase_order,
						poi.name as purchase_order_item
					FROM
						`tabPurchase Order` po
					INNER JOIN
						`tabPurchase Order Item` poi ON poi.parent = po.name
					WHERE
						po.docstatus = 1
						AND poi.sales_order_item = %s
						AND poi.sales_order = %s
					LIMIT 1
				""", (sales_order_item, sales_order), as_dict=True)
	name = purchase_order[0]['purchase_order'] if purchase_order else None
	purchase_order_item = purchase_order[0]['purchase_order_item'] if purchase_order else None
	return name, purchase_order_item

@frappe.whitelist()
def get_vat_amount(purchase_invoice):
	if purchase_invoice:
		purchase_invoice = purchase_invoice.split(', ')
		data = frappe.db.sql("select base_tax_amount from `tabPurchase Taxes and Charges` where parent in %s and account_head like %s", (purchase_invoice, '%vat%'), as_dict=1)
		vat = data[0]['base_tax_amount'] if data else 0
		return vat
	else:
		return 0