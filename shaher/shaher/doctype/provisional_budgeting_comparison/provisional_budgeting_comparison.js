// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Provisional Budgeting Comparison", {
	refresh(frm) {
        if(frm.doc.posting_date && frm.doc.__islocal){
            $.each(frm.doc.income, function (i, d) {
                if (d.account && frm.doc.posting_date) {
                    frappe.call({
                        method: 'shaher.shaher.doctype.provisional_budgeting.provisional_budgeting.get_current_value',
                        args: {
                            account: d.account,
                            date: frm.doc.posting_date
                        },
                        callback(r) {
                            if (r) {
                                d.actual_value = r.message;
                                d.provisional_vs_actual = d.actual_value - d.provisional_value
                            }
                            frm.refresh_field('income');
                        }
                    });
                }
            })
            $.each(frm.doc.expenses, function (i, d) {
                if (d.account && frm.doc.posting_date) {
                    frappe.call({
                        method: 'shaher.shaher.doctype.provisional_budgeting.provisional_budgeting.get_current_value',
                        args: {
                            account: d.account,
                            date: frm.doc.posting_date
                        },
                        callback(r) {
                            if (r) {
                                d.actual_value = r.message;
                                d.provisional_vs_actual = d.actual_value - d.provisional_value
                            }
                            frm.refresh_field('expenses');
                        }
                    });
                }
            })
        }
	},
    // onload(frm){
    //     $.each(frm.doc.income, function (i, d) {
    //         if (d.name && frm.doc.posting_date) {
    //             frappe.call({
    //                 method: 'shaher.shaher.doctype.provisional_budgeting.provisional_budgeting.get_current_value',
    //                 args: {
    //                     account: d.name,
    //                     date: frm.doc.posting_date
    //                 },
    //                 callback(r) {
    //                     if (r) {
    //                         d.actual_value = r.message;
    //                         d.provisional_vs_actual = d.actual_value - d.provisional_value
    //                     }
    //                     frm.refresh_field('income');
    //                 }
    //             });
    //         }
    //     })
    //     $.each(frm.doc.expenses, function (i, d) {
    //         if (d.name && frm.doc.posting_date) {
    //             frappe.call({
    //                 method: 'shaher.shaher.doctype.provisional_budgeting.provisional_budgeting.get_current_value',
    //                 args: {
    //                     account: d.name,
    //                     date: frm.doc.posting_date
    //                 },
    //                 callback(r) {
    //                     if (r) {
    //                         d.actual_value = r.message;
    //                         d.provisional_vs_actual = d.actual_value - d.provisional_value
    //                     }
    //                     frm.refresh_field('expenses');
    //                 }
    //             });
    //         }
    //     })
    // }
});
frappe.ui.form.on("Provisional Budgeting Comparison Child", {
    actual_value(frm,cdt,cdn) {
		var child = locals [cdt][cdn]
        if(child.actual_value&&child.provisional_value){
            child.provisional_vs_actual=child.provisional_value - child.actual_value
            frm.refresh_field('income')
               
        }
	}
})
frappe.ui.form.on("Provisional Budgeting Comparison Child Expense", {
    actual_value(frm,cdt,cdn) {
		var child = locals [cdt][cdn]
        if(child.actual_value&&child.provisional_value){
            child.provisional_vs_actual=child.provisional_value - child.actual_value
            frm.refresh_field('expenses')
               
        }
	}
})