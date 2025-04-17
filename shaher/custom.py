import frappe
import frappe
from frappe import _
from frappe.utils import date_diff, today, add_days, nowdate, unique, cstr
from frappe import _
import math
from frappe.utils.background_jobs import enqueue
from datetime import datetime, time, timedelta
from frappe.utils import cint, flt, formatdate, get_link_to_form, getdate, now,time_diff_in_hours
from frappe.utils import getdate, get_datetime
import calendar
from frappe.model.mapper import get_mapped_doc

#Show the below details while open the quotation document if there in profit percentage
@frappe.whitelist()
def margin_html(mar_dis_per,mar_tot_cost,mar_gross_tot,mar_dis_amt,total_selling,prof_per,margin_profit):
	data = ''
	data = "<table style='width:85%'>"
	data += "<tr><td style ='background-color:#dedede;font-weight:bold;text-align:center;border:1px solid black'>TOTAL COST</td><td style ='font-weight:bold;text-align:center;border:1px solid black'>%s</td><td style ='background-color:#dedede;font-weight:bold;text-align:center;border:1px solid black'>GROSS TOTAL SELLING</td><td style ='font-weight:bold;text-align:center;border:1px solid black'>%s</td></tr>"%(round(float(mar_tot_cost),2),round(float(mar_gross_tot),2))
	data += "<tr><td colspan  = 2 style = 'border:1px solid black;border-right-color:#dedede;background-color:#dedede;'><td style ='border-left-color:#dedede;background-color:#dedede;font-weight:bold;text-align:center;border:1px solid black'>DISCOUNT PERCENTAGE</td><td style ='background-color:#74cee7;font-weight:bold;text-align:center;border:1px solid black'>%s</td></tr>"%(round(float(mar_dis_per),2))
	data += "<tr><td style ='background-color:#dedede;font-weight:bold;text-align:center;border:1px solid black'>PROFIT PERCENTAGE</td><td style ='background-color:#74cee7;font-weight:bold;text-align:center;border:1px solid black'>%s</td><td style ='background-color:#dedede;font-weight:bold;text-align:center;border:1px solid black'>DISCOUNT AMOUNT</td><td style ='background-color:#74cee7;font-weight:bold;text-align:center;border:1px solid black'>%s</td></tr>"%(round(float(prof_per),2),round(float(mar_dis_amt),2))
	data += "<tr><td style ='background-color:#dedede;font-weight:bold;text-align:center;border:1px solid black'>PROFIT AMOUNT</td><td style ='background-color:#74cee7;font-weight:bold;text-align:center;border:1px solid black'>%s</td><td style ='background-color:#dedede;font-weight:bold;text-align:center;border:1px solid black'>TOTAL SELLING</td><td style ='font-weight:bold;text-align:center;border:1px solid black'>%s</td></tr>"%(round(float(margin_profit),2),round(float(total_selling),2))
	data += "</table>"
	return data

#creates Item Code based on the Item Description
@frappe.whitelist()
def create_item_code(description):
	if not frappe.db.exists("Item",{'description':description,'disabled':0}):
		item=frappe.new_doc("Item")
		item.item_name=description
		item.description=description
		item.item_group="Services"
		item.item_code = ''.join([word[0].upper() for word in description.split() if word.isalpha()])
		item.save(ignore_permissions=True)
		return item.name
	else:
		item_code=frappe.get_doc("Item",{'description':description,'disabled':0})
		return item_code

#create user and user_permission for supplier
@frappe.whitelist()
def create_user_permission(supplier_name,name,user_id):
	if frappe.db.exists("User",{'name':user_id,'enabled':1}):
		user=frappe.get_doc("User",{'name':user_id,'enabled':1})
		user.append("roles",{
			"role":"Supplier"
		})
		user.module_profile='Supplier'
		user.save(ignore_permissions=True)
		if not frappe.db.exists("User Permission",{'user':user_id,'allow':'Supplier','for_value':name}):
			usr_per=frappe.new_doc("User Permission")
			usr_per.user=user_id
			usr_per.allow='Supplier'
			usr_per.for_value=name
			usr_per.save(ignore_permissions=True)
		import string
		import random
		all_characters = string.ascii_letters + string.digits
		length = 6
		password = ''.join(random.choices(all_characters, k=length))
		if password:
			from frappe.utils.password import update_password

			update_password(user=user.name, pwd=password)
	else:
		user=frappe.new_doc("User")
		user.email=user_id
		user.send_welcome_email=0
		user.first_name=supplier_name
		user.append("roles",{
			"role":"Supplier"
		})
		user.module_profile='Supplier'
		user.send_welcome_email=0
		user.save(ignore_permissions=True)
		if not frappe.db.exists("User Permission",{'user':user_id,'allow':'Supplier','for_value':name}):
			usr_per=frappe.new_doc("User Permission")
			usr_per.user=user_id
			usr_per.allow='Supplier'
			usr_per.for_value=name
			usr_per.save(ignore_permissions=True)
		import string
		import random
		all_characters = string.ascii_letters + string.digits
		length = 6
		password = ''.join(random.choices(all_characters, k=length))
		if password:
			from frappe.utils.password import update_password

			update_password(user=user.name, pwd=password)

