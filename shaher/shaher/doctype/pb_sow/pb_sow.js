// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("PB SOW", {
    onload(frm){
        frappe.breadcrumbs.add("Project", "PB SOW");
        frappe.ready(() => {
            // Always push state when the page loads
            history.pushState(null, '', window.location.href);
        
            // Trap the back button indefinitely
            window.addEventListener('popstate', function (event) {
                history.pushState(null, '', window.location.href);
            });
        });
        
        
    },
    refresh: function(frm) {
        if (!frm.doc.__islocal) {
            history.pushState(null, null, location.href);
            frm.add_custom_button(__('Back'), function () {
                if (frm.doc.bidding_amount_difference == 0) {
                    frappe.set_route("Form", "Project Budget", frm.doc.project_budget);
                }
                else {
                    
                    frappe.msgprint(__("Please check the Bidding Amount Difference"));
                }
            });
        }
    },

    // Amount to Percent
    business_promotion_amount(frm) {
        amount = (frm.doc.business_promotion_amount / frm.doc.lpo_amount) * 100
        frm.set_value('business_promotion_percent', amount)
    },
    overhead_amount(frm) {
        amount = (frm.doc.overhead_amount / frm.doc.lpo_amount) * 100
        frm.set_value('overhead_percent', amount)
    },
    contigency_amount(frm) {
        amount = (frm.doc.contigency_amount / frm.doc.lpo_amount) * 100
        frm.set_value('contigency_percent', amount)
    },
    gross_profit_amount(frm) {
        amount = (frm.doc.gross_profit_amount / frm.doc.lpo_amount) * 100
        frm.set_value('gross_profit_percent', amount)
    },

    // Percent to Amount
    business_promotion_percent(frm) {
        amount = (frm.doc.business_promotion_percent / 100) * frm.doc.lpo_amount
        frm.set_value('business_promotion_amount', amount)
    },
    overhead_percent(frm) {
        amount = (frm.doc.overhead_percent / 100) * frm.doc.lpo_amount
        frm.set_value('overhead_amount', amount)
    },
    contigency_percent(frm) {
        amount = (frm.doc.contigency_percent / 100) * frm.doc.lpo_amount
        frm.set_value('contigency_amount', amount)
    },
    gross_profit_percent(frm) {
        amount = (frm.doc.gross_profit_percent / 100) * frm.doc.lpo_amount
        frm.set_value('gross_profit_amount', amount)
    },
    
});

// Setting default value for SOW from SO for PB Items table
frappe.ui.form.on("PB Items", {
    form_render: function(frm, cdt, cdn) {
        let child = locals[cdt][cdn];
        if (!child.sow) {
            frappe.model.set_value(cdt, cdn, "sow", frm.doc.sow);
        }
    }
});

// Setting default value for SOW from SO for PB FG Items table
frappe.ui.form.on("PB FG Items", {
    form_render: function(frm, cdt, cdn) {
        let child = locals[cdt][cdn];
        if (!child.sow) {
            frappe.model.set_value(cdt, cdn, "sow", frm.doc.sow);
        }
    }
});

// Setting auto calculation for amount and cost in PB FG Items table
frappe.ui.form.on("PB FG Items", {
    qty: function(frm, cdt, cdn) {
        update_amount(cdt, cdn);
    },
    cost: function(frm, cdt, cdn) {
        update_amount(cdt, cdn);
    },
    amount: function(frm, cdt, cdn) {
        update_cost(cdt, cdn);
    },
});

// Setting auto calculation for amount and cost in PB Items table
frappe.ui.form.on("PB Items", {
    qty: function(frm, cdt, cdn) {
        update_amount(cdt, cdn);
    },
    cost: function(frm, cdt, cdn) {
        update_amount(cdt, cdn);
    },
    amount: function(frm, cdt, cdn) {
        update_cost(cdt, cdn);
    },
});

function update_amount(cdt, cdn) {
    let row = locals[cdt][cdn];
    let qty = flt(row.qty);
    let cost = flt(row.cost);

    if (!isNaN(qty) && !isNaN(cost)) {
        frappe.model.set_value(cdt, cdn, "amount", qty * cost);
    }
}

function update_cost(cdt, cdn) {
    let row = locals[cdt][cdn];
    let qty = flt(row.qty);
    let amount = flt(row.amount);

    if (!isNaN(qty) && !isNaN(amount)) {
        frappe.model.set_value(cdt, cdn, "cost", amount / qty);
    }
}


