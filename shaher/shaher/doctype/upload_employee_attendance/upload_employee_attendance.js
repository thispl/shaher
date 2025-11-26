// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Upload Employee Attendance", {
    setup(frm){
        frm.set_query("department", function() {
            return {
                "filters": {
                    "company": frm.doc.company
                }
            };
        });
    },
    onload: function(frm) {
        frm.set_df_property('html', 'options',
            `<strong>Attendance Status:</strong>
            <ul style="list-style-type: none; padding-left: 0; margin-top: 5px;">
                <li><strong style="color: green;">P</strong> – Present</li>
                <li><strong style="color: red;">A</strong> – Absent</li>
                <li><strong style="color: orange;">RD</strong> – Rest Day</li>
                <li><strong style="color: blue;">HD</strong> – Half Day</li>
            </ul>`
        );
    },
    to_date: function(frm) {
        if (frm.doc.from_date && frm.doc.to_date) {
            if (frm.doc.from_date > frm.doc.to_date) {
                frm.set_value('to_date', null); 
                frappe.msgprint(__('To Date cannot be less than From Date'));
            }
        }
    },
    from_date: function(frm) {
        if (frm.doc.from_date && frm.doc.to_date) {
            if (frm.doc.from_date > frm.doc.to_date) {
                frm.set_value('from_date', null);
                frappe.msgprint(__('From Date cannot be greater than To Date'));
            }
        }
    },
	download: function (frm) {
        window.location.href = repl(frappe.request.url +
                 '?cmd=%(cmd)s&from_date=%(from_date)s&to_date=%(to_date)s&department=%(department)s&designation=%(designation)s&company=%(company)s&site_location=%(site_location)s&name=%(name)s',{
                 cmd: "shaher.shaher.doctype.upload_employee_attendance.upload_employee_attendance.get_template",
                 from_date: frm.doc.from_date,
                 to_date: frm.doc.to_date,
                 department:frm.doc.department,
                 designation:frm.doc.designation,
                 company:frm.doc.company,
                 site_location: frm.doc.site_location,
                 name:frm.doc.name
             })
         },
    download_template: function (frm) {
        window.location.href = repl(frappe.request.url +
                 '?cmd=%(cmd)s&from_date=%(from_date)s&to_date=%(to_date)s&department=%(department)s&designation=%(designation)s&company=%(company)s&site_location=%(site_location)s&name=%(name)s',{
                 cmd: "shaher.shaher.doctype.upload_employee_attendance.pdo_upload_format.get_template",
                 from_date: frm.doc.from_date,
                 to_date: frm.doc.to_date,
                 department:frm.doc.department,
                 designation:frm.doc.designation,
                 company:frm.doc.company,
                 site_location: frm.doc.site_location,
                 name:frm.doc.name
             })
         },
    
});