#Get Supplier Contact details to trigger mail from RFQ
@frappe.whitelist()
def get_supplier_contact(supplier):
	email_id=frappe.db.get_value("Supplier",{'name':supplier},['custom_supplier_login_id'])
	# email_id=frappe.db.get_value("Supplier",{'name':supplier},['email_id'])
	return email_id

	
@frappe.whitelist()
def mail_for_supplier_quotation(doc, method):
		if doc.items:
			request_quotation = doc.items[0].request_for_quotation
			
			owner = frappe.db.get_value("Request for Quotation", request_quotation, "owner")
	
			if owner !='Administrator':
				subject = f"Supplier Quotation - {doc.name}"
				message = f"""
				Dear Sir/Mam,<br><br>
				Supplier Quotation - {doc.name} aganist Request for Quotation - {request_quotation} has been submmitted successfully.
				<br><br>
				<i>This email has been automatically generated. Please do not reply</i>
				"""
				frappe.sendmail(
					recipients = [owner],
					subject = subject,
					message = message
				)

@frappe.whitelist()
def update_supplier_status(doc,method):
	supplier_qtn=frappe.db.get_value("Purchase Order Item",{"parent":doc.name},['supplier_quotation'])
	if supplier_qtn:
		frappe.db.set_value("Supplier Quotation",supplier_qtn,'custom_po_status','Converted to PO')

@frappe.whitelist()
def update_supplier_status_on_cancel(doc,method):
	supplier_qtn=frappe.db.get_value("Purchase Order Item",{"parent":doc.name},['supplier_quotation'])
	if supplier_qtn:
		frappe.db.set_value("Supplier Quotation",supplier_qtn,'custom_po_status','PO Cancelled')

@frappe.whitelist()
def update_po_status(doc,method):
	frappe.db.set_value("Supplier Quotation",doc.name,'custom_po_status','Pending for PO')
	
@frappe.whitelist()
def validate_remarks(doc, method):
	if doc.custom_cancellation_remarks and doc.custom_cancellation_remarks.strip():
		return doc.custom_cancellation_remarks.isalnum()
	else:
		frappe.throw("Field <b>Cancellation Remarks</b> is mandatory")
	
@frappe.whitelist()
def update_po_remarks(name, remark):
	frappe.db.set_value("Purchase Order", name, "custom_cancellation_remarks", remark)
	frappe.db.set_value("Purchase Order", name, "workflow_state", "Cancelled")
	doc = frappe.get_doc("Purchase Order", name)
	doc.cancel()
	
@frappe.whitelist()
def update_signature(user, docname, field):
	if frappe.db.exists("Employee", {"user_id": user}):
		signature = frappe.db.get_value("Employee", {"user_id": user}, ["custom_digital_signature"])
		if signature:
			frappe.db.set_value("Purchase Order", docname, field, signature)
		
@frappe.whitelist()
def trigger_mail_for_purchase_user(doc, method):
	pu_name = frappe.db.get_value("User", doc.owner, "full_name")
	subject = f"PO {doc.name} has been Approved - Reg"
	
	message = f"""
					<div style="font-family: Arial, sans-serif;
						border: solid 1px silver;
						border-radius: 10px;
						padding-top: 50px;
						padding-bottom: 50px;
						padding-right: 10px;
						padding-left: 10px;
						padding-left: 20px;">
						
						<b>Dear {pu_name}
						</b>
						<p>Greetings !</p>
						<p>PO <b>{doc.name}</b> has been approved. Kindly check and share it to the Supplier</p>
						<a style="background-color: #3488ef;
						color: white;
						text-decoration: none;
						padding: 5px;
						border-radius: 5px;" href="https://shaher.teamproit.com/app/purchase-order/{doc.name}">Open Purchase Order</a>
						
					"""
	if doc.custom_project_managers_signature:
		message += f"""
				<p>with regards,</p>
				<img src="{doc.custom_project_managers_signature}" />
				</div>
				"""
	else:
		message += "</div>"
	frappe.sendmail(
					recipients = [doc.owner],
					subject = subject,
					message = message,
				)

@frappe.whitelist()
def trigger_mail_for_supplier(name):
	doc = frappe.get_doc("Purchase Order", name)
	# if frappe.db.exists("Supplier Quotation", {"supplier": doc.supplier}):
	# 	supplier_quotation = frappe.db.get_value("Supplier Quotation", {"supplier": doc.supplier}, "quotation_number")
	# else:
	# 	supplier_quotation = ""
	supplier = frappe.db.get_value("Supplier", doc.supplier, "custom_supplier_login_id")
	frappe.log_error
	message = f"""
			<div style="font-family: Arial, sans-serif;
						border: solid 1px silver;
						border-radius: 10px;
						padding-top: 50px;
						padding-bottom: 50px;
						padding-right: 10px;
						padding-left: 10px;
						padding-left: 20px;">
						
						<b>Dear {doc.supplier}</b>
						<p>Greetings from <b>{doc.company}</b> !</p>
						<p>Please find the attached Purchase Order</p>
			"""
	if supplier:
		subject = "Purchase Order - Reg"
		frappe.sendmail(
						recipients = [supplier],
						subject = subject,
						message = message,
						attachments = [frappe.attach_print("Purchase Order", name,file_name=name, print_format="Purchase Order")]
					)
		return "ok"
	else:
		frappe.throw("Couldn't find supplier email")
		

