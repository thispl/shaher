// Copyright (c) 2025, Amar Karthick P and contributors
// For license information, please see license.txt

frappe.ui.form.on("PDF Reader", {
	refresh(frm) {
        frm.disable_save();
        if(frm.doc.attachment) {
        //    frappe.call({
        //         method: "shaher.shaher.doctype.pdf_reader.pdf_reader.fill_service_entry",
        //         args: {
        //             file_url: frm.doc.attachment,
        //             service_entry_text: "SES-00042",
        //             date_text: "2025-07-03"
        //         },
        //         callback(r) {
        //             if (r.message) {
        //                 frappe.msgprint(`<a href="${r.message}" target="_blank">Download Filled PDF</a>`);
        //             }
        //         }
        //     });
            // frappe.call({
            //     method: "shaher.shaher.doctype.pdf_reader.pdf_reader.generate_fillable_certificate",
            //     callback(r) {
            //         if (r.message) {
            //             frappe.msgprint(`<a href="${r.message}" target="_blank">Download Filled PDF</a>`);
            //         }
            //     }
            // });

            frappe.call({
                method: "shaher.shaher.doctype.pdf_reader.pdf_reader.generate_fillable_certificate",
                args: {
                    file_url: frm.doc.attachment,
                },
                callback(r) {
                    if (r.message) {
                        frappe.msgprint(`<a href="${r.message}" target="_blank">Download Filled PDF</a>`);
                    }
                }
            });
        }
	},
    read_data(frm) {
        
    },
});
