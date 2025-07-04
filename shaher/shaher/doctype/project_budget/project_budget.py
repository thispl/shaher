# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ProjectBudget(Document):
	def after_insert(self):
		if self.amended_from:
			# pro = frappe.db.exists("Project",{'budgeting':self.amended_from})
			# if pro:
			# 	project = frappe.get_doc("Project",{'budgeting':self.amended_from})
			# 	project.budgeting = self.name
			# 	project.save(ignore_permissions = True)
			pb_sow = frappe.get_all("PB SOW",{'project_budget':self.amended_from},['name','project_budget'])
			for pb in pb_sow:
				pbs = frappe.get_doc("PB SOW",{'name':pb.name,'project_budget':pb.project_budget})
				pbs.project_budget = self.name
				pbs.save(ignore_permissions=True)
			# update PB in MR
			# mrs = frappe.get_all("Material Request", 
			# 			filters={"project_budget": self.amended_from, "docstatus": 1}, 
			# 			pluck="name")
			# for mr_name in mrs:
			# 	mr = frappe.get_doc("Material Request", mr_name)
			# 	mr.project_budget = self.name
			# 	mr.save(ignore_permissions=True)
		sales_order = frappe.get_doc("Sales Order", self.sales_order)
		sales_order.custom_project_budget = self.name
		sales_order.save()


@frappe.whitelist()
def get_sow_data_from_sales_order(sales_order):
	sales_order_doc = frappe.get_doc("Sales Order", sales_order)
	scope_data = []

	for so_row in sales_order_doc.items:
		scope_data.append({
			"po_li": so_row.custom_po_li,
			"sow": so_row.item_code,
			"sow_desc": so_row.item_name,
			"uom": so_row.uom,
			"qty": so_row.qty,
			"unit_price": so_row.rate,
			"amount": so_row.amount,
		})

	return scope_data

@frappe.whitelist()
def update_sows(document,sales_order):

	doc = frappe.get_doc("Project Budget",document)
	so = frappe.get_doc('Sales Order',sales_order)
	so.set('custom_item_table', [])
	so.set('custom_supply_materials', [])
	so.set('custom_installation', [])
	so.set('custom_tools', [])
	so.set('custom_finished_goods', [])
	so.set('custom_accessories', [])
	so.set('custom_finishing_work', [])
	so.set('custom_raw_materials', [])
	so.set('custom_design', [])
	for itm in doc.item_table:
		so.append("custom_item_table",{
			"sow":itm.sow,
			"item_code":itm.item_code,
			"item_name":itm.item_name,
			"description":itm.description,
			"qty":itm.qty,
			"amount":itm.amount,
			
			"rate":itm.cost,
			
		})

	for des in doc.design:
		so.append("custom_design",{
			"sow":des.sow,
			"item_code":des.item_code,
			"item_name":des.item_name,
			"surface_area":des.surface_area,
			"item_group":des.item_group,
			"description":des.description,
			"unit":des.unit,
			"qty":des.qty,
			"amount":des.amount,
			
			"cost":des.cost,
			
		})


	for mat in doc.supply_materials:
		so.append("custom_supply_materials",{
			"sow":mat.sow,
			"item_code":mat.item_code,
			"item_name":mat.item_name,
			"surface_area":mat.surface_area,
			"item_group":mat.item_group,
			"description":mat.description,
			"unit":mat.unit,
			"qty":mat.qty,
			
			"amount":mat.amount,
			
			"cost":mat.cost,
			
		})

	for ins in doc.installation:
		so.append("custom_installation",{
			"sow":ins.sow,
			"item_code":ins.item_code,
			"item_name":ins.item_name,
			"surface_area":ins.surface_area,
			"item_group":ins.item_group,
			"description":ins.description,
			"unit":ins.unit,
			"qty":ins.qty,
			
			"amount":ins.amount,
			
			"cost":ins.cost,
			
		})
	for hv in doc.tools__equipment__transport__others:
		so.append("custom_tools",{
			"sow":hv.sow,
			"item_code":hv.item_code,
			"item_name":hv.item_name,
			"surface_area":hv.surface_area,
			"item_group":hv.item_group,
			"description":hv.description,
			"unit":hv.unit,
			"qty":hv.qty,
			
			"amount":hv.amount,
			
			"cost":hv.cost,
			
		})

	for fg in doc.finished_goods:
		so.append("custom_finished_goods",{
			"sow":fg.sow,
			"item_code":fg.item_code,
			"item_name":fg.item_name,
			"surface_area":fg.surface_area,
			"item_group":fg.item_group,
			"description":fg.description,
			"unit":fg.unit,
			"qty":fg.qty,
			
			"amount":fg.amount,
			
			"cost":fg.cost,
			
		})

		
	for fw in doc.finishing_work:
		so.append("custom_finishing_work",{
			"sow":fw.sow,
			"item_code":fw.item_code,
			"item_name":fw.item_name,
			"surface_area":fw.surface_area,
			"item_group":fw.item_group,
			"description":fw.description,
			"unit":fw.unit,
			"qty":fw.qty,
			
			"amount":fw.amount,
			
			"cost":fw.cost,
			
		})
	
	for ba in doc.accessories:
		so.append("custom_accessories",{
			"sow":ba.sow,
			"item_code":ba.item_code,
			"item_name":ba.item_name,
			"surface_area":ba.surface_area,
			"item_group":ba.item_group,
			"description":ba.description,
			"unit":ba.unit,
			"qty":ba.qty,
			
			"amount":ba.amount,
			
			"cost":ba.cost,
			
		})
	for ra in doc.raw_materials:
		so.append("custom_raw_materials",{
			"sow":ra.sow,
			"item_code":ra.item_code,
			"item_name":ra.item_name,
			"surface_area":ra.surface_area,
			"item_group":ra.item_group,
			"description":ra.description,
			"unit":ra.unit,
			"qty":ra.qty,
			
			"amount":ra.amount,
			
			"cost":ra.cost,
			
		})
	
	# for work_title in doc.work_title_summary:
	# 	so.append("so_work_title_item",{
	# 		"item_name":work_title.item_name,
	# 		"quantity":work_title.quantity,
	# 		"amount":work_title.amount,
	# 	})
	# so.total_bidding_price = total_bidding_price
	so.save(ignore_permissions=True)

