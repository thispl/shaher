// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Certification", {
	refresh: function (frm) {
			// Indicators
			frm.get_indicator = function() {
				if (frm.doc.status === "Active") {
					return ["Active", "green", "status,=,Active"];
				} else if (frm.doc.status === "Expiring Soon") {
					return ["Expiring Soon", "orange", "status,=,Expiring Soon"];
				} else if (frm.doc.status === "Expired") {
					return ["Expired", "red", "status,=,Expired"];
				}
				else if (frm.doc.status === "Unlimited") {
					return ["Unlimited", "yellow", "status,=,Unlimited"];
				}
				else if (frm.doc.status === "Not Renewable") {
					return ["Not Renewable", "yellow", "status,=,Not Renewable"];
				}
				return ["Unknown", "gray", "status,=,Unknown"];
			};
	
			let indicator = frm.get_indicator();
			if (indicator) {
				frm.page.set_indicator(indicator[0], indicator[1]);
			}
			// Purchase Order
			if (!frm.doc.purchase_order && !frm.doc.__islocal) {

				frm.add_custom_button(__("Create PO"), function () {
					var po_name = frappe.model.make_new_doc_and_get_name('Purchase Order');
	
					var po = locals['Purchase Order'][po_name];
					po.custom_division = "Certification Renewal";
					po.company = frm.doc.company;
					po.supplier = frm.doc.supplier;
					po.custom_employee_certification = frm.doc.name;
					
					var child = frappe.model.add_child(po, "Purchase Order Item", "items");
					child.item_code = frm.doc.certification;
					child.item_name = frm.doc.certification;
					child.qty = 1;
					child.uom = "Nos";
					child.custom_employee_certification = frm.doc.name
				
					frappe.set_route("Form", "Purchase Order", po_name);
				});
			}
			
			// Renew Certificate
			if (frm.doc.status == "Expired") {
				frm.add_custom_button(__("Renew Certificate"), function () {
					var ec = frappe.model.make_new_doc_and_get_name('Employee Certification');
					ec = locals['Employee Certification'][ec];
					ec.employee = frm.doc.employee
					ec.certification = frm.doc.certification
					ec.possibility_status = frm.doc.possibility_status
	
					frappe.set_route("Form", "Employee Certification",ec.name)
				});
			}
			
		
        
    },
    // validate(frm){
	// 	frm.trigger("days_left")
	// 	frm.trigger("last_renewal_date")
	// 	frm.trigger("possibility_status")
	// },
	// expiry_date(frm) {	
	// 	var frequency = frappe.datetime.get_diff(frm.doc.expiry_date,frm.doc.last_renewal_date)
	// 	frm.set_value("frequency_of_renewal_days", frequency);
	// 	var diff = frappe.datetime.get_diff(frm.doc.expiry_date, frappe.datetime.nowdate())
	// 		frm.set_value("days_left", diff);
	// 	frm.trigger("possibility_status")
	// },
	// renewal_frequency(frm){
	// 	frm.trigger("last_renewal_date")
	// },
	// possibility_status(frm) {
	// 	if (frm.doc.purchase_order) {

	// 		if (frm.doc.possibility_status == "Unlimited Validity") {
	// 			frm.set_value("status", "Unlimited");
	// 		} 
	// 		else if (frm.doc.possibility_status == "Not Renewable") {
	// 			frm.set_value("status", "Not Renewable");
	// 		} 
	// 		else if (frm.doc.possibility_status == "Renewable") {
	// 			if (frm.doc.days_left < 0) {
	// 				frm.set_value("status", "Expired");
	// 			} 
	// 			else if (frm.doc.days_left < 31) {
	// 				frm.set_value("status", "Expiring Soon");
	// 			} 
	// 			else {
	// 				frm.set_value("status", "Valid");
	// 			}
	// 		}
	// 	}
	// 	else {
	// 		if (frm.doc.possibility_status == "Unlimited Validity") {
	// 			frm.set_value("status", "Unlimited");
	// 		} 
	// 		else if (frm.doc.possibility_status == "Not Renewable") {
	// 			frm.set_value("status", "Not Renewable");
	// 		} 
	// 		else if (frm.doc.possibility_status == "Renewable") {
	// 			frm.set_value("status", "Due for Renewal")
	// 		}
	// 	}
	// }
	

});
