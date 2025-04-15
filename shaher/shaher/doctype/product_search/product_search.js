// Copyright (c) 2022, Abdulla and contributors
// For license information, please see license.txt

frappe.ui.form.on('Product Search', {
	item_code(frm){
		if(frm.doc.item_code){
		frm.call('get_data').then(r=>{
			if (r.message) {
				if(frappe.user.has_role != "Purchase User"){
				frm.fields_dict.html.$wrapper.empty().append(r.message)
				}
				frm.call('get_pod').then(r=>{
					frm.fields_dict.pod.$wrapper.empty().append(r.message)
				})
			}
		})	
		frm.call('get_data_perm').then(j=>{
			if (j.message) {
				frm.fields_dict.perm.$wrapper.empty().append(j.message)
			}
			
		})
		frappe.call({
			method:"electra.utils.get_norden_item",
			args:{
				item:frm.doc.item_code,
			},
			callback(r){
				$.each(r.message,function(i,d){
					frm.fields_dict.html_3.$wrapper.empty().append(d)
				})
			}
		})
		frappe.call({
			method:"electra.utils.get_norden_item_without_cost",
			args:{
				item:frm.doc.item_code,
			},
			callback(r){
				$.each(r.message,function(i,d){
					frm.fields_dict.html_4.$wrapper.empty().append(d)
				})
			}
		})
		
	}	
	}
})