// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("HSE Report Dashboard", {
	download(frm) {
        if (frm.doc.report){
            if (frm.doc.report=="HSE Training Matrix"){
                var path = 'shaher.shaher.doctype.hse_report_dashboard.hse_register.download'
                var args = "from_date=" + encodeURIComponent(frm.doc.from_date || '') +
                        "&to_date=" + encodeURIComponent(frm.doc.to_date || '')+
                        "&division=" + encodeURIComponent(frm.doc.division || '')+
                        "&company=" + encodeURIComponent(frm.doc.company || '');
                if (path) {
                    window.location.href = repl(frappe.request.url +
                        '?cmd=%(cmd)s&%(args)s', {
                        cmd: path,
                        args:args
                    });
                }
            }
            else if (frm.doc.report=="FTW Register"){
                var path = 'shaher.shaher.doctype.hse_report_dashboard.ftw_register.download_hse_excel'
                var args = "from_date=" + encodeURIComponent(frm.doc.from_date || '') +
                        "&to_date=" + encodeURIComponent(frm.doc.to_date || '')+
                        "&division=" + encodeURIComponent(frm.doc.division || '')+
                        "&company=" + encodeURIComponent(frm.doc.company || '');
                if (path) {
                    window.location.href = repl(frappe.request.url +
                        '?cmd=%(cmd)s&%(args)s', {
                        cmd: path,
                        args:args
                    });
                }
            }
			else if (frm.doc.report=="HSE Vehicle Register"){
                var path = 'shaher.shaher.doctype.hse_report_dashboard.vehicle_register.download_vehicle_register'
                var args = "&company=" + encodeURIComponent(frm.doc.company || '');
                if (path) {
                    window.location.href = repl(frappe.request.url +
                        '?cmd=%(cmd)s&%(args)s', {
                        cmd: path,
                        args:args
                    });
                }
            }
        }
        
	},
});
