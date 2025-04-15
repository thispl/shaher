frappe.listview_settings['Legal Compliance Monitor'] = {
    add_fields: ["status"],
    get_indicator: function (doc) {
        
        if (doc.status === "Active") {
            return [__("Active"), "green", "status,=,Active"];
        } else if (doc.status === "Expiring") {
            return [__("Expiring"), "orange","status,=,Expiring"];
        } else if (doc.status === "Expired") {
            return [__("Expired"), "red", "status,=,Expired"];
        }
    }
};

