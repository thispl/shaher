# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (
	add_days,
	cint,
	create_batch,
	cstr,
	flt,
	formatdate,
	get_datetime,
	get_number_format_info,
	getdate,
	now,
	nowdate,
)
from erpnext.accounts.utils import get_fiscal_year, get_currency_precision

class FiscalYearError(frappe.ValidationError):
	pass
class ProvisionalBudgeting(Document):
	pass

@frappe.whitelist()
def get_current_value(
	account=None,
	date=None,
	party_type=None,
	party=None,
	company=None,
	in_account_currency=True,
	cost_center=None,
	ignore_account_permission=False,
	account_type=None,
	start_date=None,
):
	if not account and frappe.form_dict.get("account"):
		account = frappe.form_dict.get("account")
	if not date and frappe.form_dict.get("date"):
		date = frappe.form_dict.get("date")
	if not party_type and frappe.form_dict.get("party_type"):
		party_type = frappe.form_dict.get("party_type")
	if not party and frappe.form_dict.get("party"):
		party = frappe.form_dict.get("party")
	if not cost_center and frappe.form_dict.get("cost_center"):
		cost_center = frappe.form_dict.get("cost_center")

	cond = ["is_cancelled=0"]
	if start_date:
		cond.append("posting_date >= %s" % frappe.db.escape(cstr(start_date)))
	if date:
		cond.append("posting_date <= %s" % frappe.db.escape(cstr(date)))
	else:
		# get balance of all entries that exist
		date = nowdate()

	if account:
		acc = frappe.get_doc("Account", account)

	try:
		get_fiscal_year(date, company=company, verbose=0)[1]
	except FiscalYearError:
		if getdate(date) > getdate(nowdate()):
			# if fiscal year not found and the date is greater than today
			# get fiscal year for today's date and its corresponding year start date
			get_fiscal_year(nowdate(), verbose=1)[1]
		else:
			# this indicates that it is a date older than any existing fiscal year.
			# hence, assuming balance as 0.0
			return 0.0

	if account:
		report_type = acc.report_type
	else:
		report_type = ""

	if cost_center and report_type == "Profit and Loss":
		cc = frappe.get_doc("Cost Center", cost_center)
		if cc.is_group:
			cond.append(
				f""" exists (
				select 1 from `tabCost Center` cc where cc.name = gle.cost_center
				and cc.lft >= {cc.lft} and cc.rgt <= {cc.rgt}
			)"""
			)

		else:
			cond.append(f"""gle.cost_center = {frappe.db.escape(cost_center)} """)

	if account:
		if not (frappe.flags.ignore_account_permission or ignore_account_permission):
			acc.check_permission("read")

		# different filter for group and ledger - improved performance
		if acc.is_group:
			cond.append(
				f"""exists (
				select name from `tabAccount` ac where ac.name = gle.account
				and ac.lft >= {acc.lft} and ac.rgt <= {acc.rgt}
			)"""
			)

			# If group and currency same as company,
			# always return balance based on debit and credit in company currency
			if acc.account_currency == frappe.get_cached_value("Company", acc.company, "default_currency"):
				in_account_currency = False
		else:
			cond.append(f"""gle.account = {frappe.db.escape(account)} """)

	if account_type:
		accounts = frappe.db.get_all(
			"Account",
			filters={"company": company, "account_type": account_type, "is_group": 0},
			pluck="name",
			order_by="lft",
		)

		cond.append(
			"""
			gle.account in (%s)
		"""
			% (", ".join([frappe.db.escape(account) for account in accounts]))
		)

	if party_type and party:
		cond.append(
			f"""gle.party_type = {frappe.db.escape(party_type)} and gle.party = {frappe.db.escape(party)} """
		)

	if company:
		cond.append("""gle.company = %s """ % (frappe.db.escape(company)))

	if account or (party_type and party) or account_type:
		precision = get_currency_precision()
		if in_account_currency:
			select_field = (
				"sum(round(debit_in_account_currency, %s)) - sum(round(credit_in_account_currency, %s))"
			)
		else:
			select_field = "sum(round(debit, %s)) - sum(round(credit, %s))"

		bal = frappe.db.sql(
			"""
			SELECT {}
			FROM `tabGL Entry` gle
			WHERE {}""".format(select_field, " and ".join(cond)),
			(precision, precision),
		)[0][0]
		# if bal is None, return 0
		return flt(bal)

