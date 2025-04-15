# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now

class VehicleMaintenanceCheckList(Document):
	def validate(self):
		if self.is_new():
			vehicle = frappe.db.sql("""
				SELECT work_finished_date, present_kilometer 
				FROM `tabVehicle Maintenance Check List` 
				WHERE register_no = %s AND docstatus = 1 
				ORDER BY creation DESC LIMIT 1
			""", (self.register_no,), as_dict=True)

			if vehicle:  # Check if the query returned a result
				self.last_service_date = vehicle[0]['work_finished_date']
			else:
				self.last_service_date = None# Or set a default value


	def on_submit(self):
		# po = frappe.new_doc("Purchase Order")
		# po.supplier = self.supplier
		# po.posting_date = now()
		# po.company = self.company
		# po.custom_division = "Vehicle"
		# po.custom_vehicle_maintenance_check = self.name
		# po.custom_vehicle_service_item = self.vehicle_service
		# po.append("items",{
		# 	"item_code" : "Vehicle Maintenance Check",
		# 	"qty":"1",
		# 	"uom": "Nos",
		# 	"item_name":f"{self.register_no}",
		# 	"description": f"Vehicle {self.register_no} - {self.vehicle_service}",
		# 	"rate":self.actual_expense,
		# 	"amount":self.actual_expense,
		# 	"schedule_date": self.work_finished_date,
		# 	"custom_vehicle_maintenance_check": self.name,
		# 	"custom_vehicle": self.register_no,
		# })
		# po.save(ignore_permissions = True)

		# self.purchase_order = po.name
  
		vehicle = frappe.get_doc("Vehicle",{'name':self.register_no})
		vehicle.last_odometer = self.present_kilometer
		vehicle.append('custom_vehicle_maintanance_log',{
			"type":"Maintenance",
			"employee":self.employee_id,
			"date":self.work_finished_date,
			"vehicle_service": self.vehicle_service,
			"document":self.name,
			"cost": self.actual_expense,
			"purchase_order": self.purchase_order,

		})
		vehicle.save(ignore_permissions=True)
		frappe.db.commit()

	def on_cancel(self):
		if frappe.db.exists("Purchase Order", {"custom_vehicle_maintenance_check": self.name}):
			po = frappe.get_doc("Purchase Order", {"custom_vehicle_maintenance_check": self.name})
			if po.docstatus == 1:
				po.cancel()
			else:
				po.delete()
  
@frappe.whitelist()
def register_no(register_no):
	if frappe.db.exists("Vehicle Maintenance Check List", {"register_no": register_no, "docstatus": 1}):
		vehicle = frappe.db.sql("""SELECT work_finished_date, present_kilometer FROM `tabVehicle Maintenance Check List` WHERE register_no = '%s' docstatus = 1 ORDER BY creation DESC LIMIT 1""" % register_no, as_dict=True)[0] or 0
		return vehicle
	

