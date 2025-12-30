// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Upload Employee Attendance", {
    //  refresh(frm) {
    //     setTimeout(() => {
    //         attach_food_allowance_events();
    //     }, 300);
    // },
    view_data(frm) {
    if(!frm.doc.__islocal){
         const method_name = frm.doc.division == "PDO"
        ? "shaher.shaher.doctype.upload_employee_attendance.upload_employee_attendance.preview_html"
        : "shaher.shaher.doctype.upload_employee_attendance.upload_employee_attendance.preview_html_oetc";

    frappe.call({
        method: method_name,
        args: { name: frm.doc.name },
        callback(r) {

            let d = new frappe.ui.Dialog({
                title: "Attendance & OT Register Preview",
                size: "extra-large",
                primary_action_label: "Update Register",
                primary_action() {
                    update_register(frm, d);
                }
            });
            d.$wrapper.find('.modal-dialog').css({
                'max-width': '95%',
                'width': '95%'
            });

            d.$wrapper.find('.modal-content').css({
                'min-height': '100%',
                'height': '100%'
            });
            // Select / Deselect all (ignore disabled)
            d.$wrapper.on('change', '#select_all', function () {
                d.$wrapper.find('.emp_select:not(:disabled)')
                    .prop('checked', this.checked);
            });
            // Make food_allowance read-only in dialog
            // Update header checkbox on row change
            d.$wrapper.on('change', '.emp_select', function () {
                const total = d.$wrapper.find('.emp_select:not(:disabled)').length;
                const checked = d.$wrapper.find('.emp_select:not(:disabled):checked').length;

                $('#select_all')
                    .prop('checked', total === checked)
                    .prop('indeterminate', checked > 0 && checked < total);
            });
                        // Live update food allowance when breakfast / lunch / dinner changes
            d.$wrapper.on('input', '.edit-field', function () {

                const field = $(this).data('field');

                // Run only for food-related fields
                if (!['breakfast', 'lunch', 'dinner'].includes(field)) return;

                const row = $(this).closest('tr');

                const breakfast = parseFloat(
                    row.find('[data-field="breakfast"]').val()
                ) || 0;

                const lunch = parseFloat(
                    row.find('[data-field="lunch"]').val()
                ) || 0;

                const dinner = parseFloat(
                    row.find('[data-field="dinner"]').val()
                ) || 0;

                const food_allowance = breakfast + (lunch * 2) + (dinner * 2);

                row.find('[data-field="food_allowance"]').val(food_allowance);
            });

            d.body.innerHTML = `
                <div class="attendance-preview-wrapper"
                    style="max-height:100vh; overflow:auto; border:1px solid #ccc; white-space:nowrap;">
                    ${r.message}
                </div>
                
            `;

            // 🔹 Add Submit Button
            d.set_secondary_action_label("Submit");
d.set_secondary_action(() => {
    let rows = d.body.querySelectorAll("tbody tr");
    let selected = [];

    rows.forEach(row => {
        let checkbox = row.querySelector(".emp_select");
        if (!checkbox || !checkbox.checked) return;

        let regname = row.getAttribute("data-regname");
        if (regname) {
            selected.push(regname);
        }
    });

    if (selected.length === 0) {
        frappe.msgprint("No employees selected!");
        return;
    }

    frappe.confirm(
        "Once submitted, selected registers cannot be edited. Do you want to continue?",
        () => {
            frappe.call({
                method: "shaher.shaher.doctype.upload_employee_attendance.upload_employee_attendance.submit_selected_registers",
                args: {
                    registers: selected
                },
                freeze: true,
                callback: function () {
                    frappe.show_alert({ message: "Submitted Successfully", indicator: "green" });
                    d.hide();
                    frm.reload_doc();
                }
            });
        }
    );
});


            d.show();
        }
    });
    }
    },



    setup(frm){
        frm.set_query("department", function() {
            return {
                "filters": {
                    "company": frm.doc.company
                }
            };
        });
    },
    // onload: function(frm) {
    //     frm.set_df_property('html', 'options',
    //         `<strong>Attendance Status:</strong>
    //         <ul style="list-style-type: none; padding-left: 0; margin-top: 5px;">
    //             <li><strong style="color: green;">P</strong> – Present</li>
    //             <li><strong style="color: red;">A</strong> – Absent</li>
    //             <li><strong style="color: orange;">RD</strong> – Rest Day</li>
    //             <li><strong style="color: blue;">HD</strong> – Half Day</li>
    //             <li>
    //             <span style="
    //             background-color: #D9D9D9;
    //             padding: 2px 6px;
    //             font-weight: bold;
    //             border: 1px solid #999;
    //             ">
    //             Grey
    //             </span>
    //             – Not Applicable (Before Date of Joining / After Relieving Date)
    //         </li>
    //         </ul>`
    //     );
    // },
    to_date: function(frm) {
        if (frm.doc.from_date && frm.doc.to_date) {
            if (frm.doc.from_date > frm.doc.to_date) {
                frm.set_value('to_date', null); 
                frappe.msgprint(__('To Date cannot be less than From Date'));
            }
        }
    },
    from_date: function(frm) {
        if (frm.doc.from_date && frm.doc.to_date) {
            if (frm.doc.from_date > frm.doc.to_date) {
                frm.set_value('from_date', null);
                frappe.msgprint(__('From Date cannot be greater than To Date'));
            }
        }
    },
	download: function (frm) {
        window.location.href = repl(frappe.request.url +
                 '?cmd=%(cmd)s&from_date=%(from_date)s&to_date=%(to_date)s&department=%(department)s&designation=%(designation)s&company=%(company)s&site_location=%(site_location)s&name=%(name)s',{
                 cmd: "shaher.shaher.doctype.upload_employee_attendance.upload_employee_attendance.get_template",
                 from_date: frm.doc.from_date,
                 to_date: frm.doc.to_date,
                 department:frm.doc.department,
                 designation:frm.doc.designation,
                 company:frm.doc.company,
                 site_location: frm.doc.site_location,
                 name:frm.doc.name
             })
         },
    download_template: function (frm) {
        if (!frm.doc.division){
            frappe.throw("Kindly enter the division.")
        }
        window.location.href = repl(frappe.request.url +
                 '?cmd=%(cmd)s&from_date=%(from_date)s&to_date=%(to_date)s&department=%(department)s&designation=%(designation)s&company=%(company)s&site_location=%(site_location)s&name=%(name)s&division=%(division)s',{
                 cmd: "shaher.shaher.doctype.upload_employee_attendance.pdo_upload_format.get_template",
                 from_date: frm.doc.from_date,
                 to_date: frm.doc.to_date,
                 department:frm.doc.department,
                 designation:frm.doc.designation,
                 company:frm.doc.company,
                 site_location: frm.doc.site_location,
                 name:frm.doc.name,
                 division:frm.doc.division
             })
         },
    
});

