// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Approval Summary", {
    refresh(frm){
        frm.disable_save()
        $('*[data-fieldname="la_approval"]').find('.grid-remove-rows').hide();
        $('*[data-fieldname="la_approval"]').find('.grid-remove-all-rows').hide();
        $('*[data-fieldname="la_approval"]').find('.grid-add-row').remove()
        $('*[data-fieldname="delivery_note_approval"]').find('.grid-remove-rows').hide();
        $('*[data-fieldname="delivery_note_approval"]').find('.grid-remove-all-rows').hide();
        $('*[data-fieldname="delivery_note_approval"]').find('.grid-add-row').remove()
        $('*[data-fieldname="mr_approval"]').find('.grid-remove-rows').hide();
        $('*[data-fieldname="mr_approval"]').find('.grid-remove-all-rows').hide();
        $('*[data-fieldname="mr_approval"]').find('.grid-add-row').remove()
        $('*[data-fieldname="po_approval"]').find('.grid-remove-rows').hide();
        $('*[data-fieldname="po_approval"]').find('.grid-remove-all-rows').hide();
        $('*[data-fieldname="po_approval"]').find('.grid-add-row').remove()
        frm.call('get_user_workflow_states', {
            doctype: "Purchase Order",
        }).then(r => {
            const allowed_states = r.message || [];
            if (allowed_states.length) {
                frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Purchase Order",
                        filters: [
                            ["workflow_state", "in", allowed_states]
                        ],
                        fields: [
                            "name", "supplier", "custom_department",
                            "transaction_date", "workflow_state", "base_grand_total"
                        ],
                        limit_page_length: 500
                    },
                    callback(res) {
                        (res.message || []).forEach(po => {
                            frm.add_child("po_approval", {
                                purchase_order: po.name,
                                supplier: po.supplier,
                                department: po.custom_department,
                                date: po.transaction_date,
                                status: po.workflow_state,
                                grand_total: po.base_grand_total
                            });
                        });

                        frm.refresh_field("po_approval");
                    }
                });
            }
        });


        frm.call('get_user_workflow_states', {
            doctype: "Material Request",
        }).then(r => {
            const allowed_states = r.message || [];
            if (allowed_states.length) {
                frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Material Request",
                        filters: [
                            ["workflow_state", "in", allowed_states]
                        ],
                        fields: [
                            "name", "material_request_type", "custom_department",
                            "custom_site", "schedule_date", "project", "workflow_state"
                        ],
                        limit_page_length: 500
                    },
                    callback(res) {
                        (res.message || []).forEach(mr => {
                            frm.add_child("mr_approval", {
                                material_request: mr.name,
                                purpose: mr.material_request_type,
                                department: mr.custom_department,
                                site: mr.custom_site,
                                date: mr.schedule_date,
                                project: mr.project,
                                status: mr.workflow_state
                            });
                        });

                        frm.refresh_field("mr_approval");
                    }
                });
            }
        });


        frm.call('get_user_workflow_states', {
            doctype: "Leave Application",
        }).then(r => {
            const allowed_states = r.message || [];
            if (allowed_states.length) {
                frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Leave Application",
                        filters: [
                            ["workflow_state", "in", allowed_states]
                        ],
                        fields: [
                            "name", "employee", "employee_name", "workflow_state",
                            "posting_date as request_date", "department", "leave_type",
                            "leave_balance", "from_date", "to_date", "half_day",
                            "half_day_date", "total_leave_days", "description",
                            "custom_leave_approver_2 as leave_approver",
                            "custom_leave_approver_name_2 as leave_approver_name","custom_user_id"
                        ],
                        limit_page_length: 500
                    },
                    callback(res) {
                        (res.message || []).forEach(la => {
                            frm.add_child("la_approval", {
                                leave_application: la.name,
                                employee: la.employee,
                                employee_name: la.employee_name,
                                status: la.workflow_state,
                                request_date: la.request_date,
                                department: la.department,
                                leave_type: la.leave_type,
                                leave_balance_before_application: la.leave_balance,
                                from_date: la.from_date,
                                to_date: la.to_date,
                                half_day: la.half_day,
                                half_day_date: la.half_day_date,
                                total_leave_days: la.total_leave_days,
                                reason: la.description,
                                leave_approver: la.leave_approver,
                                leave_approver_name: la.leave_approver_name,
                                user_id:la.custom_user_id
                            });
                        });

                        frm.refresh_field("la_approval");
                    }
                });
            }
        });

        
        frm.call('get_user_workflow_states', {
            doctype: "Delivery Note",
        }).then(r => {
            const allowed_states = r.message || [];
            if (allowed_states.length) {
                frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Delivery Note",
                        filters: [
                            ["workflow_state", "in", allowed_states]
                        ],
                        fields: [
                            "name", "customer", "custom_department",
                            "custom_site", "posting_date", "workflow_state", "base_grand_total"
                        ],
                        limit_page_length: 500
                    },
                    callback(res) {
                        (res.message || []).forEach(dn => {
                            frm.add_child("delivery_note_approval", {
                                delivery_note: dn.name,
                                customer: dn.customer,
                                department: dn.custom_department,
                                site: dn.custom_site,
                                date: dn.posting_date,
                                grand_total: dn.base_grand_total,
                                status: dn.workflow_state
                            });
                        });

                        frm.refresh_field("delivery_note_approval");
                    }
                });
            }
        });

        frm.fields_dict["po_approval"].grid.add_custom_button(__('Reject'), function () {
            $.each(frm.doc.po_approval || [], function (i, d) {
                if (d.__checked == 1) {
                    let action = null;

                    if (frappe.user.has_role("Contact Manager")) action = "Reject";
                    if (frappe.user.has_role("General Manager")) action = "Reject";
                    if (frappe.user.has_role("IT Dept User"))    action = "Reject";
                    if (frappe.user.has_role("IT Dept Approver")) action = "Reject";

                    if (action) {
                        frm.call('submit_po', {
                            doctype: "Purchase Order",
                            name: d.purchase_order,
                            action: action
                        }).then(r => {
                            frm.get_field("po_approval").grid.grid_rows[d.idx - 1].remove();
                            frm.refresh_field('po_approval');
                        });
                    }
                }
            });
        }).addClass('btn-danger');
        frm.fields_dict["po_approval"].grid.add_custom_button(__('Approve'), function () {
            $.each(frm.doc.po_approval || [], function (i, d) {
                if (d.__checked == 1) {
                    let action = null;

                    if (frappe.user.has_role("Contact Manager") && d.status=='Pending for Contact Manager') action = "Send to General Manager";
                    if (frappe.user.has_role("General Manager") && d.status=='Pending for General Manager') action = "Approve";
                    if (frappe.user.has_role("IT Dept User") && d.status=='Pending for IT Department')    action = "Send to Final Approval";
                    if (frappe.user.has_role("IT Dept Approver") && d.status=='Pending for Final Approval') action = "Approve";

                    if (action) {
                        frm.call('submit_po', {
                            doctype: "Purchase Order",
                            name: d.purchase_order,
                            action: action
                        }).then(r => {
                            frm.get_field("po_approval").grid.grid_rows[d.idx - 1].remove();
                            frm.refresh_field('po_approval');
                        });
                    }
                }
            });
        }).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" });

        frm.fields_dict["mr_approval"].grid.add_custom_button(__('Reject'), function () {
            $.each(frm.doc.mr_approval || [], function (i, d) {
                if (d.__checked == 1) {
                    let action = null;

                    if (frappe.user.has_role("Contact Manager")) action = "Reject";
                    if (frappe.user.has_role("General Manager")) action = "Reject";
                    if (frappe.user.has_role("IT Dept User"))    action = "Reject";
                    if (frappe.user.has_role("IT Dept Approver")) action = "Reject";

                    if (action) {
                        frm.call('submit_po', {
                            doctype: "Material Request",
                            name: d.material_request,
                            action: action
                        }).then(r => {
                            frm.get_field("mr_approval").grid.grid_rows[d.idx - 1].remove();
                            frm.refresh_field('mr_approval');
                        });
                    }
                }
            });
        }).addClass('btn-danger');
        frm.fields_dict["mr_approval"].grid.add_custom_button(__('Approve'), function () {
            $.each(frm.doc.mr_approval || [], function (i, d) {
                if (d.__checked == 1) {
                    let action = null;

                    if (frappe.user.has_role("Site Manager") && d.status =='Pending for Site Manager') action = "Send to Contact Manager";
                    if (frappe.user.has_role("Contact Manager") && d.status =='Pending for Contact Manager') action = "Approve";
                    if (frappe.user.has_role("IT Dept User") && d.status=='Pending for IT Department')    action = "Send to Final Approval";
                    if (frappe.user.has_role("IT Dept Approver") && d.status=='Pending for Final Approval') action = "Approve";

                    if (action) {
                        frm.call('submit_po', {
                            doctype: "Material Request",
                            name: d.material_request,
                            action: action
                        }).then(r => {
                            frm.get_field("mr_approval").grid.grid_rows[d.idx - 1].remove();
                            frm.refresh_field('mr_approval');
                        });
                    }
                }
            });
        }).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" });
        
        frm.fields_dict["la_approval"].grid.add_custom_button(__('Reject'), function () {
            $.each(frm.doc.la_approval || [], function (i, d) {
                if (d.__checked == 1) {
                    let workflow_state = null;

                    if (frappe.user.has_role("Contact Manager") && d.status =='Pending for Contact Manager') workflow_state = "Rejected";
                    if (frappe.user.has_role("General Manager") && d.status =='Pending for General Manager') workflow_state = "Rejected";
                    if (frappe.user.has_role("Site Manager") && d.status =='Pending for Site Manager') workflow_state = "Rejected";
                    if (frappe.user.has_role("HR Coordinator") && d.status =='Pending for HR Coordinator') workflow_state = "Rejected";
                    if (frappe.user.has_role("CEO") && d.status =='Pending for CEO Approval') workflow_state = "Rejected";
                    console.log(workflow_state)
                    if (workflow_state) {
                        frm.call('submit_doc', {
                            doctype: "Leave Application",
                            name: d.leave_application,
                            workflow_state: workflow_state
                        }).then(r => {
                            frm.get_field("la_approval").grid.grid_rows[d.idx - 1].remove();
                            frm.refresh_field('la_approval');
                        });
                    }
                }
            });
        }).addClass('btn-danger');
        frm.fields_dict["la_approval"].grid.add_custom_button(__('Approve'), function () {
            $.each(frm.doc.la_approval || [], function (i, d) {
                if (d.__checked == 1) {
                    let action = null;

                    if (frappe.user.has_role("Contact Manager") && d.status =='Pending for Contact Manager') action = "Send to General Manager";
                    if (frappe.user.has_role("General Manager") && d.status =='Pending for General Manager') action = "Approve";
                    if (frappe.user.has_role("Site Manager") && d.status =='Pending for Site Manager')  action = "Send to HR Coordinator";
                    // if (frappe.user.has_role("HR Coordinator") && d.status =='Pending for HR Coordinator') action = "Send to Contact Manager";
                    if (frappe.user.has_role("HR Coordinator") && d.status === "Pending for HR Coordinator" && d.user_id) {
                        let disallowed_roles1 = ["Project Manager", "CEO", "General Manager", "HR Manager", "IT Dept User"];
                        frm.call('get_user_roles', {
                            user: d.user_id
                        }).then(r => {
                            if (r.message) {
                                let roles = r.message;
                                let disallowed_roles2 = ["Project Manager", "CEO", "General Manager", "HR Manager", "IT Dept User","CFO"];
                                let hasDisallowedRole = disallowed_roles2.some(role => roles.includes(role));
                                if (!hasDisallowedRole) {
                                    action = "Send to Contact Manager";
                                }
                        }
                        });
                    }
                    if (frappe.user.has_role("HR Coordinator") && d.status === "Send to Contact Manager" && d.user_id) {
                        let disallowed_roles1 = ["CFO", "CEO", "General Manager", "HR Manager", "IT Dept User"];
                        frm.call('get_user_roles', {
                            user: d.user_id
                        }).then(r => {
                            if (r.message) {
                                let roles = r.message;
                                let hasallowedRole = disallowed_roles1.some(role => roles.includes(role));
                                if (hasDiallowedRole && !roles.includes('General Manager')) {
                                    action = "Send to General Manager";
                                }
                        }
                        });
                    }
                    if (frappe.user.has_role("HR Coordinator") && d.status === "Pending for HR Coordinator" && d.user_id) {
                        let disallowed_roles1 = ["CFO", "CEO", "General Manager", "HR Manager", "IT Dept User"];
                        frm.call('get_user_roles', {
                            user: d.user_id
                        }).then(r => {
                            if (r.message) {
                                let roles = r.message;
                                if (roles.includes('General Manager')) {
                                    action = "Send to CEO";
                                }
                        }
                        });
                    }
                    if (frappe.user.has_role("HR Coordinator") && d.status =='Pending for HR Coordinator') action = "Send to General Manager";
                    if (frappe.user.has_role("CEO") && d.status =='Pending for CEO Approval') action = "Approve";
                    if (action) {
                        frm.call('submit_po', {
                            doctype: "Leave Application",
                            name: d.leave_application,
                            action: action
                        }).then(r => {
                            frm.get_field("la_approval").grid.grid_rows[d.idx - 1].remove();
                            frm.refresh_field('la_approval');
                        });
                    }
                }
            });
        }).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" });
    },
    onload(frm){
        frappe.breadcrumbs.add("");
        frm.clear_table("la_approval")
        frm.clear_table("delivery_note_approval")
        frm.clear_table("mr_approval")
        frm.clear_table("po_approval")
    },
});
