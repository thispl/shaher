# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class HSE(Document):
    def before_insert(self):
        if self.employee:
            employee_doc = frappe.get_doc('Employee', self.employee)
            for j in employee_doc.get("custom_hse_training_matrix"):  
                self.append("hse_training_matrix", {
                    "course_name": j.course_name,
                    "course_group": j.course_group,
                    "expiry_date": j.expiry_date,
                    "validity": j.validity
                })
            for j in employee_doc.get("custom_ftw_register"):  
                self.append("ftw_register", {
                    "medical_test_done_on": j.medical_test_done_on,
                    "next_due_date": j.next_due_date,
                    "results__fitunfit": j.results__fitunfit,
                    "remarks_from_doctor": j.remarks_from_doctor
                })


def generate_html_table(docname):
    doc = frappe.get_doc('Purchase Order', docname)
    html = """
    <table border="1" style="width:100%; border-collapse:collapse;">
        <thead style="display: table-header-group;">
            <tr>
                <td style="text-align:center;background-color:#b81a0f;color:white;width:9%;">Sl No</td>
                <td style="text-align:center;background-color:#b81a0f;color:white;width:20%;">Item Code</td>
                <td style="text-align:center;background-color:#b81a0f;color:white;">Description</td>
                <td style="text-align:center;background-color:#b81a0f;color:white;">Qty</td>
                <td style="text-align:center;background-color:#b81a0f;color:white;">Unit</td>
                <td style="text-align:center;background-color:#b81a0f;color:white;">Rate</td>
                <td style="text-align:center;background-color:#b81a0f;color:white;">Amount</td>
            </tr>
        </thead>
        <tbody>
    """

    for idx, item in enumerate(doc.get("items", []), start=1):
        html += f"""
            <tr>
                <td>{idx}</td>
                <td>{item.get("item_code", "")}</td>
                <td>{item.get("description", "")}</td>
                <td style="text-align:right">{float(item.get("qty", 0)):.2f}</td>
                <td>{item.get("uom", "")}</td>
                <td style="text-align:right">{float(item.get("rate", 0)):.3f}</td>
                <td style="text-align:right">{float(item.get("amount", 0)):.3f}</td>
            </tr>
        """

    html += """
        </tbody>
    </table>
    """
    return html
