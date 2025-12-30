// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("MIS Opex", {
    
    refresh(frm) {
        




        frm.fields_dict["accommodation_table"].grid.cannot_add_rows = true;
        frm.fields_dict["accommodation_table"].grid.wrapper.find('.grid-remove-rows').hide();
        frm.fields_dict["accommodation_table"].grid.only_sortable = false;
        frm.fields_dict["accommodation_table"].refresh();
        frm.fields_dict["permanent_vehicle"].grid.cannot_add_rows = true;
        frm.fields_dict["permanent_vehicle"].grid.wrapper.find('.grid-remove-rows').hide();
        frm.fields_dict["permanent_vehicle"].grid.only_sortable = false;
        frm.fields_dict["permanent_vehicle"].refresh();
        frm.fields_dict["permanent_manpower"].grid.cannot_add_rows = true;
        frm.fields_dict["permanent_manpower"].grid.wrapper.find('.grid-remove-rows').hide();
        frm.fields_dict["permanent_manpower"].grid.only_sortable = false;
        frm.fields_dict["permanent_manpower"].refresh();
        
        if (frm.doc.__islocal){
            const currentYear = new Date().getFullYear();
            frm.set_value('year', currentYear);
            const manpowerData = [
                ["Project Manager", "Foreign", 1, 2850.000],
                ["Project Manager", "Omani", 0, 3112.900],
                ["Assistant Electrical Engineer", "Foreign", 7, 698.825],
                ["Assistant Electrical Engineer", "Omani", 10, 974.515],
                ["Protection Technician", "Foreign", 9, 408.342],
                ["Electrical Technician", "Omani", 11, 652.718],
                ["Electrical Technician", "Foreign", 9, 255.740],
                ["Over Headline Man", "Omani", 12, 597.468],
                ["Over Headline Man", "Foreign", 16, 255.740],
                ["HSE supervisor", "Omani", 1, 1073.522],
                ["Technical Coordinator", "Omani", 2, 982.550],
                ["Senior Technical Engineer", "Foreign", 1, 1419.156],
                ["Business Analyst", "Foreign", 1, 1739.304],
                ["Fire Fighting alarm system Tech", "Foreign", 11, 253.095],
                ["FF Mechanical Tech", "Omani", 5, 652.468],
                ["FF Mechanical Tech", "Foreign", 6, 253.096],
                ["AC Technicians", "Omani", 9, 669.559],
                ["AC Technicians", "Foreign", 2, 253.095],
                ["Driver", "Omani", 26, 636.476],
                ["Helper", "Omani", 15, 824.929],
                ["Helper", "Foreign", 8, 214.308],
                ["Cleaner", "Foreign", 23, 214.308],
                ["Total", "", 186, 97765.14],
            ];

            frm.clear_table("permanent_manpower");
            manpowerData.forEach(([description, employee_type, total_employees, unit_price]) => {
                let row = frm.add_child("permanent_manpower");
                row.description = `${description}`;
                row.employee_type = employee_type;
                row.total_employees = total_employees;
                row.unit_price = unit_price;
            });
            frm.refresh_field("permanent_manpower");
            const vehicleData = [
                ["Four Wheel Drive Vehicles", 5, "Muscat", 413.360],
                ["Four Wheel Drive Vehicles", 1, "Sohar", 413.360],
                ["Four Wheel Drive Vehicles", 1, "Barka", 413.360],
                ["Four Wheel Drive Vehicles", 1, "Buraimi", 413.360],
                ["Four Wheel Drive Vehicles", 1, "Ibri", 413.360],
                ["Four Wheel Drive Vehicles", 1, "S. Sharqiyah", 413.360],
                ["Four Wheel Drive Vehicles", 1, "N. Sharqiyah", 413.360],
                ["Four Wheel Drive Vehicles", 2, "Dakhaliya", 413.360],
                ["Four Wheel Drive Vehicles", 2, "Musandam", 413.360],
                ["Four Wheel Drive Vehicles", 5, "Wusat", 413.360],
                ["Four Wheel Drive Vehicles - Double Pick -up", 5, "Muscat", 283.100],
                ["Four Wheel Drive Vehicles - Double Pick -up", 4, "Sohar", 283.100],
                ["Four Wheel Drive Vehicles - Double Pick -up", 2, "Barka", 283.100],
                ["Four Wheel Drive Vehicles - Double Pick -up", 2, "Buraimi", 283.100],
                ["Four Wheel Drive Vehicles - Double Pick -up", 2, "Ibri", 283.100],
                ["Four Wheel Drive Vehicles - Double Pick -up", 2, "S. Sharqiyah", 283.100],
                ["Four Wheel Drive Vehicles - Double Pick -up", 2, "N. Sharqiyah", 283.100],
                ["Four Wheel Drive Vehicles - Double Pick -up", 2, "Dakhaliya", 283.100],
                ["Four Wheel Drive Vehicles - Double Pick -up", 4, "Musandam", 283.100],
                ["Four Wheel Drive Vehicles - Double Pick -up", 2, "Wusat", 283.100],
                ["Emergency vehicle", 1, "Muscat", 637.270],
                ["Total",0,"",0]
            ];

            frm.clear_table("permanent_vehicle");
            vehicleData.forEach(([description, total_required, region, unit_price]) => {
                let row = frm.add_child("permanent_vehicle");
                row.description = description;
                row.total_required = total_required;
                row.region = region;
                row.unit_price = unit_price;
            });
            frm.refresh_field("permanent_vehicle");
            const AccomData = [
                ["Accommodation rent (including water electricity etc.)", "Lump Sum",  10286.532 ,  1028.653],
                ['Consumables materials as per clause no. 3.11.1','Lump Sum', 454.545 , 45.455 ],["Total",0,"",0]
            ];
            frm.clear_table("accommodation_table");
            AccomData.forEach(([tools, total_required, unit_price, total_claim_this_month]) => {
                let row = frm.add_child("accommodation_table");
                row.tools = tools;
                row.total_required = total_required;
                row.unit_price = unit_price;
                row.total_claim_this_month = total_claim_this_month;
            });
            frm.refresh_field("accommodation_table");
        }

        const grid_pm = frm.fields_dict.permanent_manpower?.grid;

        if (grid_pm && grid_pm.grid_rows.length) {
            const last_row_pm = grid_pm.grid_rows[grid_pm.grid_rows.length - 1];

            last_row_pm.wrapper.css('background-color', '#f2f2f2');

            frm.doc.permanent_manpower.forEach(row => {
                if (row.idx === frm.doc.permanent_manpower.length) {
                    frappe.model.set_value(row.doctype, row.name, "read_only_row", 1);
                }
            });
        }

        const grid_acc = frm.fields_dict.accommodation_table?.grid;

        if (grid_acc && grid_acc.grid_rows.length) {
            const last_row_acc = grid_acc.grid_rows[grid_acc.grid_rows.length - 1];

            last_row_acc.wrapper.css('background-color', '#f2f2f2');

            frm.doc.accommodation_table.forEach(row => {
                if (row.idx === frm.doc.accommodation_table.length) {
                    frappe.model.set_value(row.doctype, row.name, "read_only_row", 1);
                }
            });
        }
        const grid_v = frm.fields_dict.permanent_vehicle?.grid;

        if (grid_v && grid_v.grid_rows.length) {
            const last_row_v = grid_v.grid_rows[grid_v.grid_rows.length - 1];

            last_row_v.wrapper.css('background-color', '#f2f2f2');

            frm.doc.permanent_vehicle.forEach(row => {
                if (row.idx === frm.doc.permanent_vehicle.length) {
                    frappe.model.set_value(row.doctype, row.name, "read_only_row", 1);
                }
            });
        }

  



        
    },
    invoice_from(frm) {
        if (frm.doc.invoice_from && frm.doc.invoice_upto) {
            if (frm.doc.invoice_from > frm.doc.invoice_upto) {
                frm.set_value('invoice_from', '');
                frappe.throw('Invoice From date cannot be greater than Invoice Upto Date');
            } else {
            const fromDate = frappe.datetime.str_to_obj(frm.doc.invoice_from);
            const toDate = frappe.datetime.str_to_obj(frm.doc.invoice_upto);
            const diffTime = toDate.getTime() - fromDate.getTime();
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1; 

            const tables = ["accommodation_table", "permanent_vehicle", "permanent_manpower"];
            tables.forEach(table => {
                frm.doc[table].forEach(row => {
                    row.no_of_days = diffDays;
                });
                frm.refresh_field(table);
            });
        }
        }
    },
    

    invoice_upto(frm){
        if (frm.doc.invoice_from && frm.doc.invoice_upto){
            if (frm.doc.invoice_from > frm.doc.invoice_upto){
                frm.set_value('invoice_upto','')
                frappe.throw('Invoice Upto Date must be greater than Invoice from date')
            }else {
            const fromDate = frappe.datetime.str_to_obj(frm.doc.invoice_from);
            const toDate = frappe.datetime.str_to_obj(frm.doc.invoice_upto);
            const diffTime = toDate.getTime() - fromDate.getTime();
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1; 

            const tables = ["accommodation_table", "permanent_vehicle", "permanent_manpower"];
            tables.forEach(table => {
                frm.doc[table].forEach(row => {
                    row.no_of_days = diffDays;
                });
                frm.refresh_field(table);
            });
        }
        }
    },
    month(frm) {
        set_invoice_dates_and_update_rows(frm);
    },
    year(frm) {
        set_invoice_dates_and_update_rows(frm);
    },
    show_summary(frm) {
        frappe.call({
            method: "shaher.shaher.doctype.mis_opex.mis_opex.show_summary",
            args: {
                name: frm.doc.name
            },
            callback: function (r) {
                console.log(r)
                if (r.message) {
                    frm.fields_dict.summary_total_for_manpower.$wrapper.html(r.message);
                }
            }
        });
    }


    
});