function update_register(frm, dialog) {
    let rows = dialog.body.querySelectorAll("tbody tr");
    let updates = [];

    rows.forEach(row => {
        let checkbox = row.querySelector(".emp_select");
        if (!checkbox || !checkbox.checked) return;

        let regname = row.getAttribute("data-regname");
        let fields = row.querySelectorAll(".edit-field");
        let updated_data = {};

        fields.forEach(f => {
            updated_data[f.dataset.field] = f.value;
        });

        updates.push({
            register: regname,
            fields: updated_data
        });
    });

    if (updates.length === 0) {
        frappe.msgprint("No employees selected!");
        return;
    }

    frappe.call({
        method: "shaher.shaher.doctype.upload_employee_attendance.upload_employee_attendance.update_register_data",
        args: { updates: updates },
        freeze: true,
        callback: function () {
            frappe.show_alert({ message: "Updated Successfully", indicator: "green" });
            dialog.hide();
            frm.reload_doc();
        }
    });
}


function submitAO(docname) {
    frappe.call({
        method: "frappe.client.submit",
        args: {
            doctype: "Attendance and OT Register",
            name: docname
        },
        callback() {
            frappe.show_alert("Record submitted");
        }
    });
}
function attach_food_allowance_events() {
    document.querySelectorAll(".food-input").forEach(input => {
        input.removeEventListener("input", food_input_handler);
        input.addEventListener("input", food_input_handler);
    });

    // initial calculation
    document.querySelectorAll("tr[data-regname]").forEach(row => {
        calculateFoodAllowance(row);
    });
}

function food_input_handler() {
    calculateFoodAllowance(this.closest("tr"));
}

function calculateFoodAllowance(row) {
    const getVal = (field) => {
        const el = row.querySelector(`[data-field="${field}"]`);
        return el ? parseFloat(el.value) || 0 : 0;
    };

    const breakfast = getVal("breakfast");
    const lunch = getVal("lunch");
    const dinner = getVal("dinner");

    const foodAllowance = breakfast + (2 * lunch) + (2 * dinner);

    const foodField = row.querySelector('[data-field="food_allowance"]');
    if (foodField) {
        foodField.value = foodAllowance.toFixed(2);
    }
}