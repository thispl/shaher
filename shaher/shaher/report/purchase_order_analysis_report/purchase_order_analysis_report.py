# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import copy

import frappe
from frappe import _
from frappe.query_builder.functions import IfNull, Sum
from frappe.utils import date_diff, flt, getdate


def execute(filters=None):
	if not filters:
		return [], []

	validate_filters(filters)

	columns = get_columns(filters)
	data = get_data(filters)

	if not data:
		return [], [], None, []

	data, chart_data = prepare_data(data, filters)
 
	report_data = get_report_data(filters)

	return columns, report_data, None, chart_data


def validate_filters(filters):
	from_date, to_date = filters.get("from_date"), filters.get("to_date")

	if not from_date and to_date:
		frappe.throw(_("From and To Dates are required."))
	elif date_diff(to_date, from_date) < 0:
		frappe.throw(_("To Date cannot be before From Date."))

def get_report_data(filters):
	po = frappe.qb.DocType("Purchase Order")
	po_item = frappe.qb.DocType("Purchase Order Item")
	pi_item = frappe.qb.DocType("Purchase Invoice Item")	
	pr_item = frappe.qb.DocType("Purchase Receipt Item")
	so = frappe.qb.DocType("Sales Order")

	query = (
		frappe.qb.from_(po)
		.left_join(po_item).on(po_item.parent == po.name)
		.left_join(so).on(so.name == po_item.sales_order)
		.select(
			po.transaction_date.as_("date"),
			po.total,
			po.name.as_("purchase_order"),
			po.workflow_state,
			po.status,
			po.supplier,
			so.po_no.as_("customer_po_number"),
			po.set_warehouse.as_("warehouse"),
			po.company,  # Ensure sum is not null
		)
		.where(
			(po.status.notin(("Stopped", "Closed"))) & 
			(po.docstatus != 2) # ✅ Ensure only submitted payments are considered
		)
		.groupby(po.name)
		.orderby(po.transaction_date)
	)


	for field in ("company", "name"):
		if filters.get(field):
			query = query.where(po[field] == filters.get(field))

	if filters.get("from_date") and filters.get("to_date"):
		query = query.where(po.transaction_date.between(filters.get("from_date"), filters.get("to_date")))

	if filters.get("status"):
		query = query.where(po.status.isin(filters.get("status")))

	if filters.get("project"):
		query = query.where(po_item.project == filters.get("project"))
  
	if filters.get("supplier"):
		query = query.where(po.supplier == filters.get("supplier"))
  
	if filters.get("customer_po_number"):
		query = query.where(so.po_no.like(f"%{filters.get('customer_po_number')}%"))
  
	# if filters.get("customer_po_no"):
	# 	conditions += " AND `tabDelivery Note`.po_no LIKE '%%%s%%'" % filters.customer_po_no

	data = query.run(as_dict=True)
	report_data = []
	for row in data:
		report_data.append({
			"purchase_order": row.purchase_order,
			"qty": row.test,
			"pending_qty": row.test,
			"received_qty": row.test,
			"billed_qty": row.billed_qty,
			"qty_to_bill": row.test,
			"receieved_qty": row.test,
			"status": row.status,
			"workflow_state": row.workflow_state,
			"project": row.project,
			"supplier": row.supplier,
			"customer_po_number": row.customer_po_number,
			"amount": row.total,
			"billed_amount": get_billed_amount(row.purchase_order),
			"paid_amount": get_paid_amount(row.purchase_order),
			"advance_amount": get_advance_amount(row.purchase_order),
			"warehouse": row.warehouse,
			"pending_amount": row.total - get_billed_amount(row.purchase_order),
			"company": row.company,
			"sales_order": row.sales_order,
			"received_qty_amount": row.test,
			"indent": 0,
		})
		# po = frappe.get_doc("Purchase Order", row.purchase_order)
		query = (
			frappe.qb.from_(po)
			.inner_join(po_item)
			.on(po_item.parent == po.name)
			.left_join(pi_item)
			.on((pi_item.po_detail == po_item.name) & (pi_item.docstatus == 1))
			.left_join(pr_item)
			.on((pr_item.purchase_order_item == po_item.name) & (pr_item.docstatus == 1))
			.left_join(so)
			.on(so.name == po_item.sales_order)
			.select(
				po.transaction_date.as_("date"),
				po_item.schedule_date.as_("required_date"),
				po_item.project,
				po.name.as_("purchase_order"),
				po.workflow_state,
				po.status,
				po.supplier,
				po_item.sales_order,
				so.po_no.as_("customer_po_number"),
				po_item.item_code,
				po_item.qty,
				po_item.received_qty,
				(po_item.qty - po_item.received_qty).as_("pending_qty"),
				Sum(IfNull(pi_item.qty, 0)).as_("billed_qty"),
				po_item.base_amount.as_("amount"),
				(pr_item.base_amount).as_("received_qty_amount"),
				(po_item.billed_amt * IfNull(po.conversion_rate, 1)).as_("billed_amount"),
				(po_item.base_amount - (po_item.billed_amt * IfNull(po.conversion_rate, 1))).as_(
					"pending_amount"
				),
				po.set_warehouse.as_("warehouse"),
				po.company,
				po_item.name,
			)
			.where((po_item.parent == po.name) & (po.name == row.purchase_order) & (po.status.notin(("Stopped", "Closed"))) & (po.docstatus != 2))
			.groupby(po_item.name)
			.orderby(po.transaction_date)
		)
		data_child = query.run(as_dict=True)
		for child in data_child:
			qty_to_bill = flt(child.qty) - flt(child.billed_qty)
			report_data.append({
				"item_code": child.item_code,
				"qty": child.qty,
				"received_qty": child.received_qty,
				"billed_qty": child.billed_qty,
				"sales_order": child.sales_order,
				"pending_qty": child.pending_qty,
				"amount": child.amount,
				"qty_to_bill": qty_to_bill,
				"billed_amount": child.billed_amount,
				"pending_amount": child.pending_amount,
				"received_qty_amount": child.received_qty_amount,
				"indent": 1
			})
		
	return report_data