@frappe.whitelist()
def get_po_qty(doc, method):
	po = frappe.get_doc("Purchase Order", doc.custom_purchase_order, "items")
	for po_item in po.items:
		for pi_item in doc.items:
			if po_item.item_code == pi_item.item_code:
				pi_item.custom_ordered_quantity = po_item.qty
				pi_item.custom_balance_quantity = po_item.qty - pi_item.qty
	po.save(ignore_permissions=True)
	
	
#Get the below values and set it to onload of the Vehicle document
@frappe.whitelist()
def record(name):
	maintenance = frappe.db.exists("Vehicle Maintenance Check List",{'register_no':name})
	if maintenance:
		main = frappe.db.get_all("Vehicle Maintenance Check List",{'register_no':name},['complaint','employee_id','vehicle_handover_date','garage_name'])[0]

	accident = frappe.db.exists("Vehicle Accident Report",{'plate_no':name})
	if accident:
		acc = frappe.db.get_all("Vehicle Accident Report",{'plate_no':name},['name','emp_id','date_of_accident','remarks'])[0]

		return main,acc

@frappe.whitelist()
def child_set_value(doc, method):
	wo=''
	if doc.custom_sales_order:
		if frappe.db.exists("Sales Order Item", {"parent": doc.custom_sales_order}):
			wo = frappe.db.get_value("Sales Order Item", {"parent": doc.custom_sales_order}, "custom_work_order_number")
	for item in doc.items:
		item.required_quantity = item.qty
		current_qty = frappe.db.get_value("Bin", {"item_code": item.item_code, "warehouse": doc.set_warehouse}, "actual_qty") or 0
		item.current_quantity = current_qty
		item.balance_qty_to_order = item.required_quantity - item.current_quantity
		additional_qty = float(item.additional_qty) if item.additional_qty is not None else 0
		item.finaly_qty_to_ordered = max(item.balance_qty_to_order - additional_qty, 0)
		item.qty = item.finaly_qty_to_ordered
		if wo:
			item.custom_work_order_number = wo or ''
	# for item in doc.items:
	#     item.required_quantity = item.qty
	#     current_qty = frappe.db.get_value("Bin", {"item_code": item.item_code, "warehouse": doc.set_warehouse}, "actual_qty") or 0
	#     item.current_quantity = current_qty
	#     item.balance_qty_to_order = item.required_quantity - item.current_quantity 
	#     item.finaly_qty_to_ordered = max(item.balance_qty_to_order - item.additional_qty, 0)
	#     item.qty = item.finaly_qty_to_ordered

@frappe.whitelist()
def update_item_table(sup_name,name):
	sq_sows=frappe.get_all("SQ SOW",{'supplier_quotation':sup_name})
	supplier_quotation=frappe.get_doc('Supplier Quotation',sup_name)
	supplier_quotation.set('custom_item_table',[])
	for i in sq_sows:
		sq_sow=frappe.get_doc("SQ SOW",i.name)
		
		for sow in sq_sow.manpower_table:
			supplier_quotation.append("custom_item_table",{
				'item_code':sow.item_code,
				'item_name':sow.item_name,
				'description':sow.description,
				'qty':sow.qty,
				'rate':sow.rate,
				'amount':sow.amount,
				'sow':sq_sow.sow_name
			})
		for sow in sq_sow.materials_table:
			supplier_quotation.append("custom_item_table",{
				'item_code':sow.item_code,
				'item_name':sow.item_name,
				'description':sow.description,
				'qty':sow.qty,
				'rate':sow.rate,
				'amount':sow.amount,
				'sow':sq_sow.sow_name
			})
		for sq in supplier_quotation.items:
			if sq.item_code==sq_sow.sow_id:
				sq.amount=sq_sow.total_sq_sow_amount
				sq.rate=(sq_sow.total_sq_sow_amount)/float(sq_sow.qty)
	supplier_quotation.save(ignore_permissions=True)

