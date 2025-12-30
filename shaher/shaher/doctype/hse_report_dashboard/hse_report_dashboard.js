// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("HSE Report Dashboard", {
	download(frm) {
        if (frm.doc.report){
            if (frm.doc.report=="HSE Register"){
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
        }
        
	},
});
