// Copyright (c) 2025, gifty.p@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Budget', {
	validate(frm) {
		var total_lpo_amount = 0
		var total_business_promotion = 0
		var total_overheads = 0
		var contigency_amount = 0
		var discount = 0
		if (frm.doc.scope_of_work) {

			$.each(frm.doc.scope_of_work, function (i, d) {
				total_lpo_amount += d.amount
				total_business_promotion += d.total_business_promotion
				total_overheads += d.total_overhead
				contigency_amount += d.total_contigency
				discount += d.discount
			})
			frm.set_value('lpo_amount',total_lpo_amount)
			frm.set_value('discount_amount',discount)
			frm.set_value("business_promotion", total_business_promotion)
			
		}
		$.each(frm.doc.scope_of_work, function (i, d) {
			frappe.call({
				method: "frappe.client.get_list",
				args: {
					doctype: "PB SOW",
					filters: {
						project_budget: frm.doc.name,
						sow: d.sow,
						po_li: d.po_li
					},
					fields: ["*"]
				},
				callback(r) {
					$.each(r.message, function (j, k) {
						d.qty = k.qty;
						d.unit = k.uom;
						d.total_overhead = k.overhead_amount;
						d.overhead_ = k.overhead_percent;
						// d.total_amount_as_overhead = k.total_amount_as_overhead;
						// d.total_profit = k.total_profit;
						// d.total_amount_of_profit = k.total_amount_of_profit;
						d.contigency_ = k.contigency_percent;
						d.total_contigency = k.contigency_amount;
						// d.total_overheads = k.total_amount_as_overhead + k.total_amount_of_profit + k.contigency + k.total_amount_as_engineering_overhead;
						// d.total_profit_amount = k.total_profit_amount;
						// d.total_profit_percent = k.total_profit_percent;
						d.total_business_promotion = k.business_promotion_amount;
						// d.total_cost = k.pb_total_cost;
						// d.total_bidding_price = k.pb_bidding_amount;
						// d.unit_price = k.pb_bidding_unit_rate;
						d.gross_profit_amount = k.gross_profit_amount;
						d.gross_profit_ = k.gross_profit_percent;
					})
				}
				
			})
			frm.refresh_field("scope_of_work")
		})
		// $.each(frm.doc.scope_of_work, function (i, d) {
		// 	frappe.call({
		// 		method: "frappe.client.get_list",
		// 		args: {
		// 			'doctype': 'PB SOW',
		// 			filters: {
		// 				'project_budget': frm.doc.name,
		// 				'sow': d.sow,
		// 			},
		// 			fields: ['*']
		// 		},
		// 		callback(r) {
		// 			$.each(r.message, function (j, k) {
		// 				d.qty = k.qty
		// 				d.unit = k.uom
		// 				d.total_overhead = k.total_overhead
		// 				d.total_amount_as_overhead = k.total_amount_as_overhead
		// 				d.total_profit = k.total_profit
		// 				d.total_amount_of_profit = k.total_amount_of_profit
		// 				d.contigency_percent = k.contigency_percent
		// 				d.contigency = k.contigency
		// 				d.engineering_overhead = k.engineering_overhead
		// 				d.total_amount_as_engineering_overhead = k.total_amount_as_engineering_overhead
		// 				d.total_overheads = k.total_amount_as_overhead + k.total_amount_of_profit + k.contigency + k.total_amount_as_engineering_overhead
		// 				d.total_profit_amount = k.total_profit_amount
		// 				d.total_profit_percent = k.total_profit_percent
						
		// 				d.total_cost = k.pb_total_cost
		// 				d.total_bidding_price = k.pb_bidding_amount
		// 				d.unit_price = k.pb_bidding_unit_rate
						
		// 					d.net_profit_percent = k.pb_net_profit_percent
		// 					d.net_profit_amount = k.pb_net_profit_amount
							
						
						
		// 			})

		// 		}
		// 	})
		// 	frm.refresh_field("scope_of_work")
		// })
		
	


	},
    onload(frm) {
        frappe.breadcrumbs.add("Project", "Project Budget");
		if (frm.doc.__islocal) {
		// frm.set_value('date_of_budget',frappe.datetime.nowdate())
		frappe.db.get_value('Sales Order',frm.doc.sales_order,'docstatus')
        .then(r => {
            var value = r.message.docstatus
			if(value == 1){
				if(frm.doc.amended_from){
					let d = new frappe.ui.Dialog({
						title: 'Remarks for Revision',
						fields: [
							
							{
								label: 'Remarks',
								fieldname:'remarks',
								reqd:1,
								fieldtype:'Small Text',
							},
							{
								fieldname:'section',
								fieldtype:'Section Break',
								hidden:1
							},
							{
								label: 'Date',
								fieldname:'date',
								fieldtype:'Date',
								default: frappe.datetime.now_date()
							},
							{
								label: 'Time',
								fieldname:'time',
								fieldtype:'Time',
								default: frappe.datetime.now_time()
							},
						],
						primary_action_label: 'Submit',
						primary_action(values) {
							// if(frm.set_value('revision',values.revision)){
							// 	if(frm.doc.revision == "PB - Revision"){
							// 		var cal = frm.doc.pb_revision + 1
							// 		frm.set_value('pb_revision',cal)
							// 	}
							// 	if(frm.doc.revision == "SO - Revision"){
							// 		var cal = frm.doc.so_revision + 1
							// 		frm.set_value('so_revision',cal)
							// 		frm.set_value('pb_revision',cal)
							// 	}
								d.hide();
							// }
							var value = values.remarks;
							var Date = values.date;
							var Time = values.time;
							let newRemark = {
								date:Date,
								time:Time,
								remarks: value, 
							};
							frm.add_child('remarks', newRemark);
							// frm.doc.remarks.push(newRemark);
							frm.refresh_field('remarks');
							
							}
					});
					
					d.show();
				}
			}
		})
		}
    },
	refresh(frm) {
		frm.add_custom_button(__('Combine'),
		function () {
			frm.trigger('update_so')
		})
		frm.trigger('update_naming')
		if (frm.doc.__islocal) {
			frm.trigger('get_sow_data_from_sales_order')
		}
        // frm.trigger('budget')
	},
    sales_order(frm) {
		frm.trigger('get_sow_data_from_sales_order')
    },
	update_naming: function(frm) {
	    if(frm.doc.__islocal){
        		    if(frm.doc.division=='OETC'){
        		        value = "PB-OETC-.{company_shortcode}.-.YYYY.-"
        		        frm.set_value('naming_series', value)
        		    }
        		    else if(frm.doc.division=='PDO'){
        		        value = "PB-PDO-.{company_shortcode}.-.YYYY.-"
        		        frm.set_value('naming_series', value)
        		    }
        		    else if(frm.doc.division=='General'){
        		        value = "PB-GEN-.{company_shortcode}.-.YYYY.-"
        		        frm.set_value('naming_series', value)
        		    }
        		    else{
        		        value = "PB-.{company_shortcode}.-.YYYY.-"
        		        frm.set_value('naming_series', value)
        		    }
		}
	},
	get_sow_data_from_sales_order: function(frm) {
        frappe.call({
            method: "shaher.shaher.doctype.project_budget.project_budget.get_sow_data_from_sales_order",
            args: {
                sales_order: frm.doc.sales_order
            },
            callback: function(r) {
                if (r.message) {
                    frm.clear_table("scope_of_work");
                    r.message.forEach(row => {
                        let child = frm.add_child("scope_of_work", {
                            po_li: row.po_li,
                            sow: row.sow,
                            sow_desc: row.sow_desc,
                            uom: row.uom,
                            qty: row.qty,
                            unit_price: row.unit_price,
                            amount: row.amount,
                            bidding_amount: row.bidding_amount,
                        });
                    });
                    frm.refresh_field("scope_of_work");
                }
            }
        });
        
    },

	before_workflow_action: async (frm) => {
        if (frm.doc.workflow_state === "Draft") {
            let promise = new Promise((resolve, reject) => {
                if (frm.selected_workflow_action === "Approve") {
                    frappe.run_serially([
                        () => frm.trigger("get_pb_sow"),
                        () => frm.save(),
                        () => frm.trigger("work_title"),
                        () => frm.save(),
                        () => frm.trigger("msow_update"),
                        () => frm.trigger("combine_tables"),
                        () => frm.save(),
                        // () => {
                        //     if (frm.doc.item_table && frm.doc.item_table.length > 0) {
                        //         resolve();
                        //     } else {
                        //         reject("Please save each PBSOW and submit the Project Budget");
                        //     }
                        // }
                    ]).then(() => resolve())
                      .catch(err => reject(err));
                } else {
                    resolve(); // Resolve immediately if not approving
                }
            });
        
            await promise.catch(error => frappe.throw(error));
        }
		if (frm.doc.workflow_state === "In Review") {
            let promise = new Promise((resolve, reject) => {
                if (frm.selected_workflow_action === "Approve") {
					// frappe.dom.freeze();
					frappe.run_serially([
						// () => frm.save(),
						() => frm.trigger("update_so"),
						() => new Promise(resolve => setTimeout(resolve, 2000)),
						() => frm.save(),
						// () => frappe.dom.unfreeze()
					]).then(() => resolve())
				}
				resolve();
			});
			await promise.catch(() => frappe.throw());
			
		}

        
    },
    combine_tables(frm){
		var total_budget_of_the_project  = 0 
		frm.clear_table('item_table')		
		$.each(frm.doc.design,function(i,d){
			total_budget_of_the_project += d.amount
			frm.add_child('item_table',{
				'docname':d.docname,
				'pb_doctype':d.pb_doctype,
				'delivered_qty':d.delivered_qty,
				'billed_qty':d.billed_qty,
				'work_title':d.work_title,
				'item_code':d.item_code,
				'sow':d.sow,
				'item_name':d.item_name,
				'surface_area':d.surface_area,
				'description':d.description,
				'unit':d.unit,
				'qty':d.qty,
				'cost':d.cost,
				'cost_amount':d.cost_amount,
				'unit_price':d.unit_price,
				'amount':d.amount,
				'difference':d.difference,
				'rate_with_overheads':d.rate_with_overheads,
				'amount_with_overheads':d.amount_with_overheads
			})
			frm.refresh_field('item_table')
		})
	
		$.each(frm.doc.supply_materials,function(i,d){
			total_budget_of_the_project += d.amount
			frm.add_child('item_table',{
				'item_code':d.item_code,
				'docname':d.docname,
				'pb_doctype':d.pb_doctype,
				'delivered_qty':d.delivered_qty,
				'billed_qty':d.billed_qty,
				'work_title':d.work_title,
				'sow':d.sow,
				'item_name':d.item_name,
				'surface_area':d.surface_area,
				'description':d.description,
				'unit':d.unit,
				'qty':d.qty,
				'cost':d.cost,
				'cost_amount':d.cost_amount,
				'unit_price':d.unit_price,
				'amount':d.amount,
				'difference':d.difference,
				'rate_with_overheads':d.rate_with_overheads,
				'amount_with_overheads':d.amount_with_overheads
			})
			frm.refresh_field('item_table')
		})
		$.each(frm.doc.finishing_work,function(i,d){
			total_budget_of_the_project += d.amount
			frm.add_child('item_table',{
				'item_code':d.item_code,
				'docname':d.docname,
				'pb_doctype':d.pb_doctype,
				'delivered_qty':d.delivered_qty,
				'billed_qty':d.billed_qty,
				'work_title':d.work_title,
				'sow':d.sow,
				'item_name':d.item_name,
				'surface_area':d.surface_area,
				'description':d.description,
				'unit':d.unit,
				'qty':d.qty,
				'cost':d.cost,
				'cost_amount':d.cost_amount,
				'unit_price':d.unit_price,
				'amount':d.amount,
				'difference':d.difference,
				'rate_with_overheads':d.rate_with_overheads,
				'amount_with_overheads':d.amount_with_overheads
			})
			frm.refresh_field('item_table')
		})
		$.each(frm.doc.accessories,function(i,d){
			total_budget_of_the_project += d.amount
			frm.add_child('item_table',{
				'item_code':d.item_code,
				'docname':d.docname,
				'pb_doctype':d.pb_doctype,
				'delivered_qty':d.delivered_qty,
				'billed_qty':d.billed_qty,
				'work_title':d.work_title,
				'sow':d.sow,
				'item_name':d.item_name,
				'surface_area':d.surface_area,
				'description':d.description,
				'unit':d.unit,
				'qty':d.qty,
				'cost':d.cost,
				'cost_amount':d.cost_amount,
				'unit_price':d.unit_price,
				'amount':d.amount,
				'difference':d.difference,
				'rate_with_overheads':d.rate_with_overheads,
				'amount_with_overheads':d.amount_with_overheads
			})
			frm.refresh_field('item_table')
		})
		$.each(frm.doc.installation,function(i,d){
			total_budget_of_the_project += d.amount
			frm.add_child('item_table',{
				'item_code':d.item_code,
				'docname':d.docname,
				'pb_doctype':d.pb_doctype,
				'delivered_qty':d.delivered_qty,
				'billed_qty':d.billed_qty,
				'work_title':d.work_title,
				'sow':d.sow,
				'item_name':d.item_name,
				'surface_area':d.surface_area,
				'description':d.description,
				'unit':d.unit,
				'qty':d.qty,
				'cost':d.cost,
				'cost_amount':d.cost_amount,
				'unit_price':d.unit_price,
				'amount':d.amount,
				'difference':d.difference,
				'rate_with_overheads':d.rate_with_overheads,
				'amount_with_overheads':d.amount_with_overheads
			})
			frm.refresh_field('item_table')
		})
		$.each(frm.doc.tools__equipment__transport__others,function(i,d){
			total_budget_of_the_project += d.amount
			frm.add_child('item_table',{
				'item_code':d.item_code,
				'docname':d.docname,
				'pb_doctype':d.pb_doctype,
				'delivered_qty':d.delivered_qty,
				'billed_qty':d.billed_qty,
				'work_title':d.work_title,
				'sow':d.sow,
				'item_name':d.item_name,
				'surface_area':d.surface_area,
				'description':d.description,
				'unit':d.unit,
				'qty':d.qty,
				'cost':d.cost,
				'cost_amount':d.cost_amount,
				'unit_price':d.unit_price,
				'amount':d.amount,
				'difference':d.difference,
				'rate_with_overheads':d.rate_with_overheads,
				'amount_with_overheads':d.amount_with_overheads
			})
			frm.refresh_field('item_table')
		})
		$.each(frm.doc.others,function(i,d){
			total_budget_of_the_project += d.amount
			frm.add_child('item_table',{
				'item_code':d.item_code,
				'docname':d.docname,
				'pb_doctype':d.pb_doctype,
				'delivered_qty':d.delivered_qty,
				'billed_qty':d.billed_qty,
				'work_title':d.work_title,
				'sow':d.sow,
				'item_name':d.item_name,
				'surface_area':d.surface_area,
				'description':d.description,
				'unit':d.unit,
				'qty':d.qty,
				'cost':d.cost,
				'cost_amount':d.cost_amount,
				'unit_price':d.unit_price,
				'amount':d.amount,
				'difference':d.difference,
				'rate_with_overheads':d.rate_with_overheads,
				'amount_with_overheads':d.amount_with_overheads
			})
			frm.refresh_field('item_table')
		})
		$.each(frm.doc.finished_goods,function(i,d){
			total_budget_of_the_project += d.amount
			frm.add_child('item_table',{
				'item_code':d.item_code,
				'docname':d.docname,
				'pb_doctype':d.pb_doctype,
				'delivered_qty':d.delivered_qty,
				'billed_qty':d.billed_qty,
				'work_title':d.work_title,
				'sow':d.sow,
				'item_name':d.item_name,
				'surface_area':d.surface_area,
				'description':d.description,
				'unit':d.unit,
				'qty':d.qty,
				'cost':d.cost,
				'cost_amount':d.cost_amount,
				'unit_price':d.unit_price,
				'amount':d.amount,
				'difference':d.difference,
				'rate_with_overheads':d.rate_with_overheads,
				'amount_with_overheads':d.amount_with_overheads
			})
			frm.refresh_field('item_table')
		})
        $.each(frm.doc.raw_materials,function(i,d){
			total_budget_of_the_project += d.amount
			frm.add_child('item_table',{
				'item_code':d.item_code,
				'docname':d.docname,
				'pb_doctype':d.pb_doctype,
				'delivered_qty':d.delivered_qty,
				'billed_qty':d.billed_qty,
				'work_title':d.work_title,
				'sow':d.sow,
				'item_name':d.item_name,
				'surface_area':d.surface_area,
				'description':d.description,
				'unit':d.unit,
				'qty':d.qty,
				'cost':d.cost,
				'cost_amount':d.cost_amount,
				'unit_price':d.unit_price,
				'amount':d.amount,
				'difference':d.difference,
				'rate_with_overheads':d.rate_with_overheads,
				'amount_with_overheads':d.amount_with_overheads
			})
			frm.refresh_field('item_table')
		})		
		$.each(frm.doc.manpower,function(i,d){
			total_budget_of_the_project += d.amount
			frm.add_child('item_table',{
				"item": d.worker,
				'docname':d.docname,
				'pb_doctype':d.pb_doctype,
				'delivered_qty':d.delivered_qty,
				'billed_qty':d.billed_qty,
				'work_title':d.work_title,
				'sow':d.sow,
				"item_name": d.worker,
				"qty": d.total_workers,
				"rate": d.rate_with_overheads,
				'cost':d.cost,
				'unit_price':d.rate,
				"cost_amount":d.cost_amount,
				"estimated_cost":d.estimated_cost,
				"estimated_amount":d.estimated_amount,
				"amount": d.amount,
				"amount_with_overheads": d.amount_with_overheads,
				"rate_with_overheads":d.rate_with_overheads,
			})
			frm.refresh_field('item_table')
		})
		frm.set_value('total_budget_of_the_project',total_budget_of_the_project)	
	},
    get_pb_sow: function (frm) {
        const tables = [
            'design', 'supply_materials', 'raw_materials', 'finishing_work', 'accessories',
            'installation', 'finished_goods', 'heavy_equipments', 'others'
        ];
        tables.forEach(table => frm.clear_table(table));

        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: 'PB SOW',
                filters: { project_budget: frm.doc.name },
                fields: ['name']
            },
            callback(r) {
                (r.message || []).forEach(pb_sow => {
                    frappe.call({
                        method: "frappe.client.get",
                        args: {
                            doctype: 'PB SOW',
                            name: pb_sow.name
                        },
                        callback(resp) {
                            const doc = resp.message;
							console.log(doc.sow)
                            const add_rows = (table, source, work_title, extra_fields = {}) => {
                                (doc[source] || []).forEach(item => {
                                    frm.add_child(table, {
                                        work_title: work_title,
                                        docname: item.name,
                                        pb_doctype: item.doctype,
                                        sow: doc.sow,
                                        item_group: item.item_group,
                                        item_code: item.item_code,
                                        item_name: item.item_name,
                                        description: item.description,
                                        unit: item.unit,
                                        qty: item.qty,
                                        cost: item.cost,
                                        amount: item.amount,
                                    });
                                });
                                frm.refresh_field(table);
                            };

                            add_rows("design", "design", "DESIGN");
                            add_rows("raw_materials", "raw_materials", "RAW MATERIALS");
                            add_rows("supply_materials", "materials", "SUPPLY MATERIALS");
                            // add_rows("materials", "mep_materials", "SUPPLY MATERIALS", { docstatus: 1 });
                            add_rows("finishing_work", "finishing_work", "FINISHING WORK");
                            frm.refresh_field('finishing_work');

                            add_rows("accessories", "accessories", "ACCESSORIES");
                            add_rows("installation", "installation", "INSTALLATION");
                            add_rows("others", "others", "SUBCONTRACT");
                            add_rows("finished_goods", "finished_goods", "FINISHED GOODS", { bom: item => item.bom });
                            add_rows("heavy_equipments", "heavy_equipments", "TOOLS/EQUIPMENTS/TRANSPORT/OTHERS");
                        }
                    });
                });
            }
        });
    },
	update_so(frm){

			frappe.call({
				method:'shaher.shaher.doctype.project_budget.project_budget.update_sows',
				args:{
					document:frm.doc.name,
					sales_order:frm.doc.sales_order
				},
				callback(r){
					
				}
			});
				
	},
	// Update Worktitle
	work_title(frm) {
		frm.clear_table('work_title_summary');
	
		const config = [
			{ tables: ['design'], label: 'DESIGN', qty_key: 'qty', amount_key: 'amount' },
			{ tables: ['supply_materials', 'raw_materials'], label: 'SUPPLY MATERIALS', qty_key: 'qty', amount_key: 'amount' },
			{ tables: ['finishing_work'], label: 'FINISHING WORK', qty_key: 'qty', amount_key: 'amount' },
			{ tables: ['accessories'], label: 'ACCESSORIES', qty_key: 'qty', amount_key: 'amount' },
			{ tables: ['installation'], label: 'INSTALLATION', qty_key: 'qty', amount_key: 'amount' },
			{ tables: ['manpower'], label: 'MANPOWER', qty_key: 'total_workers', amount_key: 'amount' },
			{ tables: ['heavy_equipments'], label: 'TOOLS/EQUIPMENTS/TRANSPORT/OTHERS', qty_key: 'qty', amount_key: 'amount' },
			{ tables: ['manpower_subcontract'], label: 'SUBCONTRACT', qty_key: 'qty', amount_key: 'amount' },
			{ tables: ['finished_goods'], label: 'FINISHED GOODS', qty_key: 'qty', amount_key: 'amount' },
		];
	
		config.forEach(group => {
			let total_qty = 0;
			let total_amount = 0;
	
			group.tables.forEach(table => {
				(frm.doc[table] || []).forEach(row => {
					total_qty += row[group.qty_key] || 0;
					total_amount += row[group.amount_key] || 0;
				});
			});
	
			if (total_qty > 0) {
				frm.add_child("work_title_summary", {
					item_name: group.label,
					quantity: total_qty,
					amount: total_amount
				});
			}
		});
		
		frm.refresh_field('work_title_summary');

	},
