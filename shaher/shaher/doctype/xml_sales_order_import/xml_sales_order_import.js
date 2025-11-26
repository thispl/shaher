// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt


frappe.ui.form.on("XML Sales Order Import", {
    onload(frm) {
        frappe.breadcrumbs.add('XML Sales Order Import', 'XML Sales Order Import');
    },
	refresh(frm) {
        frm.fields_dict.html_1.$wrapper.html(`
            <p style="font-size: 15px;">A) Attach the .xml file to be uploaded</p>
        `);
        frm.fields_dict.html_2.$wrapper.html(`
            <p style="font-size: 15px; margin-top: 45px;">B) Upload the attached file</p>
        `);
        frm.fields_dict.html_3.$wrapper.html(`
            <p style="font-size: 15px; margin-top: 45px;"></p>
        `);
        
	},
    validate(frm){
        if (frm.doc.attach) {
            let extension = frm.doc.attach.split('.').pop().toLowerCase();
            if (extension !== 'xml') {
                frm.set_value('attach','')
                frappe.throw(__('Only XML files are allowed!'));
            }
        }
    },
    upload(frm){
        if(frm.doc.attach){
            frappe.call({
                'method':'shaher.shaher.xml_file_upload.parse_uploaded_xml',
                'args':{
                    'file_name':frm.doc.attach
                },
                callback(r){
                    if(r.message){
                        
                        frappe.set_route('Form', 'Sales Order', r.message)
                        frm.set_value('attach','')
                        frm.save()
                    }
                }
            })
        }
    }
});
