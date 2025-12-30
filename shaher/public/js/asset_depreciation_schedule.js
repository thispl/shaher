frappe.ui.form.on("Asset Depreciation Schedule", {
    onload(frm) {
        if (frm.doc.custom_depreciation_method == "Written Down Value") {
            const grid = frm.get_field('depreciation_schedule').grid;
            grid.update_docfield_property('accumulated_depreciation_amount', 'hidden', 1);
            grid.reset_grid();
        }
    },
    setup(frm) {
        if (frm.doc.custom_depreciation_method == "Written Down Value") {
            const grid = frm.get_field('depreciation_schedule').grid;
            grid.update_docfield_property('accumulated_depreciation_amount', 'hidden', 1);
            grid.reset_grid();
        }
    },
    refresh(frm) {
        if (frm.doc.custom_depreciation_method == "Written Down Value") {
            const grid = frm.get_field('depreciation_schedule').grid;
            grid.update_docfield_property('accumulated_depreciation_amount', 'hidden', 1);
            grid.reset_grid();
        }
    },
});