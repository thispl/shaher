// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Leave Salary", {
	refresh(frm) {
		if(!frm.doc.__islocal){
	    frm.add_custom_button(__('Print'), function (){
			window.open(
				frappe.urllib.get_full_url(`/api/method/frappe.utils.print_format.download_pdf?
					doctype=${encodeURIComponent("Leave Salary")}
					&name=${encodeURIComponent(frm.doc.name)}
					&format=${encodeURIComponent('Leave Salary')}`)
			);
		});
	}
	},
	visa(frm){
			frm.set_value('total_deduction',frm.doc.visa+frm.doc.air_ticket_expense+frm.doc.course_deduction+frm.doc.others)
	},
	air_ticket_expense(frm){
			frm.set_value('total_deduction',frm.doc.visa+frm.doc.air_ticket_expense+frm.doc.course_deduction+frm.doc.others)
	},
	course_deduction(frm){
			frm.set_value('total_deduction',frm.doc.visa+frm.doc.air_ticket_expense+frm.doc.course_deduction+frm.doc.others)
	},
	others(frm){
			frm.set_value('total_deduction',frm.doc.visa+frm.doc.air_ticket_expense+frm.doc.course_deduction+frm.doc.others)
	},
});
