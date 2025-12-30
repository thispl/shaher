import frappe
from frappe.utils import flt, getdate, date_diff

def update_opening_value(doc, method):
	depreciation_start_date = frappe.db.get_value(
		"Asset", doc.asset, "available_for_use_date"
	)

	total_rows = len(doc.depreciation_schedule)
	opening_value = flt(doc.gross_purchase_amount)
	accumulated_depreciation_amount = 0
	previous_schedule_date = None
	value_after_depreciation = flt(doc.gross_purchase_amount)

	for idx, row in enumerate(doc.depreciation_schedule, start=1):
		# Number of Days
		if idx == 1:
			no_of_days = date_diff(row.schedule_date, depreciation_start_date) + 1
		elif 1 < idx < total_rows:
			no_of_days = date_diff(row.schedule_date, previous_schedule_date)
		else:
			no_of_days = date_diff(row.schedule_date, previous_schedule_date) - 1

		previous_schedule_date = row.schedule_date
		row.custom_no_of_days = no_of_days
		row.custom_opening_value = opening_value

		# Manual Depreciation
		if doc.depreciation_method == "Manual":
			depreciation_amount = (
				(opening_value * flt(doc.custom_rate_of_depreciation) / 100) / 365
			) * flt(no_of_days)

			depreciation_amount = flt(
				depreciation_amount,
				row.precision("depreciation_amount")
			)
			row.depreciation_amount = depreciation_amount

			value_after_depreciation -= depreciation_amount
			row.custom_value_after_depreciation = value_after_depreciation
   
			accumulated_depreciation_amount += depreciation_amount
			row.accumulated_depreciation_amount = accumulated_depreciation_amount
			if doc.custom_depreciation_method == "Written Down Value":
				opening_value -= depreciation_amount
