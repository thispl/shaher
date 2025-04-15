// Copyright (c) 2024, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('HR Policy', {
	refresh: function(frm) {
        console.log("HI")
        if (frm.doc.hr_policy) {
            console.log("HI")
            var html_view = '<iframe src="' + frm.doc.hr_policy + '" width="800" height="600"></iframe>';
            $(frm.fields_dict['view'].wrapper).html(html_view);
        }
    },
    hr_policy: function(frm) {
        console.log("HI")
        if (frm.doc.hr_policy) {
            console.log("HI")
            var html_view = '<iframe src="' + frm.doc.hr_policy + '" width="800" height="600"></iframe>';
            $(frm.fields_dict['view'].wrapper).html(html_view);
        }
    },
    onload: function(frm) {
        console.log("HI")
        if (frm.doc.hr_policy) {
            console.log("HI")
            var html_view = '<iframe src="' + frm.doc.hr_policy + '" width="800" height="600"></iframe>';
            $(frm.fields_dict['view'].wrapper).html(html_view);
        }
    },
});
