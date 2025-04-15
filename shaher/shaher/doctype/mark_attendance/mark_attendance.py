# mark_attendance.py
import frappe
from frappe.model.document import Document
from datetime import datetime


import frappe
from frappe.model.document import Document

class MarkAttendance(Document):
    
    def on_submit(self):
        # Check if the user has the "HOD" role
        if "HOD" not in frappe.get_roles(frappe.session.user):
            frappe.throw("You do not submit have permission to mark attendance.")

        if not self.out_time:
            
            frappe.throw("Please provide 'Out Time' before submitting.")
    



        # Mark IN time
        if self.in_time:
            ec = frappe.new_doc("Employee Checkin")
            ec.employee = self.employee
            ec.employee_name = self.employee_name
            ec.time = self.in_time
            ec.log_type = "IN"
            ec.device_id = "Shaher IN"
            ec.marked_for_mobile = 1
            ec.save(ignore_permissions=True)
            
            frappe.db.commit()
        
        # Mark OUT time
        if self.out_time:
            ec = frappe.new_doc("Employee Checkin")
            ec.employee = self.employee
            ec.employee_name = self.employee_name
            ec.time = self.out_time
            ec.log_type = "OUT"
            ec.device_id = "Shaher OUT"
            ec.marked_for_mobile = 1
            ec.save(ignore_permissions=True)
            
            frappe.db.commit()

        frappe.msgprint("Employee Checkin marked successfully!")

       





# @frappe.whitelist()
# def fetch_geolocation_details(lat, lon):
#     """
#     Fetch geolocation details from the Nominatim API using latitude and longitude.
#     """
#     try:
#         # Convert and validate inputs
#         lat = float(lat)
#         lon = float(lon)

#         # Make the API request
#         url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
#         response = requests.get(url)

#         if response.status_code == 200:
#             data = response.json()
#             address = data.get("address", {})
#             return {
#                 "display_name": data.get("display_name", ""),
#                 "state_district": address.get("state_district", ""),
#                 "state": address.get("state", ""),
#                 "postcode": address.get("postcode", "")
#             }
#         else:
#             frappe.throw(f"Error fetching geolocation data: HTTP {response.status_code}")

#     except ValueError:
#         frappe.throw("Latitude and Longitude must be valid floating-point numbers.")
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Error in fetch_geolocation_details")
#         frappe.throw(f"An error occurred while fetching geolocation details: {str(e)}")