@frappe.whitelist
def update_item_table_without_amount(sup_name,name):
	sq_sows=frappe.get_all("SQ SOW",{'supplier_quotation':sup_name})
	supplier_quotation=frappe.get_doc('Supplier Quotation',sup_name)
	supplier_quotation.set('custom_item_table',[])
	for i in sq_sows:
		sq_sow=frappe.get_doc("SQ SOW",i.name)
		
		for sow in sq_sow.manpower_table:
			supplier_quotation.append("custom_item_table",{
				'item_code':sow.item_code,
				'item_name':sow.item_name,
				'description':sow.description,
				'qty':sow.qty,
				'rate':sow.rate,
				'amount':sow.amount,
				'sow':sq_sow.sow_name
			})
		for sow in sq_sow.materials_table:
			supplier_quotation.append("custom_item_table",{
				'item_code':sow.item_code,
				'item_name':sow.item_name,
				'description':sow.description,
				'qty':sow.qty,
				'rate':sow.rate,
				'amount':sow.amount,
				'sow':sq_sow.sow_name
			})
	supplier_quotation.save(ignore_permissions=True)

@frappe.whitelist()
def create_user_permission_on_validate(doc,method):
	if frappe.db.exists("User",{'name':doc.custom_supplier_login_id,'enabled':1}):
		user=frappe.get_doc("User",{'name':doc.custom_supplier_login_id,'enabled':1})
		user.append("roles",{
			"role":"Supplier"
		})
		user.module_profile='Supplier'
		user.save(ignore_permissions=True)
		if not frappe.db.exists("User Permission",{'user':doc.custom_supplier_login_id,'allow':'Supplier','for_value':doc.name}):
			usr_per=frappe.new_doc("User Permission")
			usr_per.user=doc.custom_supplier_login_id
			usr_per.allow='Supplier'
			usr_per.for_value=doc.name
			usr_per.save(ignore_permissions=True)
		import string
		import random
		all_characters = string.ascii_letters + string.digits
		length = 6
		password = ''.join(random.choices(all_characters, k=length))
		if password:
			from frappe.utils.password import update_password

			update_password(user=user.name, pwd=password)
	else:
		user=frappe.new_doc("User")
		user.email=doc.custom_supplier_login_id
		user.first_name=doc.supplier_name
		user.append("roles",{
			"role":"Supplier"
		})
		user.module_profile='Supplier'
		user.send_welcome_email=0
		user.save(ignore_permissions=True)
		if not frappe.db.exists("User Permission",{'user':doc.custom_supplier_login_id,'allow':'Supplier','for_value':doc.name}):
			usr_per=frappe.new_doc("User Permission")
			usr_per.user=doc.custom_supplier_login_id
			usr_per.allow='Supplier'
			usr_per.for_value=doc.name
			usr_per.save(ignore_permissions=True)
		import string
		import random
		all_characters = string.ascii_letters + string.digits
		length = 6
		password = ''.join(random.choices(all_characters, k=length))
		if password:
			from frappe.utils.password import update_password

			update_password(user=user.name, pwd=password)

@frappe.whitelist()
def monthly_expiry_doc():   
	current_date = nowdate()
	next_date = add_days(current_date, 30)
	docs = frappe.get_all("Legal Compliance Monitor",
						  {'next_due': ('between', (current_date, next_date))},
						  ['name','days_left','next_due'])
   

	recipients_docs_map = {}  # This dictionary will map recipients to the documents

	for i in docs:
		doc = frappe.get_doc("Legal Compliance Monitor", i.name)
		# For each recipient, append the document information
		for user in doc.alert_mails:
			recipient = user.user
			if recipient not in recipients_docs_map:
				recipients_docs_map[recipient] = []  # Initialize if not present
			recipients_docs_map[recipient].append(i)

	# Now, send an email for each recipient with their corresponding documents
	for recipient, recipient_docs in recipients_docs_map.items():
		# Create the document list table for this recipient
		documents = '''
		<table class="table table-bordered" border=1 style="border-width:2px; border-color:#000;">
			<tr>
				<td colspan="8" style=text-align:center><b>Legal Compliance Monitor List</b></td>
			</tr>
			<tr>
				<td colspan="2"><b>Document Name</b></td>
				<td colspan="2"><b>Expiry Date</b></td>
				<td colspan="2"><b>Days Left</b></td>
			</tr>
		'''
		
		for doc_info in recipient_docs:
			documents += '''
			<tr>
				<td colspan="2">{name}</td>
				<td colspan="2">{next_due}</td>
				<td colspan="2">{days_left}</td>
			</tr>
			'''.format(name=doc_info.name,  
					   next_due=doc_info.next_due, 
					   days_left=doc_info.days_left)
		
		documents += '</table>'

		# Send the email to this recipient
		frappe.sendmail(
			recipients=[recipient],
			subject="Legal Compliance Monitor Expiry Alert",
			message=f"""
				Dear Sir/Mam,<br><br>
				Kindly find the attached Legal Compliance Monitor List for Expiry Soon.<br><br>
				{documents}
				<br><br>
				Regards,<br>
				Your Company
			"""
		)
	
	return True
		
@frappe.whitelist()
def create_scheduled_job():
	pos = frappe.db.exists('Scheduled Job Type', 'monthly_expiry_doc')
	if not pos:
		sjt = frappe.new_doc("Scheduled Job Type")
		sjt.update({
			"method": 'shaher.custom.monthly_expiry_doc',
			"frequency": 'Cron',
			"cron_format": '0 2 * * *'
		})
		sjt.save(ignore_permissions=True)

