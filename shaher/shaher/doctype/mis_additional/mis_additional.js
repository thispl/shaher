// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("MIS ADDITIONAL", {
    refresh(frm) {
        if (!frm.doc.__islocal && frm.doc.docstaus != 2){
            frm.add_custom_button(__('Create Additional Work'), function () {
            newdoc = frappe.model.make_new_doc_and_get_name('ADDITIONAL WORK');
            newdoc = locals['ADDITIONAL WORK'][newdoc];
            newdoc.against = 'MIS ADDITIONAL'; 
            newdoc.additional_work_against = 'MIS';
            newdoc.reference_id = frm.doc.name;
            newdoc.month=frm.doc.month;
            newdoc.year=frm.doc.year;
            newdoc.invoice_from=frm.doc.invoice_from;
            newdoc.invoice_upto=frm.doc.invoice_upto;
            frappe.set_route("Form", "ADDITIONAL WORK", newdoc.name);
            });
        }
        frm.fields_dict["base_vehicle"].grid.cannot_add_rows = true;
        frm.fields_dict["base_vehicle"].grid.wrapper.find('.grid-remove-rows').hide();
        frm.fields_dict["base_vehicle"].grid.only_sortable = false;
        frm.fields_dict["base_vehicle"].refresh();
        frm.fields_dict["base_vehicle_cost_per_trip"].grid.cannot_add_rows = true;
        frm.fields_dict["base_vehicle_cost_per_trip"].grid.wrapper.find('.grid-remove-rows').hide();
        frm.fields_dict["base_vehicle_cost_per_trip"].grid.only_sortable = false;
        frm.fields_dict["base_vehicle_cost_per_trip"].refresh();
        
        
        if (frm.doc.__islocal){
            const currentYear = new Date().getFullYear();
            frm.set_value('year', currentYear);
            
            const vehicleData = [
                ["(Hiab) 3 TON", 200.000],
                ["(Hiab) 5 TON", 250.000],
                ["(Hiab) 10 TON & Above", 125.000],
                ["Emergency vehicle", 250.000],
                ["Crane 25 TON", 250.000],
                ["Crane 50 TON", 300.000],
                ["Crane 100 TON & Above", 900.000],
                ["Washing Skid", 125.000],
                ["Canter 5 Ton", 60.000],
                ["Low Bed trailer", 250.000],
                ["Flat Bed trailer", 250.000],
                ["JCB", 125.000],
                ["Shovel", 200.000],
                ["Grader", 250.000],
                ["Excavator", 220.000],
                ["Bucket truck", 250.000],
                ["Cable Puller Machine", 200.000],
                ["Conductor stringing machine suitable for 132kV, 220kV & 400kV", 400.000],
                ["Winch Machine 10 Ton", 350.000],
                ["Portable Diesel Generator (350 KVA)", 150.000],
                ["Sag Bridge up to 400kV.", 30.000],
                ["Man lifter machine", 150.000],
                ["Cable Jack", 50.000],
                ["Welding set Potable", 65.000],
                ["Hydraulic crimping tool suitable for 132kV, 220kV & 400 kV", 150.000],
                ["OHL Trolly (cycle) suitable for 132kV, 220kV & 400 kV", 20.000],
                ["Come Along Clamps suitable for 132kV, 220kV & 400 kV.", 5.000],
                ["Lever chain hoist suitable for 132kV, 220kV & 400 kV.", 5.000],
                ["Snatch block 1 Ton", 2.000],
                ["Snatch block 2 Ton", 2.000],
                ["Snatch block 3 Ton", 2.000],
                ["Snatch block 6 Ton", 5.000]
                ];


            frm.clear_table("base_vehicle");
            vehicleData.forEach(([description, unit_price]) => {
                let row = frm.add_child("base_vehicle");
                row.description = description;
                row.unit_price = unit_price;
            });
            frm.refresh_field("base_vehicle");
            const vehiclepertrip = [
                ["Water tanker 650 Gallon for GS", 20.000],
                ["Water tanker 1300 Gallon for GS", 40.000],
                ["Water tanker 5000 Gallon for GS", 90.000],
                ["Water tanker 10000 Gallon for GS", 200.000],
                ["Drainage tanker 5000 Gallon for GS", 90.000]
            ];
            
            frm.clear_table("base_vehicle_cost_per_trip");
            vehiclepertrip.forEach(([ description,unit_price]) => {
                let row = frm.add_child("base_vehicle_cost_per_trip");
                row.unit_price = unit_price;
                row.description = description;
            });
            frm.refresh_field("base_vehicle_cost_per_trip");
            
            
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

            const tables = ["base_vehicle", "base_manpower"];
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

            const tables = ["base_vehicle", "base_manpower"];
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
		    frm.refresh_field('base_manpower')
        }
		
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
            frm.refresh_field('base_manpower')
        }
		
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
            frm.refresh_field('base_manpower')

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
            frm.refresh_field('base_manpower')

        }
		
	},
	
})

