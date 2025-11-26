# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.workflow import apply_workflow

class ApprovalSummary(Document):
    # pass
    @frappe.whitelist()
    def submit_doc(self,doctype,name,workflow_state):
        doc = frappe.get_doc(doctype,name)
        doc.workflow_state = workflow_state
        if workflow_state=="Approved":
            doc.status="Approved"
        else:
            if workflow_state=="Rejected":
                if doctype =='Leave Application':
                    doc.status="Rejected"
        doc.save(ignore_permissions=True)
        if workflow_state == "Approved":
            doc.submit()
        elif workflow_state == "Rejected":
            if doctype =='Leave Application':
                doc.submit()
        return "ok"
    
    @frappe.whitelist()
    def submit_dn(self,doctype,name,workflow_state):
        frappe.errprint("inside")
        doc = frappe.get_doc(doctype,name)
        doc.workflow_state = workflow_state
        doc.save(ignore_permissions=True)
        if workflow_state == "To Bill" or workflow_state=="Pending for SE":
            if doc.docstatus==0:
                doc.submit()
        return "ok"

    @frappe.whitelist()
    def submit_mr(self,doctype,name,workflow_state):
        frappe.errprint("inside")
        doc = frappe.get_doc(doctype,name)
        doc.workflow_state = workflow_state
        doc.save(ignore_permissions=True)
        if workflow_state == "Approved" or workflow_state=="Rejected":
            if doc.docstatus==0:
                doc.submit()
        return "ok"


    @frappe.whitelist()
    def get_user_roles(self,user):
        return frappe.get_all("Has Role", filters={"parent": user}, pluck="role")
    @frappe.whitelist()
    def submit_po(self,doctype, name, action):
        doc = frappe.get_doc(doctype, name)
        apply_workflow(doc, action)  

        return {"name": doc.name, "workflow_state": doc.workflow_state}


    @frappe.whitelist()
    def get_user_workflow_states(self,doctype):
        workflows = frappe.get_all(
            "Workflow",
            filters={"document_type": doctype, "is_active": 1},
            pluck="name"
        )
        if not workflows:
            return []
        states_roles = frappe.get_all(
            "Workflow Document State",
            filters={"parent": ["in", workflows],'state':["not in",['Approved','Rejected','Cancelled','Draft']]},
            fields=["state", "allow_edit"]
        )

        user_roles = frappe.get_roles(frappe.session.user)

        allowed_states = [
            s["state"] for s in states_roles if s["allow_edit"] in user_roles
        ]
        return sorted(set(allowed_states))

        