@frappe.whitelist()
def update_days_left():
	value = frappe.get_all("Legal Compliance Monitor",["next_due","name"])
	for i in value:
		if i.next_due:
			diff = date_diff(i.next_due, today())
			frappe.db.set_value("Legal Compliance Monitor",i.name,"days_left",diff)
			next_due_date = frappe.utils.getdate(i.next_due)
			current_date = frappe.utils.getdate(today())
			next_due_month = next_due_date.month
			next_due_year = next_due_date.year
			current_month = current_date.month
			current_year = current_date.year
			if next_due_month == current_month and next_due_year == current_year and diff>=0:
				frappe.db.set_value("Legal Compliance Monitor", i.name, "status", "Expiring")
				frappe.db.set_value("Legal Compliance Monitor", i.name, "today_status", "Expiring")
			elif diff < 0:
				frappe.db.set_value("Legal Compliance Monitor", i.name, "status", "Expired")
				frappe.db.set_value("Legal Compliance Monitor", i.name, "today_status", "Expired")
			else:
				frappe.db.set_value("Legal Compliance Monitor", i.name, "status", "Active")
				frappe.db.set_value("Legal Compliance Monitor", i.name, "today_status", "Active")

@frappe.whitelist()
def update_days_left_daily():
	job = frappe.db.exists('Scheduled Job Type', 'update_days_left')
	if not job:
		emc = frappe.new_doc("Scheduled Job Type")
		emc.update({
			"method": 'shaher.custom.update_days_left',
			"frequency": 'Cron',
			"cron_format": '00 00 * * *'
		})
		emc.save(ignore_permissions=True)

@frappe.whitelist()
def get_gratuity(employee):
	from datetime import datetime
	from dateutil import relativedelta
	date_2 = datetime.now()
	doj = frappe.db.get_value('Employee',employee,'date_of_joining')
	absent_days = 0
	absent_days += frappe.db.get_value("Employee",{"name":employee},['custom_absent_days'])
		
	attendance = frappe.get_all(
		"Attendance",
			filters={
				"employee": employee,
				"attendance_date": ["between", (doj, nowdate())],
				"docstatus": ["=", 1],
				"leave_application":'' 
			},
			fields=["status"]
	)
	for i in attendance:
		if i.status =="Absent":
			absent_days +=1
		if i.status =="Half Day":
			absent_days+=0.5
	
	diff = relativedelta.relativedelta(date_2, doj)
	yos = cstr(diff.years) + ' years, ' + cstr(diff.months) +' months and ' + cstr(diff.days) + ' days'

	basic_salary = frappe.db.get_value('Employee',employee,'custom_basic')
	current_yoe_days = date_diff(nowdate(),doj) + 1
	current_yoe = round((current_yoe_days / 365),3)

	if(1 <= diff.years <= 3):
		gratuity_per_year = (basic_salary * .5)
		total_gratuity = math.ceil(gratuity_per_year/365*(current_yoe_days-absent_days))
		return total_gratuity
	elif(diff.years > 3):
		gratuity_per_year = basic_salary
		total_gratuity = math.ceil(gratuity_per_year/365*(current_yoe_days-absent_days))
		return total_gratuity
		
@frappe.whitelist()
def calculate_rejoining_date(to_date):
	return add_days(to_date,1)

@frappe.whitelist()
def validate_next_due_date(doc,method):
	# doc = frappe.get_doc("Leave Application",'HR-LAP-2025-00001')
	if doc.leave_type=='Annual Leave' and doc.custom_is_extension == 0:
		days,doj = frappe.db.get_value("Employee",{'name':doc.employee},['custom_annual_leave_applicable_after','date_of_joining'])
		if days:
			if frappe.db.exists("Leave Application",{'employee':doc.employee,'leave_type':'Annual Leave','docstatus':('!=',2)}):
				leave_app = frappe.get_doc("Leave Application",{'employee':doc.employee,'leave_type':'Annual Leave','docstatus':('!=',2)},order_by='creation DESC')
				if frappe.db.exists("Leave Application",{'employee':doc.employee,'leave_type':'Annual Leave','docstatus':('!=',2),'custom_is_extension':1,'from_date':('>',(add_days(leave_app.to_date,1)))}):
					leave_app_extn = frappe.get_doc("Leave Application",{'employee':doc.employee,'leave_type':'Annual Leave','docstatus':('!=',2),'custom_is_extension':1,'from_date':('>',(add_days(leave_app.to_date,1)))},order_by='creation DESC')
					end_date = leave_app_extn.to_date
				else:
					end_date = leave_app.to_date
				next_due_date = add_days(end_date,int(days))
				current_due_date = date_diff(doc.from_date,end_date) + 1
				print(current_due_date)
				if int(days) > current_due_date:
					frappe.throw(f"You can apply Annual Leave only after Next Due Date: {next_due_date}")
			else:
				next_due_date = add_days(doj,int(days))
				current_due_date = date_diff(today(),doj) + 1
				if int(days) > current_due_date:
					frappe.throw(f"You can apply Annual Leave after the Due Date: {next_due_date}")
		else:
			frappe.throw("Annual Leave Applicable after Days is not updated in Employee MIS.Kindly update that and check")


