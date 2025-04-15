frappe.ui.form.on("Salary Certificate", {
    before_workflow_action: function (frm) {
        var workflow_list = ["Pending for HR Department", "Pending for HOD", "Pending for HR Manager"];

        if (workflow_list.includes(frm.doc.workflow_state) && frm.selected_workflow_action === "Reject") {
            if (!frm.doc.rejection_remark) {
                let d = new frappe.ui.Dialog({
                    title: __("Rejection Remarks"),
                    fields: [
                        {
                            label: __("Remark"),
                            fieldname: "remark",
                            fieldtype: "Small Text",
                            reqd: 1,
                        },
                    ],
                    primary_action_label: __("Submit"),
                    primary_action: function () {
                        let data = d.get_values();
                        if (data && data.remark) {
                            frm.set_value("rejection_remark", data.remark).then(function () {
                                frm.set_value("workflow_state", "Rejected").then(function () {
                                    frm.save();
                                    d.hide();
                                });
                            });
                        } else {
                            frappe.msgprint(__("Please enter a remark before submitting."));
                        }
                    }
                });

                d.show();
                frappe.validated = false;
                frappe.msgprint(__("Please enter a remark before submitting."));

            }
        }
    }
});
