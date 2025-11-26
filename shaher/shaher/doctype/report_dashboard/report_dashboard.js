// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Report Dashboard", {
    download(frm) {
        if (frm.doc.report == 'Currency Exchange Gain / Loss') {
            console.log("outside")
            var path = 'shaher.shaher.doctype.report_dashboard.profit_loss_report.download'
            if (path) {
                window.location.href = repl(frappe.request.url +
                    '?cmd=%(cmd)s&%(args)s', {
                    cmd: path,
                });
            }
        }
        else if (frm.doc.report == 'VAT Summary') {
            var path = 'shaher.shaher.doctype.report_dashboard.vat_summary.download'
            var args = "from_date=" + encodeURIComponent(frm.doc.from_date || '') +
					"&to_date=" + encodeURIComponent(frm.doc.to_date || '')+
                    "&company=" + encodeURIComponent(frm.doc.company || ''); 
            if (path) {
                window.location.href = repl(frappe.request.url +
                    '?cmd=%(cmd)s&%(args)s', {
                    cmd: path,
                    args:args
                });
            }
            
        }
        else if (frm.doc.report == 'Salary Register Report') {
            var path = 'shaher.shaher.doctype.report_dashboard.salary_register_report.download'
            var args = "from_date=" + encodeURIComponent(frm.doc.from_date || '') +
					"&to_date=" + encodeURIComponent(frm.doc.to_date || '')+
                    "&company=" + encodeURIComponent(frm.doc.company || ''); 
            if (path) {
                window.location.href = repl(frappe.request.url +
                    '?cmd=%(cmd)s&%(args)s', {
                    cmd: path,
                    args:args
                });
            }
            
        }
        else if (frm.doc.report == 'Timesheet Report') {
            var path = 'shaher.shaher.doctype.report_dashboard.timesheet_report.download'
            var args = "from_date=" + encodeURIComponent(frm.doc.from_date || '') +
					"&to_date=" + encodeURIComponent(frm.doc.to_date || '')+
                    "&company=" + encodeURIComponent(frm.doc.company || '')+
                    "&site_location=" + encodeURIComponent(frm.doc.site_location || ''); 
            if (path) {
                window.location.href = repl(frappe.request.url +
                    '?cmd=%(cmd)s&%(args)s', {
                    cmd: path,
                    args:args
                });
            }
            
        }
        else if (frm.doc.report == 'Monthly Attendance Sheet') {
            var path = 'shaher.shaher.doctype.report_dashboard.monthly_attendance_sheet.download'
            var args = "from_date=" + encodeURIComponent(frm.doc.from_date || '') +
					"&to_date=" + encodeURIComponent(frm.doc.to_date || '')+
                    "&company=" + encodeURIComponent(frm.doc.company || ''); 
            if (path) {
                window.location.href = repl(frappe.request.url +
                    '?cmd=%(cmd)s&%(args)s', {
                    cmd: path,
                    args:args
                });
            }
            
        }
        else if(frm.doc.report == 'Standard Rated Sales'){
            var path = 'shaher.shaher.doctype.report_dashboard.standard_rated_sales.download'
            var args = "from_date=" + encodeURIComponent(frm.doc.from_date || '') +
					"&to_date=" + encodeURIComponent(frm.doc.to_date || '');
            console.log(args)
            if (path) {
                window.location.href = repl(frappe.request.url +
                    '?cmd=%(cmd)s&%(args)s', {
                    cmd: path,
                    args:args
                });
            }
        }
        else if(frm.doc.report == 'Zero Rated Sales'){
            var path = 'shaher.shaher.doctype.report_dashboard.zero_rated_sales.download'
            var args = "from_date=" + encodeURIComponent(frm.doc.from_date || '') +
					"&to_date=" + encodeURIComponent(frm.doc.to_date || '');
            if (path) {
                window.location.href = repl(frappe.request.url +
                    '?cmd=%(cmd)s&%(args)s', {
                    cmd: path,
                    args:args
                });
            }
        }
        else if(frm.doc.report == 'Input Tax'){
            var path = 'shaher.shaher.doctype.report_dashboard.input_tax.download'
            var args = "from_date=" + encodeURIComponent(frm.doc.from_date || '') +
					"&to_date=" + encodeURIComponent(frm.doc.to_date || '');
            if (path) {
                window.location.href = repl(frappe.request.url +
                    '?cmd=%(cmd)s&%(args)s', {
                    cmd: path,
                    args:args
                });
            }
        }
	},
});
