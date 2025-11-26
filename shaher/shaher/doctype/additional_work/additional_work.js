// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("ADDITIONAL WORK", {
	refresh(frm) {
        if(frm.doc.__islocal){
            const currentYear = new Date().getFullYear();
            frm.set_value('year', currentYear);
        }
	},
});

frappe.ui.form.on('Additional Work Details', {
	unit_qty(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.unit_qty>0 && row.unit_price > 0){
           row.total_claim_this_month=row.unit_price*row.unit_qty
            row.amount_to_be_paid= row.total_claim_this_month-row.total_deduction

        }else{
            row.amount_to_be_paid= 0

        }
        frm.refresh_field('additional_work_details')
	},
	unit_price(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.unit_qty>0 && row.unit_price>0){
           row.total_claim_this_month=row.unit_price*row.unit_qty
            row.amount_to_be_paid= row.total_claim_this_month

        }else{
            row.amount_to_be_paid= 0

        }
        frm.refresh_field('additional_work_details')
	},	
    total_deduction(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.total_deduction>0){
           
            row.amount_to_be_paid= row.total_claim_this_month-row.total_deduction

        }else{
            row.amount_to_be_paid= row.total_claim_this_month

        }
        frm.refresh_field('additional_work_details')
	},
    total_claim_this_month(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.total_deduction>0){
           
            row.total_deduction= tot
            row.amount_to_be_paid= row.total_claim_this_month-row.total_deduction
            frm.refresh_field('additional_work_details')

        }else{
            row.amount_to_be_paid= row.total_claim_this_month

        }
        frm.refresh_field('additional_work_details')

	},
	
})