msow_update(frm) {
	$.each(frm.doc.scope_of_work, function (i, d) {
		frappe.call({
			method: "frappe.client.get_list",
            args: {
                doctype: "PB SOW",
                filters: {
                    project_budget: frm.doc.name,
                    sow: d.sow,
					po_li: d.po_li
                },
                fields: ["*"]
            },
			callback(r) {
				$.each(r.message, function (j, k) {
					d.qty = k.qty;
					d.unit = k.uom;
					d.total_overhead = k.overhead_amount;
					d.overhead_ = k.overhead_percent;
					// d.total_amount_as_overhead = k.total_amount_as_overhead;
					// d.total_profit = k.total_profit;
					// d.total_amount_of_profit = k.total_amount_of_profit;
					d.contigency_ = k.contigency_percent;
					d.total_contigency = k.contigency_amount;
					// d.total_overheads = k.total_amount_as_overhead + k.total_amount_of_profit + k.contigency + k.total_amount_as_engineering_overhead;
					// d.total_profit_amount = k.total_profit_amount;
					// d.total_profit_percent = k.total_profit_percent;
					d.total_business_promotion = k.business_promotion_amount;
					// d.total_cost = k.pb_total_cost;
					// d.total_bidding_price = k.pb_bidding_amount;
					// d.unit_price = k.pb_bidding_unit_rate;
					d.gross_profit_amount = k.gross_profit_amount;
					d.gross_profit_ = k.gross_profit_percent;
				})
			}
			
		})
		frm.refresh_field("scope_of_work")
	})
}
	

})




frappe.ui.form.on('Budget Scope of Work', {

	budget(frm, cdt, cdn) {
		frm.save()
		var child = locals[cdt][cdn]

		frappe.db.get_value('PB SOW', { 'project_budget': frm.doc.name, 'sow': child.sow, 'po_li': child.po_li }, 'name')
			.then(r => {
				if (r.message && Object.entries(r.message).length === 0) {
					frappe.route_options = {
						'project_budget': frm.doc.name,
						'sales_order': frm.doc.sales_order,
						'company': frm.doc.company,
						'sow': child.sow,
						'qty': child.qty,
						'uom': child.unit,
                        'po_li': child.po_li,
                        'uom': child.uom,
                        'lpo_amount': child.amount,
					}
					frappe.new_doc('PB SOW')
				}
				else {
					frappe.route_options = {
						'project_budget': frm.doc.name,
						'sales_order': frm.doc.sales_order,
						'company': frm.doc.company,
						'sow': child.sow,
						'qty': child.qty,
						'uom': child.unit,
                        'po_li': child.po_li,
                        'uom': child.uom,
					}
					frappe.set_route('Form', 'PB SOW', r.message.name)
				}
			})

	}
});