@frappe.whitelist()
def email_salary_slip(from_date):
	ss = frappe.get_all("Salary Slip",{'start_date':from_date,'docstatus':1},['employee','name'])
	for s in ss:
		doc = frappe.get_doc("Salary Slip",s['name'])
		receiver = frappe.db.get_value("Employee", doc.employee, "user_id")
		if not receiver:
			receiver = frappe.db.get_value("Employee", doc.employee, "company_email")
		message = f"Dear {doc.employee_name},<br><br> Kindly check your payslip for the period {doc.start_date.strftime('%d-%m-%Y')} and {doc.end_date.strftime('%d-%m-%Y')}."

		if receiver:
			email_args = {
				"recipients":receiver,
				"message": _(message),
				"subject": 'Salary Slip - from {0} to {1}'.format(doc.start_date, doc.end_date),
				"attachments": [frappe.attach_print("Salary Slip", doc.name,
					file_name="Pay Slip", print_format="Pay Slip New")],
				"reference_doctype": doc.doctype,
				"reference_name": doc.name
				}
			if not frappe.flags.in_test:
				print('yes')
				enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
			else:
				print('No')
				frappe.sendmail(**email_args)
		else:
			print(_("{0}: Employee email not found, hence email not sent").format(doc.employee_name))

@frappe.whitelist()
def ot_calculation(name):
	doc=frappe.get_doc("Attendance",name)
	# frappe.errprint("TEST")
	basic=frappe.db.get_value("Employee",{'name':doc.employee},['custom_basic'])
	if doc.custom_work_place:
		if doc.custom_work_place=='Office':
			wh=int(9)
		else:
			wh=int(10)
	if not basic:
		basic=0
	att=getdate(doc.attendance_date)
	year = att.year
	month = att.month
	total_days_in_month = calendar.monthrange(year, month)[1]
	hh=check_holiday(att,doc.employee)
	if hh:
		ot=2
	else:
		ot=1.5
	start=frappe.db.get_value("Shift Type",{'name':'G'},['start_time'])
	if isinstance(start, timedelta): 
		start = (datetime.min + start).time()
	start_date=datetime.combine(att,start)
	end=frappe.db.get_value("Shift Type",{'name':'G'},['end_time'])
	if isinstance(end, timedelta): 
		end = (datetime.min + end).time()
	end_date=datetime.combine(att,end)
	end_time = datetime.combine(att, time(19, 0, 0))
	in_time = get_datetime(doc.in_time) if doc.in_time else None
	out_time = get_datetime(doc.out_time) if doc.out_time else None
	if in_time and out_time:
		if in_time <= start_date and out_time>end_time:
			if basic>0:
				per_hour=basic/total_days_in_month/wh
				ot_amount=per_hour*float(ot)
				if hh:
					ot_hrs=time_diff_in_hours(out_time,end_date)
				else:
					ot_hrs=time_diff_in_hours(out_time,in_time)
				tot_ot=ot_amount*ot_hrs               
			else:
				ot_hrs=0
				tot_ot=0
		else:
			ot_hrs=0
			tot_ot=0
	else:
		ot_hrs=0
		tot_ot=0
	return ot_hrs,tot_ot

			
@frappe.whitelist()
def check_holiday(date,emp):
	holiday_list = frappe.db.get_value('Employee',emp,'holiday_list')
	holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
	left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
	if holiday:
		return 'H'
	
@frappe.whitelist()
def update_service_entry_number(docname,se_no, se_date):
	frappe.db.set_value("Delivery Note", docname, "service_entry_number", se_no)
	frappe.db.set_value("Delivery Note", docname, "custom_service_entry_date", se_date)
	return "done"

@frappe.whitelist()
def custom_round(value):
	integer_part = int(value)
	decimal_part = value - integer_part
	if decimal_part < 0.50:
		decimal_part = 0.00
	else:
		decimal_part = 0.50
	amount=integer_part + decimal_part
	amount=round(amount,2)
	return integer_part + decimal_part

# To update the DN's date in the SI's items table
@frappe.whitelist()
def udpate_date_of_supply(doc, method):
	for row in doc.items:
		if row.delivery_note:
			delivery_date = frappe.db.get_value("Delivery Note", row.delivery_note, "posting_date")
			service_entry = frappe.db.get_value("Delivery Note", row.delivery_note, "service_entry_number")
			row.custom_date_of_supply = delivery_date
			row.custom_service_entry_number = service_entry

import frappe

import frappe

