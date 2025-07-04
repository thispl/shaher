// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Full and Final Settlement", {
    refresh(frm) {
		if(!frm.doc.__islocal){
	    frm.add_custom_button(__('Print'), function (){
			window.open(
				frappe.urllib.get_full_url(`/api/method/frappe.utils.print_format.download_pdf?
					doctype=${encodeURIComponent("Full and Final Settlement")}
					&name=${encodeURIComponent(frm.doc.name)}
					&format=${encodeURIComponent('Full and Final Settlement')}`)
			);
		});
	}
	},
    onload: function(frm) {
        if (frm.doc.employee) {
            frappe.call({
                method: 'shaher.custom.generate_leave_summary',
                args: {
                    date_of_joining: frm.doc.date_of_joining,
                    relieving_date: frm.doc.rdate,
                    employee: frm.doc.employee,
                },
                callback: function(r) {
                    if (r.message) {
                        frm.fields_dict.html.$wrapper.html(r.message);
                    }
                }
            });
        } else {
            frm.fields_dict.html.$wrapper.html("<p></p>");
        }
    },
    to_date: function(frm) {
        if (frm.doc.from_date && frm.doc.to_date) {
            if (frm.doc.from_date > frm.doc.to_date) {
                frm.set_value('to_date', null); 
                frappe.msgprint(__('To date should be greater than valid from date.'));
            }
        }
        if (frm.doc.from_date && frm.doc.to_date) {
            // Call the Python method to calculate the balance amount
            frappe.call({
                method: "shaher.shaher.doctype.full_and_final_settlement.full_and_final_settlement.calculate_balance_amount",  // Path to the method
                args: {
                    "employee": frm.doc.employee,
                    "from_date": frm.doc.from_date,
                    "to_date": frm.doc.to_date
                },
                callback: function(response) {
                    // Set the balance amount in the form
                    frm.set_value('balance_amount', response.message);
                }
            });
        } else {
            frm.set_value("balance_amount", "");
        }
    },
    from_date: function(frm) {
        if (frm.doc.from_date && frm.doc.to_date) {
            if (frm.doc.from_date > frm.doc.to_date) {
                frm.set_value('from_date', null);
                frappe.msgprint(__('From date cannot be greater than <b>To Date</b>'));
            }
        }
    },
	employee(frm) {
        if (frm.doc.employee){
            frappe.call({
                method:"shaher.shaher.doctype.full_and_final_settlement.full_and_final_settlement.get_years",
                args:{
                    "employee":frm.doc.employee,
                },
                callback(r){
                    frm.set_value("years",r.message)
                }
            })
        }else{
            frm.set_value('years',0)
        }
	},
});

frappe.ui.form.on("Leave Salary Details", {
    from_date: function (frm, cdt, cdn) {
        validate_and_calculate(frm, cdt, cdn);
    },
    to_date: function (frm, cdt, cdn) {
        validate_and_calculate(frm, cdt, cdn);
    }
});

function validate_and_calculate(frm, cdt, cdn) {
    const row = locals[cdt][cdn];
    const from = row.from_date;
    const to = row.to_date;
    if (!from || !to) {
        frappe.model.set_value(cdt, cdn, "days", "");
        frappe.model.set_value(cdt, cdn, "amount", "");
        return;
    }
    if (from && to) {
        if (from > to) {
            frappe.msgprint("To Date must be after From Date.");
            frappe.model.set_value(cdt, cdn, "to_date", "");
            frappe.model.set_value(cdt, cdn, "days", "");
            frappe.model.set_value(cdt, cdn, "amount", "");
        } else {
            const fromDate = frappe.datetime.str_to_obj(from);
            const toDate = frappe.datetime.str_to_obj(to);
            const diffDays = frappe.datetime.get_day_diff(toDate, fromDate) + 1;
            frappe.model.set_value(cdt, cdn, "days", diffDays);

            if (frm.doc.employee) {
                frappe.db.get_value("Employee", frm.doc.employee, "custom_basic")
                    .then(r => {
                        const basic = r.message.custom_basic || 0;
                        const amount = (basic / 365) * diffDays;
                        frappe.model.set_value(cdt, cdn, "amount", amount.toFixed(2));
                    });
            }
        }
    }
}