function set_invoice_dates_and_update_rows(frm) {
    const monthMap = {
        Jan: 0, Feb: 1, Mar: 2, Apr: 3, May: 4, Jun: 5,
        Jul: 6, Aug: 7, Sep: 8, Oct: 9, Nov: 10, Dec: 11
    };

    const month = frm.doc.month;
    const year = frm.doc.year;

    if (month && year && monthMap.hasOwnProperty(month)) {
        const monthIndex = monthMap[month];

        const fromDate = new Date(year, monthIndex, 1);
        const toDate = new Date(year, monthIndex + 1, 0); 

        frm.set_value('invoice_from', frappe.datetime.obj_to_str(fromDate));
        frm.set_value('invoice_upto', frappe.datetime.obj_to_str(toDate));

        
    }else{
        frm.set_value('invoice_from', '');
        frm.set_value('invoice_upto', '');

    }
}


frappe.ui.form.on('Permanent Manpower', {
    

	
	employees_provided(frm, cdt, cdn) {
        
		var row = locals[cdt][cdn];
        if (row.employees_provided>0 && row.unit_price > 0){
            row.total_claim_this_month = row.employees_provided*row.unit_price
            row.amount_to_be_paid=row.total_claim_this_month
		    frm.refresh_field('permanent_manpower')
        } 
        let total_row = null;
        let total_employees = 0;
        frm.doc.permanent_manpower.forEach(r => {
            if (r.description === "Total") {
                total_row = r;   // store total row
            } else {
                // sum only non-total rows
                total_employees += (r.employees_provided || 0);
            }
        });
        if (total_row) {
            total_row.employees_provided = total_employees;
        }
    //     if (row.description =="Total"){
    //         frm.fields_dict['permanent_manpower'].grid.update_docfield_property(
    //         'employees_provided', 
    //         'read_only',
    //         1, // value
    //         row.name // specific row
    //     );
    // }
		
	},
    no_of_absent(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.no_of_absent>0 && row.unit_price > 0){
            row.deduction_for_absent= row.unit_price/row.no_of_days*row.no_of_absent
            if (row.penalty_for_absent > 0){
                tot=row.penalty_for_absent+row.deduction_for_absent
            }else{
                tot=row.deduction_for_absent
            }
            row.total_deduction= tot
            row.amount_to_be_paid= row.amount_to_be_paid-tot
            frm.refresh_field('permanent_manpower')
        }
        let total_row = null;
        let total_employees = 0;
        let total_deduction = 0;

        frm.doc.permanent_manpower.forEach(r => {
            if (r.description === "Total") {
                total_row = r;   
            } else {
                total_employees += (r.employees_provided || 0);
                total_deduction += (r.total_deduction || 0);
            }
        });

        if (total_row) {
            total_row.no_of_absent = total_employees;
            total_row.total_deduction = total_deduction;
            const base_amount = total_row.amount_to_be_paid || 0;
            total_row.amount_to_be_paid = base_amount - total_deduction;
        }

        frm.refresh_field("permanent_manpower");

		
	},
    deduction_for_absent(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.deduction_for_absent>0){
            if (row.penalty_for_absent > 0){
                tot=row.penalty_for_absent+row.deduction_for_absent
            }else{
                tot=row.deduction_for_absent
            }
            row.total_deduction= tot
            row.amount_to_be_paid= row.amount_to_be_paid-tot
            frm.refresh_field('permanent_manpower')

        }
		
	},
    penalty_for_absent(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.penalty_for_absent>0){
            if (row.deduction_for_absent > 0){
                tot=row.penalty_for_absent+row.deduction_for_absent
            }else{
                tot=row.penalty_for_absent
            }
            row.total_deduction= tot
            row.amount_to_be_paid= row.amount_to_be_paid-tot
            frm.refresh_field('permanent_manpower')

        }
		
	},
	
})