def validate_purchase_invoice(doc, method):

	purchase_orders = list(set(d.purchase_order for d in doc.items if d.purchase_order))

	if not purchase_orders:
		return  

   
	sales_orders = frappe.get_all("Purchase Order Item",
								  filters={"parent": ["in", purchase_orders]},
								  fields=["sales_order"])

	sales_order_names = list(set(so.sales_order for so in sales_orders if so.sales_order))

	if not sales_order_names:
		return  

   
	sales_order_data = frappe.get_all("Sales Order",
									  filters={"name": ["in", sales_order_names], "docstatus": ["!=", 2]},
									  fields=["name", "grand_total", "per_delivered"])

	for so in sales_order_data:
	   
		if so.per_delivered < 100:
			frappe.throw(f"Cannot save Purchase Invoice: Sales Order {so.name} is not fully delivered.")

	   
		sales_invoices = frappe.get_all("Sales Invoice",
										filters={"sales_order": so.name, "docstatus": ["!=", 2]},
										fields=["name", "outstanding_amount", "grand_total"])

		for si in sales_invoices:
		   
			# if si.outstanding_amount > 0:
			#     frappe.throw(f"Cannot save Purchase Invoice: Sales Invoice {si.name} is not fully paid.")

			
			payment_total = frappe.db.sql("""
				SELECT SUM(per.allocated_amount) FROM `tabPayment Entry Reference` per
				JOIN `tabPayment Entry` pe ON per.parent = pe.name
				WHERE per.reference_doctype = 'Sales Invoice' AND per.reference_name = %s
				AND pe.docstatus = 1
			""", (si.name,))[0][0] or 0  

		   
			if payment_total != si.grand_total:
				frappe.throw(f"Cannot save Purchase Invoice: Payment Entry total ({payment_total}) "
							 f"does not match Sales Invoice Grand Total ({si.grand_total}) for {si.name}.")


@frappe.whitelist()
def get_project_items(doctype, txt, searchfield, start, page_len, filters):
	project = filters.get("project") if filters else None
	if project:
		doc = frappe.get_doc("Project", project)
		return [(row.item_code,) for row in doc.custom_items]
	
@frappe.whitelist()
def get_qty_rate(item_code, project):
	qty = frappe.db.get_value("Project Item Table", {"item_code": item_code, "parent": project}, "qty")
	rate = frappe.db.get_value("Project Item Table", {"item_code": item_code, "parent": project}, "rate")
	return qty, rate
		
@frappe.whitelist()
def update_employee_certification(doc, method):
	if doc.custom_employee_certification:
		ec = frappe.get_doc("Employee Certification", doc.custom_employee_certification)
		ec.purchase_order = doc.name
		ec.save(ignore_permissions=True)
		
@frappe.whitelist()
def create_vehicle_maintenance_check(doc, methods):
	if doc.custom_division == "Vehicle":
		for row in doc.items:
			vmc = frappe.new_doc("Vehicle Maintenance Check List")
			vmc.register_no = row.custom_vehicle
			vmc.supplier = doc.supplier
			vmc.actual_expense = row.base_net_amount
			vmc.vehicle_service = row.item_code
			vmc.work_finished_date = row.schedule_date
			vmc.present_kilometer = row.custom_present_kilometer
			vmc.purchase_order = doc.name
			vmc.save(ignore_permissions=True)
			row.custom_vehicle_maintenance_check = vmc.name
		frappe.msgprint("Vehicle Maintenance Check List created successfully.")
		
@frappe.whitelist()
def remove_vmc_linked(doc, mthod):
	if doc.custom_division == "Vehicle":
		for row in doc.items:
			if row.custom_vehicle_maintenance_check:
				row.custom_vehicle_maintenance_check = ""
			if row.custom_vehicle:
				row.custom_vehicle = ""
		
@frappe.whitelist()
def cancel_vehicle_maintenance_check(doc, methods):
	if doc.custom_division == "Vehicle":
		if frappe.db.exists("Vehicle Maintenance Check List", {"purchase_order": doc.name, "docstatus": 1}):
			vmcs = frappe.get_all("Vehicle Maintenance Check List", {"purchase_order": doc.name, "docstatus": 1}, "name")
			for i in vmcs:
				vmc = frappe.get_doc("Vehicle Maintenance Check List", i.name)
				if vmc.docstatus == 1:
					vmc.cancel(ignore_permissions=True)
				if vmc.docstatus == 0:
					vmc.delete(ignore_permissions=True)
				
@frappe.whitelist()
def validate_kilometer(doc, methods):
	if doc.custom_division == "Vehicle":
		for row in doc.items:
			if row.custom_present_kilometer and row.custom_last_kilometer:
				if row.custom_present_kilometer < row.custom_last_kilometer:
					frappe.throw("<b>Present Kilometer</b> should be greater than the <b>Last Kilometer</b>")
					
@frappe.whitelist()
def pdo_validation(doc, methods):
	# Check Service Entry
	if doc.custom_division == "PDO":
		idx = 0
		for row in doc.items:
			idx+=1
			if not row.custom_service_entry_number:
				frappe.errprint("true")
				frappe.throw(
					f"<b>Row {idx}</b>: Service Entry Number is not found for the Item {row.item_code}", 
					title="Service Entry Not Found"
				)
			
