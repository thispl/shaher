// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.query_reports["Salary Register Report"] = {
	"filters": [
		{
			"label": __("From Date"),
			"fieldname": "from_date",
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.month_start()
		},
		{
			"label": __("To Date"),
			"fieldname": "to_date",
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.month_end()
		},
		{
			"label": __("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company"
		},
		{
			"label": __("Employee"),
			"fieldname": "employee",
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"label": __("Division"),
			"fieldname": "division",
			"fieldtype": "Link",
			"options": "Division"
		},
	]

};
