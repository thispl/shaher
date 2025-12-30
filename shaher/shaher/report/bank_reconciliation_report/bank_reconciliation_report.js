// File: custom_bank_reco.js

frappe.query_reports["Bank Reconciliation Report"] = {
    "filters": [
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_user_default("Company"),
            "reqd": 1
        },
        {
            "fieldname": "account",
            "label": __("Bank Account"),
            "fieldtype": "Link",
            "options": "Account",
            "get_query": function() {
                var company = frappe.query_report.get_filter_value('company');
                return {
                    filters: {
                        'account_type': 'Bank',
                        'company': company
                    }
                }
            },
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        }
    ]
};