def get_data(filters):
	po = frappe.qb.DocType("Purchase Order")
	po_item = frappe.qb.DocType("Purchase Order Item")
	pi_item = frappe.qb.DocType("Purchase Invoice Item")
	pr_item = frappe.qb.DocType("Purchase Receipt Item")
	so = frappe.qb.DocType("Sales Order")

	query = (
		frappe.qb.from_(po)
		.inner_join(po_item)
		.on(po_item.parent == po.name)
		.left_join(pi_item)
		.on((pi_item.po_detail == po_item.name) & (pi_item.docstatus == 1))
		.left_join(pr_item)
		.on((pr_item.purchase_order_item == po_item.name) & (pr_item.docstatus == 1))
		.left_join(so)
		.on(so.name == po_item.sales_order)
		.select(
			po.transaction_date.as_("date"),
			po_item.schedule_date.as_("required_date"),
			po_item.project,
			po.name.as_("purchase_order"),
			po.workflow_state,
			po.status,
			po.supplier,
			po_item.sales_order,
			so.po_no.as_("customer_po_number"),
			po_item.item_code,
			po_item.qty,
			po_item.received_qty,
			(po_item.qty - po_item.received_qty).as_("pending_qty"),
			Sum(IfNull(pi_item.qty, 0)).as_("billed_qty"),
			po_item.base_amount.as_("amount"),
			(pr_item.base_amount).as_("received_qty_amount"),
			(po_item.billed_amt * IfNull(po.conversion_rate, 1)).as_("billed_amount"),
			(po_item.base_amount - (po_item.billed_amt * IfNull(po.conversion_rate, 1))).as_(
				"pending_amount"
			),
			po.set_warehouse.as_("warehouse"),
			po.company,
			po_item.name,
		)
		.where((po_item.parent == po.name) & (po.status.notin(("Stopped", "Closed"))) & (po.docstatus != 2))
		.groupby(po_item.name)
		.orderby(po.transaction_date)
	)

	for field in ("company", "name"):
		if filters.get(field):
			query = query.where(po[field] == filters.get(field))

	if filters.get("from_date") and filters.get("to_date"):
		query = query.where(po.transaction_date.between(filters.get("from_date"), filters.get("to_date")))

	if filters.get("status"):
		query = query.where(po.status.isin(filters.get("status")))

	if filters.get("project"):
		query = query.where(po_item.project == filters.get("project"))
  
	if filters.get("supplier"):
		query = query.where(po.supplier == filters.get("supplier"))
  
	if filters.get("customer_po_number"):
		query = query.where(so.po_no.like(f"%{filters.get('customer_po_number')}%"))
  
	# if filters.get("customer_po_no"):
	# 	conditions += " AND `tabDelivery Note`.po_no LIKE '%%%s%%'" % filters.customer_po_no

	data = query.run(as_dict=True)

	return data


