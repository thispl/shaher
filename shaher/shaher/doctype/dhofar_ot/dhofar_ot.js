// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("DHOFAR OT", {
   
	refresh(frm) {
        frm.fields_dict["overtime_details"].grid.cannot_add_rows = true;
        frm.fields_dict["overtime_details"].grid.wrapper.find('.grid-remove-rows').hide();
        frm.fields_dict["overtime_details"].grid.only_sortable = false;
        frm.fields_dict["overtime_details"].refresh();
    
        if (frm.doc.__islocal) {
            const currentYear = new Date().getFullYear();
            frm.set_value('year', currentYear);
            const rawData = [
                ["Overtime Project Manager - Omani", 3112.900, 2100.000, 1012.900],
                ["Overtime Project Manager - Foreign", 2850.000, 1900.000, 950.000],
                ["Overtime Protection Engineer - Foreign", 2859.819, 1900.000, 959.819],
                ["Overtime Sr. Technical Engineer - Foreign", 1419.156, 950.000, 469.156],
                ["Overtime Asst. Electrical Engineer - Omani", 974.515, 650.000, 324.515],
                ["Overtime Asst. Electrical Engineer - Foreign", 698.825, 466.000, 232.825],
                ["Overtime Business Analyst - Foreign", 1739.304, 1160.000, 579.304],
                ["Overtime Technical Coordinator - Omani", 982.550, 656.000, 326.550],
                ["Overtime HSE Supervisor - Omani", 1073.522, 716.000, 357.522],
                ["Overtime Protection Technicians - Foreign", 408.342, 273.000, 135.342],
                ["Overtime Electrical Technicians - Omani", 652.718, 436.000, 216.718],
                ["Overtime Electrical Technicians - Foreign", 255.740, 170.000, 85.740],
                ["Overtime Over Head Lineman - Omani", 597.468, 399.000, 198.468],
                ["Overtime Over Head Lineman - Foreign", 255.740, 170.000, 85.740],
                ["Overtime Fire Fighting Alarm Technician - Foreign", 253.095, 189.000, 64.095],
                ["Overtime FF Mechanical Technician - Omani", 652.468, 435.000, 217.468],
                ["Overtime FF Mechanical Technician - Foreign", 253.096, 169.000, 84.096],
                ["Overtime AC Technicians - Omani", 669.556, 447.000, 222.556],
                ["Overtime AC Technicians - Foreign", 253.095, 169.000, 84.095],
                ["Overtime Drivers - Omani", 636.476, 425.000, 211.476],
                ["Overtime Helpers - Omani", 824.929, 550.000, 274.929],
                ["Overtime Helpers & Cleaner - Foreign", 214.308, 143.000, 71.308]
            ]


            const hourlyRates = [
                10.500, 13.125, 17.500, 
                9.896, 11.875, 15.833, 
                9.896, 11.875, 15.833, 
                4.948, 5.938, 7.917, 
                3.385, 4.063, 5.417, 
                2.427, 2.913, 3.883, 
                6.042, 7.250, 9.667, 
                3.417, 4.100, 5.467, 
                3.729, 4.475, 5.967, 
                1.422, 1.706, 2.275, 
                2.271, 2.725, 3.633, 
                0.885, 1.063, 1.417, 
                2.078, 2.494, 3.325, 
                0.885, 1.063, 1.417, 
                0.984, 1.181, 1.575, 
                2.266, 2.719, 3.625, 
                0.880, 1.056, 1.408, 
                2.328, 2.794, 3.725, 
                0.880, 1.056, 1.408, 
                2.214, 2.656, 3.542, 
                2.865, 3.438, 4.583, 
                0.745, 0.894, 1.192
            ];


            const units = ["Per Hour on Day Time", "Per Hour on Night Time", "Per Hour on Weekend & Holidays"];

            frm.clear_table("overtime_details");

            let rateIndex = 0;

            rawData.forEach(([description, monthly_unit_rate, basic_salary, allowances]) => {
                for (let i = 0; i < 3; i++) {
                    let row = frm.add_child("overtime_details");
                    row.description = description;
                    row.monthly_unit_rate = monthly_unit_rate;
                    row.basic_salary = basic_salary;
                    row.allowances = allowances;

                    row.unit = units[i]; // "Day", "Night", "Weekend"
                    row.ot_hourly_rate = hourlyRates[rateIndex]; // Matching hourly rate

                    rateIndex++;
                }
            });

            frm.refresh_field("overtime_details");
        }

	},
    month(frm) {
        set_invoice_dates_and_update_rows(frm);
    },
    year(frm) {
        set_invoice_dates_and_update_rows(frm);
    },
    invoice_from(frm) {
        if (frm.doc.invoice_from && frm.doc.invoice_upto) {
            if (frm.doc.invoice_from > frm.doc.invoice_upto) {
                frm.set_value('invoice_from', '');
                frappe.throw('Invoice From date cannot be greater than Invoice Upto Date');
            }
        }
    },
    

    invoice_upto(frm){
        if (frm.doc.invoice_from && frm.doc.invoice_upto){
            if (frm.doc.invoice_from > frm.doc.invoice_upto){
                frm.set_value('invoice_upto','')
                frappe.throw('Invoice Upto Date must be greater than Invoice from date')
            }
        }
    },

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

frappe.ui.form.on('Overtime Details', {
	
	qty(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if (row.ot_hourly_rate > 0){
            row.total = row.qty*row.ot_hourly_rate
            row.amount_to_be_paid=row.total
		    frm.refresh_field('overtime_details')
        }else{
            row.total = 0
            row.amount_to_be_paid=0
        }
		
	},
    
    
})