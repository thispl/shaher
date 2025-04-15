# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MultiVehicleMaintenanceCheck(Document):
	def validate(self):
		for v in self.vehicle:
			vmc = frappe.new_doc("Vehicle Maintenance Check List")
			vmc.multi_vehicle_maintenance_check_list = self.name
			vmc.make = v.make
			vmc.register_no = v.register_no
			vmc.vehicle_name = v.vehicle_name
			vmc.model = v.model
			vmc.type_of_vehicle = v.type_of_vehicle
			vmc.type_of_vehicle = v.type_of_vehicle
			vmc.driver = v.driver
			vmc.last_kilometer = v.last_kilometer
			vmc.last_service_date = v.last_service_date
			vmc.present_kilometer = v.present_kilometer
			vmc.vehicle_service = self.vehicle_service
			vmc.actual_expense = self.actual_expense
			vmc.time_to_finish_work = self.time_to_finish_work
			vmc.vehicle_handover_date = self.vehicle_handover_date
			vmc.approximate_exp = self.approximate_exp
			vmc.complaint = self.complaint
			vmc.supplier = self.supplier
			vmc.supplier_type = self.supplier_type
			vmc.hr_manager = vmc.hr_manager
			for e in self.employee:
				if vmc.register_no == e.register_no:
					vmc.employee_id = e.employee_id
					vmc.date_of_joining = e.date_of_joining
					vmc.driver_name = e.driver_name
					vmc.company = e.company
				vmc.save(ignore_permissions=True)