frappe.ui.form.on('Permanent Vehicle', {
	
	total_provided(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.total_provided>0 && row.unit_price > 0){
            row.total_claim_this_month = row.total_provided*row.unit_price
            row.amount_to_be_paid=row.total_claim_this_month
		    frm.refresh_field('permanent_vehicle')
        }
		
	},
    days_of_unavailability(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.days_of_unavailability>0 && row.unit_price > 0){
            row.deduction= row.unit_price/row.no_of_days*row.days_of_unavailability
            if (row.penalty > 0){
                tot=row.penalty+row.deduction
            }else{
                tot=row.deduction
            }
            row.total_deduction= tot
            row.amount_to_be_paid= row.amount_to_be_paid-tot
            frm.refresh_field('permanent_vehicle')
        }
		
	},
    deduction(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.deduction>0){
            if (row.penalty > 0){
                tot=row.penalty+row.deduction
            }else{
                tot=row.deduction
            }
            row.total_deduction= tot
            row.amount_to_be_paid= row.amount_to_be_paid-tot
            frm.refresh_field('permanent_vehicle')

        }
		
	},
    penalty(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.penalty>0){
            if (row.deduction > 0){
                tot=row.penalty+row.deduction
            }else{
                tot=row.penalty
            }
            row.total_deduction= tot
            row.amount_to_be_paid= row.amount_to_be_paid-tot
            frm.refresh_field('permanent_vehicle')

        }
		
	},
    
	
})