@frappe.whitelist()
def validate_grand_total(so,date,total):
	grand_total=frappe.db.get_value("Sales Order",so,'base_grand_total')
	qtn=frappe.db.get_value("Sales Order",so,'quotation')
	profit_per=frappe.db.get_value("Quotation",qtn,'custom_prof_percentage')
	purchase_orders=frappe.get_all("Purchase Order",{'custom_sales_order':so,'docstatus':1,'transaction_date':('<=',date)},['base_grand_total'])
	total_base_grand_total = sum(po['base_grand_total'] for po in purchase_orders) + float(total)
	percentage_difference = ((total_base_grand_total - (grand_total*((100-profit_per)/100))) / (grand_total*((100-profit_per)/100))) * 100
	if total_base_grand_total > (grand_total*((100-profit_per)/100)):
		return "above",round(percentage_difference,2)
	if total_base_grand_total < (grand_total*((100-profit_per)/100)):
		return "below",round(abs(percentage_difference),2)
	if total_base_grand_total == (grand_total*((100-profit_per)/100)):
		return 'equals',0

@frappe.whitelist()
def validate_grand_total_qtn(supp_qtn,total,profit_per):
	total_base_grand_total=frappe.db.get_value("Supplier Quotation",supp_qtn,'base_grand_total')
	threshold = float(total) * ((100 - float(profit_per)) / 100)

	# Calculate percentage difference
	percentage_difference = ((total_base_grand_total - threshold) / threshold) * 100

	if total_base_grand_total > threshold:
		return "above", round(percentage_difference,2)
	
@frappe.whitelist()
def update_coc_fields(doc, methods):
	if doc.custom_division == "PDO" and len(doc.items) > 0:
		first_row = doc.items[0]  # Get the first row
		so = first_row.against_sales_order
		wo = first_row.custom_work_order_number
		# start_date, po_value = frappe.db.get_value("Sales Order", so, ["transaction_date", "grand_total"])
		start_date = frappe.db.get_value("Sales Order", so, ["transaction_date"])
		end_date = doc.custom_approval_date
		# doc.custom_purchase_order_value = po_value if po_value else ''
		doc.custom_work_start_date = start_date if start_date else ''
		doc.custom_work_finish_date = end_date
		doc.custom_purchase_order_no = doc.po_no
		doc.custom_actual_work_carried_out_ = doc.grand_total
		doc.custom_work_order_no = wo
	
@frappe.whitelist()
def get_user_details(user):
	employee_sign = frappe.db.get_value("Employee",{'name':user},['custom_digital_signature'])
	if employee_sign:
		return "https://shaher.teamproit.com/"+employee_sign

# @frappe.whitelist()
# def rejection_remark(name, remark):
# 	frappe.db.set_value("Salary Certificate", name, "rejection_remark", remark)
# 	doc = frappe.get_doc("Salary Certificate", name)
# 	doc.save()
# 	frappe.db.set_value("Salary Certificate", name, "workflow_state", "Rejected")

@frappe.whitelist()
def update_approval_date_mr(doc,method):
	if(doc.workflow_state == "Approved"):
		frappe.db.set_value("Material Request",doc.name,"custom_approval_date",today())

@frappe.whitelist()
def update_approval_date_po(doc,method):
	if(doc.workflow_state == "Approved"):
		frappe.db.set_value("Purchase Order",doc.name,"custom_approval_date",today())

@frappe.whitelist()
def update_approval_date_pi(doc,method):
	frappe.db.set_value("Purchase Invoice",doc.name,"custom_approval_date",today())

@frappe.whitelist()
def update_approval_date_pr(doc,method):
	frappe.db.set_value("Purchase Receipt",doc.name,"custom_approval_date",today())

@frappe.whitelist()
def make_quotation(source_name, target_doc=None):
    def postprocess(source, target):
        # Map 'Provisional Budgeting Child Expense' manually since get_mapped_doc doesn't support multiple child tables
        for expense in source.get("expenses"):
            target.append("expenses", {
                "account": expense.account,
                "current_value": expense.current_value,
                "provisional_value": expense.provisional_value
            })

    doclist = get_mapped_doc("Provisional Budgeting", source_name, {
        "Provisional Budgeting": {
            "doctype": "Provisional Budgeting Comparison",
            "field_map": {
                "name": "provisional_budgeting",
            }
        },
        "Provisional Budgeting Child": {
            "doctype": "Provisional Budgeting Comparison Child",
            "field_map": {
                "account": "account",
                "current_value": "current_value",
                "provisional_value": "provisional_value",
            }
        }
    }, target_doc, postprocess)

    return doclist

@frappe.whitelist()
def check_inactive_employee(employee):
	
	status = frappe.db.get_value("Employee", {"employee": employee}, ["status"])
	
	if status == "Active":
		return "Active"
	else:
		return "Inactive"