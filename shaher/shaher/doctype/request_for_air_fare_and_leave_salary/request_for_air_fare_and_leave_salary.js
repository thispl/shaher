// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Request for Air Fare and Leave Salary", {
	last_leave_availed_to_date: function(frm) {
        validate_dates(frm);
        if(frm.doc.last_leave_availed_to_date && frm.doc.last_leave_availed_from_date){
        let diff = frappe.datetime.get_diff(frm.doc.last_leave_availed_to_date, frm.doc.last_leave_availed_from_date) + 1;
        frm.set_value('last_leave_availed_days', diff);
        }
        
    },
    last_leave_availed_from_date: function(frm) {
        validate_dates(frm);
        if(frm.doc.last_leave_availed_to_date && frm.doc.last_leave_availed_from_date){
        frm.trigger('last_leave_availed_to_date');
        }
    },
    leave_salary_period_from_date: function(frm) {
        validate_dates(frm);
    },
    leave_salary_period_to_date: function(frm) {
        validate_dates(frm);
    },
    air_fare_period_from_date: function(frm) {
        validate_dates(frm);
    },
    air_fare_period_to_date: function(frm) {
        validate_dates(frm);
    },
    
});



function validate_dates(frm) {
    if (frm.doc.last_leave_availed_from_date && frm.doc.last_leave_availed_to_date && frm.doc.last_leave_availed_from_date > frm.doc.last_leave_availed_to_date) {
        // frm.set_value('last_leave_availed_from_date', '');
        frm.set_value('last_leave_availed_to_date', '');
        frm.set_value('last_leave_availed_days', '');
        frappe.throw(__('From Date cannot be after To Date'));
    }
    if (frm.doc.leave_salary_period_from_date && frm.doc.leave_salary_period_to_date && frm.doc.leave_salary_period_from_date > frm.doc.leave_salary_period_to_date) {
        // frm.set_value('leave_salary_period_from_date', '');
        frm.set_value('leave_salary_period_to_date', '');
        frappe.throw(__('From Date cannot be after To Date'));
    }
    if (frm.doc.air_fare_period_from_date && frm.doc.air_fare_period_to_date && frm.doc.air_fare_period_from_date > frm.doc.air_fare_period_to_date) {
        // frm.set_value('air_fare_period_from_date', '');
        frm.set_value('air_fare_period_to_date', '');
        frappe.throw(__('From Date cannot be after To Date'));
    }
}
