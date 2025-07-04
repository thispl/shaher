// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Financial Monitor Document", {
    valid_upto: function(frm) {
        if (frm.doc.valid_from && frm.doc.valid_upto) {
            if (frm.doc.valid_from > frm.doc.valid_upto) {
                frm.set_value('valid_upto', null); 
                frappe.msgprint(__('Valid Upto date should be greater than valid from date.'));
            }
        }
    },
    valid_from: function(frm) {
        if (frm.doc.valid_from && frm.doc.valid_upto) {
            if (frm.doc.valid_from > frm.doc.valid_upto) {
                frm.set_value('valid_from', null);
                frappe.msgprint(__('Valid from date cannot be greater than Valid Upto Date'));
            }
        }
    },
    document_date(frm) {
        const selectedDate = frappe.datetime.str_to_obj(frm.doc.document_date);
        const today = frappe.datetime.get_today();
        const todayObj = frappe.datetime.str_to_obj(today);
        if (selectedDate > todayObj) {
            frm.set_value('document_date', null); 
            frappe.msgprint(__('Document date cannot be a future date.'));
        }
        if (frm.doc.cheque_clearance_date){
            if(frm.doc.document_date){
                if (frm.doc.cheque_clearance_date <= frm.doc.document_date) {
                    frm.set_value('document_date', null); 
                    frappe.msgprint(__('Cheque clearance should be after document date.'));
                }
            }
    }
    },
    cheque_clearance_date(frm){
        if (frm.doc.cheque_clearance_date){
                if(frm.doc.document_date){
                    if (frm.doc.cheque_clearance_date <= frm.doc.document_date) {
                        frm.set_value('cheque_clearance_date', null); 
                        frappe.msgprint(__('Cheque clearance should be after document date.'));
                    }
                }
        }
    },
    status(frm){
        const today = frappe.datetime.get_today();
        if (frm.doc.status=='Issued'){
            frm.set_value('refer_date',today)
        }else{
            frm.set_value('refer_date',null)
        }
    },
	setup(frm) {
        frm.set_query("bank_account", function() {
			return {
				filters: {
					'disabled': 0,
                    'bank':frm.doc.bank_name
				}
			};
		});
        frm.set_query("party_type", function() {
			return {
				filters: {
					'name': ['in', ['Customer', 'Supplier', 'Bank']]
                    
				}
			};
		});
	},
});