def prepare_data(data, filters):
	completed, pending = 0, 0
	pending_field = "pending_amount"
	completed_field = "billed_amount"

	if filters.get("group_by_po"):
		purchase_order_map = {}

	for row in data:
		# sum data for chart
		completed += row[completed_field]
		pending += row[pending_field]

		# prepare data for report view
		row["qty_to_bill"] = flt(row["qty"]) - flt(row["billed_qty"])

		if filters.get("group_by_po"):
			po_name = row["purchase_order"]

			if po_name not in purchase_order_map:
				# create an entry
				row_copy = copy.deepcopy(row)
				purchase_order_map[po_name] = row_copy
			else:
				# update existing entry
				po_row = purchase_order_map[po_name]
				po_row["required_date"] = min(getdate(po_row["required_date"]), getdate(row["required_date"]))

				# sum numeric columns
				fields = [
					"qty",
					"received_qty",
					"pending_qty",
					"billed_qty",
					"qty_to_bill",
					"amount",
					"received_qty_amount",
					"billed_amount",
					"pending_amount",
				]
				for field in fields:
					po_row[field] = flt(row[field]) + flt(po_row[field])

	chart_data = prepare_chart_data(pending, completed)

	if filters.get("group_by_po"):
		data = []
		for po in purchase_order_map:
			data.append(purchase_order_map[po])
		return data, chart_data

	return data, chart_data


def prepare_chart_data(pending, completed):
	labels = ["Amount to Bill", "Billed Amount"]

	return {
		"data": {"labels": labels, "datasets": [{"values": [pending, completed]}]},
		"type": "donut",
		"height": 300,
	}


def get_columns(filters):
	columns = [
		# {"label": _("Date"), "fieldname": "date", "fieldtype": "Date", "width": 90},
		# {"label": _("Required By"), "fieldname": "required_date", "fieldtype": "Date", "width": 90},
		{
			"label": _("Purchase Order"),
			"fieldname": "purchase_order",
			"fieldtype": "Link",
			"options": "Purchase Order",
			"width": 200,
		},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 130},
		{"label": _("Workflow State"), "fieldname": "workflow_state", "fieldtype": "Data", "width": 130},
		{
			"label": _("Project"),
			"fieldname": "project",
			"fieldtype": "Link",
			"options": "Project",
			"width": 130,
		},
		{
			"label": _("Supplier"),
			"fieldname": "supplier",
			"fieldtype": "Link",
			"options": "Supplier",
			"width": 130,
		},
		{
			"label": _("Customer PO Number"),
			"fieldname": "customer_po_number",
			"fieldtype": "Data",
			"width": 130
		}
	]

	if not filters.get("group_by_po"):
		columns.append(
			{
				"label": _("Item Code"),
				"fieldname": "item_code",
				"fieldtype": "Link",
				"options": "Item",
				"width": 100,
			}
		)

	columns.extend(
		[
			{
				"label": _("Qty"),
				"fieldname": "qty",
				"fieldtype": "Float",
				"width": 120,
				"convertible": "qty",
			},
			{
				"label": _("Received Qty"),
				"fieldname": "received_qty",
				"fieldtype": "Float",
				"width": 120,
				"convertible": "qty",
			},
			{
				"label": _("Pending Qty"),
				"fieldname": "pending_qty",
				"fieldtype": "Float",
				"width": 80,
				"convertible": "qty",
			},
			{
				"label": _("Billed Qty"),
				"fieldname": "billed_qty",
				"fieldtype": "Float",
				"width": 80,
				"convertible": "qty",
			},
			{
				"label": _("Qty to Bill"),
				"fieldname": "qty_to_bill",
				"fieldtype": "Float",
				"width": 80,
				"convertible": "qty",
			},
			{
				"label": _("Amount"),
				"fieldname": "amount",
				"fieldtype": "Currency",
				"width": 110,
				"options": "Company:company:default_currency",
				"convertible": "rate",
			},
			{
				"label": _("Billed Amount"),
				"fieldname": "billed_amount",
				"fieldtype": "Currency",
				"width": 110,
				"options": "Company:company:default_currency",
				"convertible": "rate",
			},
			{
				"label": _("Paid Amount"),
				"fieldname": "paid_amount",
				"fieldtype": "Currency",
				"width": 110,
				"options": "Company:company:default_currency",
				"convertible": "rate",
			},
   			{
				"label": _("Advance Amount"),
				"fieldname": "advance_amount",
				"fieldtype": "Currency",
				"width": 110,
				"options": "Company:company:default_currency",
				"convertible": "rate",
			},
			{
				"label": _("Pending Amount"),
				"fieldname": "pending_amount",
				"fieldtype": "Currency",
				"width": 130,
				"options": "Company:company:default_currency",
				"convertible": "rate",
			},
			{
				"label": _("Received Qty Amount"),
				"fieldname": "received_qty_amount",
				"fieldtype": "Currency",
				"width": 130,
				"options": "Company:company:default_currency",
				"convertible": "rate",
			},
			{
				"label": _("Warehouse"),
				"fieldname": "warehouse",
				"fieldtype": "Link",
				"options": "Warehouse",
				"width": 100,
			},
			{
				"label": _("Company"),
				"fieldname": "company",
				"fieldtype": "Link",
				"options": "Company",
				"width": 100,
			},
			{
				"label": _("Sales Order"),
				"fieldname": "sales_order",
				"fieldtype": "Link",
				"options": "Sales Order",
				"width": 100
			}
		]
	)

	return columns

