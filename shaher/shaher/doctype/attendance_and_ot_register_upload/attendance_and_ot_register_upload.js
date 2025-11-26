// // Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// // For license information, please see license.txt

frappe.ui.form.on("Attendance and OT Register Upload", {
    onload(frm){
         if (!frm.doc.attach) {
            frm.set_df_property("html_preview", "options", "");
            frm.refresh_field("html_preview");
        }
    },
	refresh(frm) {
        frm.fields_dict.emp.$wrapper.html(`
            <p style="font-size: 15px;margin-top: 40px;">             </p>
        `);
        frm.fields_dict.get_tem.$wrapper.html(`
            <p style="font-size: 15px; ">A) Get the Template</p>
        `);
         frm.fields_dict.att.$wrapper.html(`
            <p style="font-size: 15px;margin-top: 45px;">B) Attach the file to be uploaded</p>
        `);
        frm.fields_dict.up.$wrapper.html(`
            <p style="font-size: 15px; margin-top: 45px;">C) Upload the attached file</p>
        `)
        if(frm.doc.attach){
		 frappe.call({
            method: "shaher.shaher.doctype.attendance_and_ot_register_upload.attendance_and_ot_register_upload.excel_preview",  
            args: {
                file_url: frm.doc.attach
            },
            callback: function (r) {
                if (r.message) {
                    frm.fields_dict.html_preview.$wrapper.html(r.message); 
                } 
				
            }
        });
    }
   

	},
	get_templete(frm)
	{
		var path ="shaher.shaher.doctype.attendance_and_ot_register_upload.attendance_and_ot_register_upload.get_template"
        var args = "location=" + encodeURIComponent(frm.doc.location || '')+ "&company=" + encodeURIComponent(frm.doc.company || '')+"&from_date=" + encodeURIComponent(frm.doc.from_date || '')+ "&to_date=" + encodeURIComponent(frm.doc.to_date || '')

		if (path) {
		window.location.href = repl(frappe.request.url +
			'?cmd=%(cmd)s&%(args)s', {
			cmd: path,
            args:args
		});
	}

	},
  
	upload(frm){
         if (!frm.doc.from_date || !frm.doc.to_date) {
        frappe.msgprint("Please Enter the Date");
        return;
    }
        if (!frm.doc.attach) {
        frappe.msgprint("Please attach the file to be uploaded");
        return;
    }
    
		let d = new frappe.ui.Dialog({
    title: 'Enter details',
    fields: [
        {
            label: 'Create and Submit Attendance and OT Register',
            fieldname: 'create_and_submit',
            fieldtype: 'Check',
            onchange: function () {
                if (d.get_value('create_and_submit')) {
                    d.set_value('create_only', 0);  
                }
            }
        },
        {
            label: 'Create Attendance and OT Register',
            fieldname: 'create_only',
            fieldtype: 'Check',
            onchange: function () {
                if (d.get_value('create_only')) {
                    d.set_value('create_and_submit', 0); 
                }
            }
        }
    ],
    size: 'small',
    primary_action_label: 'Upload',
    primary_action(values) {
        if (values.create_and_submit) {
            
             frappe.call({
                    method: "shaher.shaher.doctype.attendance_and_ot_register_upload.attendance_and_ot_register_upload.create_doc",
                    args: {
                        file_url: frm.doc.attach,
                        from_date: frm.doc.from_date,
                        to_date:frm.doc.to_date,
                        doc_name:frm.doc.name,
                        submit: true
                    },
                    freeze: true,
                    callback: function (r) {
                        if (r.message) {
                            frappe.msgprint("Documents Created and Submitted: " + r.message.length);
                        }
                        d.hide();
                    }
                });
        } else if (values.create_only) {
           
            frappe.call({
                    method: "shaher.shaher.doctype.attendance_and_ot_register_upload.attendance_and_ot_register_upload.create",
                    args: {
                        file_url: frm.doc.attach,
                        from_date: frm.doc.from_date,
                        to_date:frm.doc.to_date,
                        doc_name : frm.doc.name,
                        submit: true
                    },
                    freeze: true,
                    callback: function (r) {
                        if (r.message) {
                            frappe.msgprint("Documents Created " + r.message.length);
                        }
                        d.hide();
                    }
                });
        } else {
            frappe.msgprint("Please select one option.");
        }
    },

});

d.show();




	},
    from_date: function (frm) {
		frm.events.validate_from_to_date(frm, "from_date");
	},

	to_date: function (frm) {
		frm.events.validate_from_to_date(frm, "to_date");
	},
    validate_from_to_date: function (frm, updated_field) {
		if (!frm.doc.from_date || !frm.doc.to_date) return;

		const from_date = Date.parse(frm.doc.from_date);
		const to_date = Date.parse(frm.doc.to_date);

		if (to_date < from_date) {
			const other_field = updated_field === "from_date" ? "to_date" : "from_date";

			frm.set_value(other_field, frm.doc[updated_field]);
			frappe.show_alert({
				message: __("Changing '{0}' to {1}.", [
					__(frm.fields_dict[other_field].df.label),
					frappe.datetime.str_to_user(frm.doc[updated_field]),
				]),
				indicator: "blue",
			});
		}
	},

});


