// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Attendance Settings", {
	refresh: function(frm) {
		frm.disable_save();
	},
	onload: function(frm) {
		frm.disable_save()
	},
	process_attendance(frm){
			if (frm.doc.employee && frm.doc.from_date && frm.doc.to_date){
                console.log("yes")
				frappe.call({
					"method": "shaher.mark_attendance.mark_att_with_employee_enqueue",
					"args":{
						"from_date" : frm.doc.from_date,
						"to_date": frm.doc.to_date,
						"employee": frm.doc.employee 
					},
					freeze: true,
					freeze_message: 'Processing Attendance....',
					callback(r){
						if(r.message == "ok"){
							frappe.msgprint("Attendance is running in the background. Check again later.")
						}
					}
				})
			}
			else{
                console.log("no")
				frappe.call({
					"method": "shaher.mark_attendance.mark_att_enqueue",
					"args":{
						"from_date" : frm.doc.from_date,
						"to_date": frm.doc.to_date 
					},
					freeze: true,
					freeze_message: 'Processing Attendance....',
					callback(r){
						if(r.message == "ok"){
							frappe.msgprint("Attendance is running in the background. Check again later.")
						}
					}
				})
			}
		}
});
