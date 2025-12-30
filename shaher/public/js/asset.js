frappe.ui.form.on("Asset", {
    // refresh(frm) {

    // },
});

frappe.ui.form.on("Asset Finance Book", {
    // Fields
    custom_depreciation_method(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.custom_depreciation_method === "Double Declining Balance") {
            frappe.model.set_value(cdt, cdn, "depreciation_method", "Double Declining Balance");
        }
        else {
            frappe.model.set_value(cdt, cdn, "depreciation_method", "Manual");
        }
        frappe.model.set_value(cdt, cdn, "custom_rate_of_depreciation", 0);
        frappe.model.set_value(cdt, cdn, "total_number_of_depreciations", 0);
        calculate_total_number_of_depreciations(frm, cdt, cdn);
    },
    custom_rate_of_depreciation(frm, cdt, cdn) {
        calculate_total_number_of_depreciations(frm, cdt, cdn);
    },

    
});

// Calculcations and functions
function calculate_total_number_of_depreciations(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (row.custom_depreciation_method == "Written Down Value" && row.custom_rate_of_depreciation > 0) {
        frappe.call({
            method: "shaher.events.asset.get_total_no_of_depreciation",
            args: {
                opening_value: frm.doc.gross_purchase_amount,
                rate_of_depreciation: row.custom_rate_of_depreciation,
                available_for_use_date: frm.doc.available_for_use_date,
                depreciation_start_date: row.depreciation_start_date,
                frequency: row.frequency_of_depreciation,
                daily_prota_based: row.daily_prota_based,
            },
            freeze: true,
            freeze_message: "Calculating total no. of depreciations ...",
            callback(r) {
                if (r && r.message) {
                    frappe.model.set_value(cdt, cdn, "total_number_of_depreciations", r.message);
                }
            }
        })
    }
}
