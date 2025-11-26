// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Attendance and OT Register", {
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
