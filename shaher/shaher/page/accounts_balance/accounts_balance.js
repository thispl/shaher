// frappe.pages['accounts-balance'].on_page_load = function(wrapper) {
// 	var page = frappe.ui.make_app_page({
// 		parent: wrapper,
// 		title: 'None',
// 		single_column: true
// 	});
// }

frappe.pages['accounts-balance'].on_page_load = function(wrapper) {
    let page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Dimension-wise Accounts Balance',
        // single_column: true
    });

    // Filters
    // let filters = {
    //     company: frappe.ui.form.make_control({
    //         df: {
    //             fieldname: "company",
    //             label: "Company",
    //             fieldtype: "Link",
    //             options: "Company",
    //             reqd: 1
    //         },
    //         parent: page.page.form,
    //         render_input: true
    //     }),
    //     from_date: frappe.ui.form.make_control({
    //         df: {
    //             fieldname: "from_date",
    //             label: "From Date",
    //             fieldtype: "Date",
    //             reqd: 1
    //         },
    //         parent: page.page.form,
    //         render_input: true
    //     }),
    //     to_date: frappe.ui.form.make_control({
    //         df: {
    //             fieldname: "to_date",
    //             label: "To Date",
    //             fieldtype: "Date",
    //             reqd: 1
    //         },
    //         parent: page.page.form,
    //         render_input: true
    //     }),
    // };

    // page.add_button('Show Report', () => {
    //     let filter_values = {
    //         company: filters.company.get_value(),
    //         from_date: filters.from_date.get_value(),
    //         to_date: filters.to_date.get_value()
    //     };

    //     if (!filter_values.company || !filter_values.from_date || !filter_values.to_date) {
    //         frappe.msgprint("Please fill in all filters.");
    //         return;
    //     }

    //     frappe.call({
    //         method: "erpnext.accounts.report.dimension_wise_accounts_balance_report.dimension_wise_accounts_balance_report.execute",
    //         args: { filters: filter_values },
    //         callback: function(r) {
    //             if (r.message) {
    //                 render_datatable(r.message[0], r.message[1]);
    //             }
    //         }
    //     });
    // });

    // // Placeholder for DataTable
    // let table_wrapper = $(`<div class="report-table mt-4"></div>`).appendTo(page.body);

    // function render_datatable(columns, data) {
    //     // Clear previous
    //     table_wrapper.empty();

    //     const datatable = new frappe.DataTable(table_wrapper[0], {
    //         columns: columns.map(col => ({
    //             name: col.label,
    //             id: col.fieldname,
    //             editable: false,
    //             format: value => {
    //                 if (col.fieldtype === "Currency" && value !== null) {
    //                     return format_currency(value);
    //                 }
    //                 return value;
    //             }
    //         })),
    //         data: data,
    //         layout: 'fixed',
    //         no_data_message: "No records found"
    //     });
    // }
};
