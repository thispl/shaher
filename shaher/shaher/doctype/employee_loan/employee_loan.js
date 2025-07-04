// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Loan", {
    refresh(frm){
        frm.fields_dict["loan_details"].grid.cannot_add_rows = true;
        frm.fields_dict["loan_details"].grid.wrapper.find('.grid-remove-rows').hide();
        if (frm.doc.docstatus==2){
            frm.add_custom_button(__('Change Date'), function() {
                var loan = frappe.model.make_new_doc_and_get_name('Employee Loan');
                loan = locals['Employee Loan'][loan];
                loan.employee=frm.doc.employee
                loan.reason=frm.doc.reason
                loan.amount=frm.doc.amount
                loan.date=frm.doc.date
                loan.reference=frm.doc.name
                loan.date_changed=1
                loan.count=frm.doc.count
                loan.deduction=frm.doc.deduction
                $.each(frm.doc.loan_details || [], function (i, row) {
                    if (row.deducted == 1) {
                        var new_child = frappe.model.add_child(loan, 'loan_details');
                        new_child.from_date = row.from_date;
                        new_child.to_date = row.to_date;
                        new_child.deduction_amount = row.deduction_amount;
                        new_child.deducted = 1;
                        new_child.salary_slip = row.salary_slip;
                    }
                });
                
                frappe.set_route("Form", "Employee Loan",loan.name)
           
             });
        }
        
		
    },
	count(frm) {
        if (frm.doc.count){
            if(frm.doc.count > 0){
                frm.set_value('deduction',frm.doc.amount/frm.doc.count)
            }else{
                frm.set_value('deduction',0)
            }          
        }else{
            frm.set_value('deduction',0)
        }
	},
    deduction_start_from: function(frm) {
        if (frm.doc.deduction_start_from) {
            if (frm.doc.date && frm.doc.date > frm.doc.deduction_start_from) {
                frm.set_value('deduction_start_from', null);
                frappe.msgprint("Deduction start date cannot be less than Loan Given Date");
                return;
            }
            let len = frm.doc.loan_details ? frm.doc.loan_details.length : 0;
            if(frm.doc.date_changed==1){
                frappe.call({
                    method: "shaher.shaher.doctype.employee_loan.employee_loan.calculate_loan_schedule_len",
                    args: {
                        start_date: frm.doc.deduction_start_from,
                        count: frm.doc.count,
                        total_amount: frm.doc.amount,
                        // extension: frm.doc.date_changed,
                        datecount: len,
                        // ref:frm.doc.reference
                    },
                    callback: function(r) {
                        if (r.message) {
                            if (frm.doc.date_changed == 1) {
                                // Keep only deducted = 1 rows
                                frm.doc.loan_details = frm.doc.loan_details.filter(row => row.deducted == 1);
                            } else {
                                // Clear entire table
                                frm.clear_table("loan_details");
                            }
    
                            // Add new rows from the server response
                            r.message.forEach(row => {
                                let child = frm.add_child("loan_details");
                                child.from_date = row.from_date;
                                child.to_date = row.to_date;
                                child.deduction_amount = row.deduction_amount;
                                // child.balance = row.balance; // optional if returned
                            });
    
                            frm.refresh_field("loan_details");
                        }
                    }
                });
            }else{
                frappe.call({
                    method: "shaher.shaher.doctype.employee_loan.employee_loan.calculate_loan_schedule",
                    args: {
                        start_date: frm.doc.deduction_start_from,
                        count: frm.doc.count,
                        total_amount: frm.doc.amount,
                        extension: frm.doc.date_changed,
                        datecount: len
                    },
                    callback: function(r) {
                        if (r.message) {
                            if (frm.doc.date_changed == 1) {
                                // Keep only deducted = 1 rows
                                frm.doc.loan_details = frm.doc.loan_details.filter(row => row.deducted == 1);
                            } else {
                                // Clear entire table
                                frm.clear_table("loan_details");
                            }
    
                            // Add new rows from the server response
                            r.message.forEach(row => {
                                let child = frm.add_child("loan_details");
                                child.from_date = row.from_date;
                                child.to_date = row.to_date;
                                child.deduction_amount = row.deduction_amount;
                                // child.balance = row.balance; // optional if returned
                            });
    
                            frm.refresh_field("loan_details");
                        }
                    }
                });
            }
            

        }else{
            if (frm.doc.date_changed == 0) {
                frm.clear_table("loan_details");
                frm.refresh_field("loan_details");
            } else {
                let updated_rows = frm.doc.loan_details.filter(row => row.deducted == 1);            
                frm.clear_table("loan_details");
                updated_rows.forEach(row => {
                    let child = frm.add_child("loan_details");
                    child.from_date = row.from_date;
                    child.to_date = row.to_date;
                    child.deduction_amount = row.deduction_amount;
                    child.salary_slip = row.salary_slip;
                    child.deducted = row.deducted;
                    child.balance = row.balance; 
                });
                frm.refresh_field("loan_details");
            }
            
                
        }
    },

    date(frm){
        if (frm.doc.deduction_start_from){
            if (frm.doc.date){
                if (frm.doc.date > frm.doc.deduction_start_from){
                    frm.set_value('date',null)
                    frappe.msgprint("Loan Given Date cannot be greater than Deduction start date")
                }
            }
        }
    },
});
frappe.ui.form.on('Loan Details', {
    form_render: function(frm, cdt, cdn){
        frm.fields_dict.loan_details.grid.wrapper.find('.grid-delete-row').hide();
        frm.fields_dict.loan_details.grid.wrapper.find('.grid-move-row').hide();
     },
    from_date: function (frm, cdt, cdn) {
        let child = locals[cdt][cdn];
        if (child.from_date) {
            let from_date = frappe.datetime.str_to_obj(child.from_date);
            let to_date = new Date(from_date);
            to_date.setMonth(to_date.getMonth() + 1);
            to_date.setDate(to_date.getDate() - 1);
            let to_date_str = frappe.datetime.obj_to_str(to_date);
            frappe.model.set_value(cdt, cdn, 'to_date', to_date_str);
            frappe.model.set_value(cdt, cdn, 'deduction_amount', frm.doc.deduction);
        }else{
            frappe.model.set_value(cdt, cdn, 'to_date', null);
            frappe.model.set_value(cdt, cdn, 'deduction_amount', 0);
        }
    }
});

