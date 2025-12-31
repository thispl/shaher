// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Internal Payment Certificate", {
    onload(frm) {
        frappe.breadcrumbs.add("Accounting", "Internal Payment Certificate");
		frm.disable_save();
        frm.fields_dict.html.$wrapper.html(`
                    <div style="min-height: 80%; max-height: 80%; display: flex; align-items: center; justify-content: center;">
                        <p style="text-align: center; font-size: 16px; color: #6c757d;">
                            Please provide filters
                        </p>
                    </div>
                `);
    },
	refresh(frm) {
        frappe.call({
            method: "shaher.custom.back_to_back_so",
            callback: function(r) {
                if (!r.message) return;
                
                let so_list = r.message;

                frm.set_query("sales_order", () => {
                    return {
                        filters: {
                            name: ["in", so_list]
                        }
                    };
                });
            }
        });
        frappe.call({
            method: "shaher.custom.back_to_back_po",
            callback: function(r) {
                if (!r.message) return;
                
                let po_list = r.message;

                frm.set_query("purchase_order", () => {
                    return {
                        filters: {
                            name: ["in", po_list]
                        }
                    };
                });
            }
        });
        frappe.call({
            method: "shaher.custom.back_to_back_pi",
            callback: function(r) {
                if (!r.message) return;
                
                let pi_list = r.message;

                frm.set_query("purchase_invoice", () => {
                    return {
                        filters: {
                            name: ["in", pi_list]
                        }
                    };
                });
            }
        });
		frm.disable_save();
        frm.add_custom_button('Clear Filters', function() {
            frm.set_value("sales_order", "");
            frm.set_value("purchase_order", "");
            frm.set_value("purchase_invoice", "");
            frm.set_value("supplier", "");
            frm.fields_dict.html.$wrapper.html(`
                    <div style="min-height: 80%; max-height: 80%; display: flex; align-items: center; justify-content: center;">
                        <p style="text-align: center; font-size: 16px; color: #6c757d;">
                            Please provide filters
                        </p>
                    </div>
                `);
        });
        frm.add_custom_button('Generate Report', function() {
            if (frm.doc.sales_order || frm.doc.purchase_order || frm.doc.purchase_invoice) {
                frm.trigger('get_html_report');
            }
        }).css({
            'background-color': 'black',
            'color': 'white',
            'border': '1px solid black'
        });

	},
    get_html_report(frm) {
        frappe.call({
            method: "shaher.shaher.doctype.internal_payment_certificate.internal_payment_certificate.get_report_data",
            args: {
                sales_order_filter: frm.doc.sales_order,
                purchase_order_filter: frm.doc.purchase_order,
                purchase_invoice_filter: frm.doc.purchase_invoice,
                supplier_filter: frm.doc.supplier,
            },
            freeze: true,
            freee_message: "Generating Report ...",
            callback: function(r) {
                if (r.message) {
                    frm.fields_dict.html.$wrapper.html(r.message);
                }
            }
        });
    },
    sales_order: function(frm) {
        if (frm.doc.sales_order) {
            frm.set_value("purchase_order", "");
            frm.set_value("purchase_invoice", "");
        }
    },
    purchase_order: function(frm) {
        if (frm.doc.purchase_order) {
            frm.set_value("sales_order", "");
            frm.set_value("purchase_invoice", "");
        }
    },
    purchase_invoice: function(frm) {
        if (frm.doc.purchase_invoice) {
            frm.set_value("sales_order", "");
            frm.set_value("purchase_order", "");
        }
    }

});