@frappe.whitelist()
def get_paid_amount(po):
	# Fetch all submitted Purchase Invoices linked to the PO
	pi_list = frappe.get_all(
		"Purchase Invoice",
		filters={"custom_purchase_order": po, "docstatus": 1},  # Ensure only submitted PIs
		pluck="name"
	)

	if not pi_list:
		return 0  # No payments if there are no linked Purchase Invoices

	# Convert list to SQL-friendly format
	pi_names = ", ".join(f"'{pi}'" for pi in pi_list)

	# Fetch total allocated amount from Payment Entry References
	paid_amount = frappe.db.sql(
		f"""
		SELECT SUM(per.allocated_amount) as total_paid_amount
		FROM `tabPayment Entry` pe
		INNER JOIN `tabPayment Entry Reference` per ON per.parent = pe.name
		WHERE per.reference_name IN ({pi_names}) AND pe.docstatus = 1
		""",
		as_dict=True
	)

	return paid_amount[0].get("total_paid_amount", 0) if paid_amount and paid_amount[0].get("total_paid_amount") else 0

@frappe.whitelist()
def get_advance_amount(po):
	# Fetch total allocated amount from Payment Entry References
	paid_amount = frappe.db.sql(
		"""
		SELECT SUM(per.allocated_amount) as total_paid_amount
		FROM `tabPayment Entry` pe
		INNER JOIN `tabPayment Entry Reference` per ON per.parent = pe.name
		WHERE per.reference_name = '%s' AND pe.docstatus = 1
		""" %(po),
		as_dict=True
	)

	return paid_amount[0].get("total_paid_amount", 0) if paid_amount and paid_amount[0].get("total_paid_amount") else 0

@frappe.whitelist()
def get_billed_amount(po):
	# Fetch all submitted Purchase Invoices linked to the PO
	pi_list = frappe.get_all(
		"Purchase Invoice",
		filters={"custom_purchase_order": po, "docstatus": 1},  # Ensure only submitted PIs
		pluck="name"
	)

	if not pi_list:
		return 0  # No payments if there are no linked Purchase Invoices

	# Convert list to SQL-friendly format
	pi_names = ", ".join(f"'{pi}'" for pi in pi_list)

	# Fetch total allocated amount from Payment Entry References
	paid_amount = frappe.db.sql(
		f"""
		SELECT SUM(total) as total_paid_amount
		FROM `tabPurchase Invoice`
		WHERE name IN ({pi_names}) AND docstatus != 2
		""",
		as_dict=True
	)

	return paid_amount[0].get("total_paid_amount", 0) if paid_amount and paid_amount[0].get("total_paid_amount") else 0
