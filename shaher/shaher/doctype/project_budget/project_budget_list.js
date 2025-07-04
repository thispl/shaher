frappe.listview_settings['Project Budget'] = {
    onload(listview) {
        frappe.breadcrumbs.add("Project", "Project Budgets");
    }
};