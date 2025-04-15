// Copyright (c) 2024, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Warning Letter", {
    employee(frm) {
        frappe.call({
            method: "shaher.shaher.doctype.warning_letter.warning_letter.warning_letter_count",
            args: {
                "employee": frm.doc.employee
            },
            callback: function(r) {
                if (r.message) {
                    frm.set_value("total_waring_count", r.message);
                }
            }
        });
    },

    issue_type(frm) {
        frappe.call({
            method: "shaher.shaher.doctype.warning_letter.warning_letter.issue_type_count",
            args: {
                "employee": frm.doc.employee,
                "issue_type": frm.doc.issue_type
            },
            callback: function(r) {
                if (r.message) {
                    frm.set_value("total_issue_count", r.message)
                }
            }
        })
    }
});

