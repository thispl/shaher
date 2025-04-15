// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Provisional Budgeting", {
	refresh(frm){
        if(frm.doc.docstatus==1){
            frm.add_custom_button(__("Create Comparison"), function () {
                frappe.db.get_value('Provisional Budgeting Comparison', { 'provisional_budgeting': frm.doc.name }, 'name')
					.then(r => {
						if (r.message && Object.entries(r.message).length === 0) {
							frappe.model.open_mapped_doc({
								method: "shaher.custom.make_quotation",
								frm: cur_frm
							})
						}
						else {
							frappe.set_route('Form', 'Provisional Budgeting Comparison', r.message.name)
							
						}


					})
                
            })
        }
        if (frm.doc.company && frm.doc.__islocal) {
            fetchAccounts(frm, 'Income', 'income');
            fetchAccounts(frm, 'Expense', 'expenses');
        }
        if (frm.doc.company){
            frm.fields_dict['income'].grid.get_field('account').get_query = function(doc, cdt, cdn) {
            return {
                filters: {
                    disabled: 0,
                    company: frm.doc.company,
                    root_type:'Income'
                }
                };
            };
            frm.fields_dict['expenses'].grid.get_field('account').get_query = function(doc, cdt, cdn) {
            return {
                filters: {
                    disabled: 0,
                    company: frm.doc.company,
                    root_type:'Expense'
                }
                };
            };
        }
    }
});
frappe.ui.form.on('Provisional Budgeting Child', {
	account(frm,cdt,cdn) {
		var child = locals [cdt][cdn]
        if(child.account&&frm.doc.posting_date){
            frappe.call({
                'method':'shaher.shaher.doctype.provisional_budgeting.provisional_budgeting.get_current_value',
                'args':{
                    'account':child.account,
                    'date':frm.doc.posting_date
                },
                callback(r){
                    if(r){
                        child.current_value=r.message
                    }
                    frm.refresh_field('income')
                }
            })
        }
	}
})
frappe.ui.form.on('Provisional Budgeting Child Expense', {
	account(frm,cdt,cdn) {
		var child = locals [cdt][cdn]
        if(child.account&&frm.doc.posting_date){
            frappe.call({
                'method':'shaher.shaher.doctype.provisional_budgeting.provisional_budgeting.get_current_value',
                'args':{
                    'account':child.account,
                    'date':frm.doc.posting_date
                },
                callback(r){
                    if(r){
                        child.current_value=r.message
                    }

                    frm.refresh_field('expenses')
                }
            })
        }
	}
})



function fetchAccounts(frm, root_type, table_field) {
    frappe.call({
        method: 'frappe.client.get_list',
        args: {
            doctype: 'Account',
            filters: {
                root_type: root_type,
                is_group: 1, 
                company: frm.doc.company
            },
            fields: ['name', 'account_name', 'is_group']
        },
        callback: function(response) {
            if (response.message) {
                response.message.forEach(account => {
                    checkAndFetchChildAccounts(frm, account, table_field);
                });
            }
        }
    });
}

function checkAndFetchChildAccounts(frm, account, table_field) {
    frappe.call({
        method: 'frappe.client.get_list',
        args: {
            doctype: 'Account',
            filters: {
                parent_account: account.name
            },
            fields: ['name', 'account_name', 'is_group']
        },
        callback: function(response) {
            if (response.message.length > 0) {
                response.message.forEach(child => {
                    if (child.is_group) {
                        checkAndFetchChildAccounts(frm, child, table_field);
                    } else {
                        addAccountToTable(frm, child, table_field);
                    }
                });
            } else {
                
                addAccountToTable(frm, account, table_field);
            }
        }
    });
}

function addAccountToTable(frm, account, table_field) {
    if (!isAccountAlreadyAdded(frm, account.name, table_field)) {
        let row = frm.add_child(table_field);  
        row.account = account.name;
        if (account.name && frm.doc.posting_date) {
            frappe.call({
                method: 'shaher.shaher.doctype.provisional_budgeting.provisional_budgeting.get_current_value',
                args: {
                    account: account.name,
                    date: frm.doc.posting_date
                },
                callback(r) {
                    if (r) {
                        row.current_value = r.message;
                    }
                    frm.refresh_field(table_field);
                }
            });
        }
        frm.refresh_field(table_field);
    }
}

function isAccountAlreadyAdded(frm, account_name, table_field) {
    return frm.doc[table_field].some(row => row.account === account_name);
}