frappe.ui.form.on('Permanent Vehicle', {
	
	total_provided(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.total_provided>0 && row.unit_price > 0){
            row.total_claim_this_month = row.total_provided*row.unit_price
            row.amount_to_be_paid=row.total_claim_this_month
		    frm.refresh_field('base_vehicle')
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
            frm.refresh_field('base_vehicle')
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
            frm.refresh_field('base_vehicle')

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
            frm.refresh_field('base_vehicle')

        }
		
	},
    
	
})

frappe.ui.form.on('Base Vehicle Cost Per Trip', {
	no_of_trip(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.no_of_trip>0){
           row.total_claim_this_month=row.unit_price*row.no_of_trip
            row.amount_to_be_paid= row.total_claim_this_month-row.total_deduction

        }else{
            row.amount_to_be_paid= 0

        }
        frm.refresh_field('base_vehicle_cost_per_trip')
	},
		
    total_deduction(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.total_deduction>0){
           
            row.amount_to_be_paid= row.total_claim_this_month-row.total_deduction

        }else{
            row.amount_to_be_paid= row.total_claim_this_month

        }
        frm.refresh_field('base_vehicle_cost_per_trip')
	},
    total_claim_this_month(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.total_deduction>0){
           
            row.total_deduction= tot
            row.amount_to_be_paid= row.total_claim_this_month-row.total_deduction
            frm.refresh_field('base_manpower')

        }else{
            row.amount_to_be_paid= row.total_claim_this_month

        }
        frm.refresh_field('base_vehicle_cost_per_trip')

	},
	
})

frappe.ui.form.on('AIRCONDITIONING SYSTEM SPARE PARTS', {
	unit_qty(frm,cdt,cdn){
        var row = locals[cdt][cdn];
        if (row.unit_qty > 0){
            row.total_claim_this_month=row.unit_price*row.unit_qty
            if (row.deduction > 0){
                row.amount_to_be_paid=row.total_claim_this_month-row.deduction
            }else{
                row.amount_to_be_paid=row.total_claim_this_month
            }
        }else{
            row.total_claim_this_month=0
            row.amount_to_be_paid=0
        }
        frm.refresh_field('airconditioning_system_spare_parts')
    },
	unit_price(frm,cdt,cdn){
        var row = locals[cdt][cdn];
        if (row.unit_qty > 0 && row.unit_price > 0){
            row.total_claim_this_month=row.unit_price*row.unit_qty
        }else{
            row.total_claim_this_month=0
        }
        frm.refresh_field('airconditioning_system_spare_parts')
    },
    total_deduction(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.total_deduction>0){
           
            row.total_deduction= tot
            row.amount_to_be_paid= row.total_claim_this_month-row.total_deduction
            frm.refresh_field('airconditioning_system_spare_parts')

        }else{
            row.amount_to_be_paid= row.total_claim_this_month

        }
		
	},
    total_claim_this_month(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.total_deduction>0){
           
            row.total_deduction= tot
            row.amount_to_be_paid= row.total_claim_this_month-row.total_deduction
            frm.refresh_field('airconditioning_system_spare_parts')

        }else{
            row.amount_to_be_paid= row.total_claim_this_month

        }
		
	},
	
})

frappe.ui.form.on('FF Systems Spare Parts', {
	unit_qty(frm,cdt,cdn){
        var row = locals[cdt][cdn];
        if (row.unit_qty > 0){
            row.total_claim_this_month=row.unit_price*row.unit_qty
        }else{
            row.total_claim_this_month=0
        }
        frm.refresh_field('ff_systems_spare_parts')

    },
	unit_price(frm,cdt,cdn){
        var row = locals[cdt][cdn];
        if (row.unit_qty > 0 && row.unit_price > 0){
            row.total_claim_this_month=row.unit_price*row.unit_qty
        }else{
            row.total_claim_this_month=0
        }
        frm.refresh_field('ff_systems_spare_parts')

    },
    total_deduction(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.total_deduction>0){
           
            row.total_deduction= tot
            row.amount_to_be_paid= row.total_claim_this_month-row.total_deduction
            frm.refresh_field('ff_systems_spare_parts')

        }else{
            row.amount_to_be_paid= row.total_claim_this_month
            frm.refresh_field('ff_systems_spare_parts')
        }
		
	},
    total_claim_this_month(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.total_deduction>0){
           
            row.total_deduction= tot
            row.amount_to_be_paid= row.total_claim_this_month-row.total_deduction
            frm.refresh_field('ff_systems_spare_parts')

        }else{
            row.amount_to_be_paid= row.total_claim_this_month
            frm.refresh_field('ff_systems_spare_parts')
        }
		
	},
	
})


frappe.ui.form.on('Overtime Details', {
	
	qty(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.qty>0 && row.ot_hourly_rate > 0){
            row.total = row.qty*row.ot_hourly_rate
            row.amount_to_be_paid=row.total
		    frm.refresh_field('overtime_details')
        }else{
            row.total = 0
            row.amount_to_be_paid=0
        }
		
	},
    ot_hourly_rate(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.qty>0 && row.ot_hourly_rate > 0){
            row.total = row.qty*row.ot_hourly_rate
            row.amount_to_be_paid=row.total
		    frm.refresh_field('overtime_details')
        }else{
            row.total = 0
            row.amount_to_be_paid=0
        }
		
	},
    
    
})
