app_name = "shaher"
app_title = "Shaher"
app_publisher = "gifty.p@groupteampro.com"
app_description = "Shaher"
app_email = "it.support@groupteampro.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "shaher",
# 		"logo": "/assets/shaher/logo.png",
# 		"title": "Shaher",
# 		"route": "/shaher",
# 		"has_permission": "shaher.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/shaher/css/shaher.css"
# app_include_js = "/assets/shaher/js/shaher.js"

# include js, css files in header of web template
web_include_css = "/assets/shaher/css/shaher.css"
# web_include_js = "/assets/shaher/js/shaher.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "shaher/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "shaher/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "shaher.utils.jinja_methods",
# 	"filters": "shaher.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "shaher.install.before_install"
# after_install = "shaher.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "shaher.uninstall.before_uninstall"
# after_uninstall = "shaher.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "shaher.utils.before_app_install"
# after_app_install = "shaher.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "shaher.utils.before_app_uninstall"
# after_app_uninstall = "shaher.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "shaher.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	# "ToDo": "custom_app.overrides.CustomToDo"
    "Payroll Entry":"shaher.shaher.overrides.CustomPayrollEntry",
    "Salary Slip":"shaher.shaher.overrides.CustomSalarySlip",
    
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Supplier Quotation": {
		"on_submit": ["shaher.custom.mail_for_supplier_quotation","shaher.custom.update_po_status"]
	},
    "Purchase Invoice":{
        "on_submit":"shaher.custom.update_approval_date_pi"
	},
	"Purchase Order":{
		"after_insert": "shaher.custom.update_employee_certification",
		"on_submit":["shaher.custom.update_supplier_status",
               "shaher.custom.trigger_mail_for_purchase_user",
               "shaher.custom.create_vehicle_maintenance_check",
			   "shaher.custom.update_approval_date_po"
               ],
		"before_cancel": ["shaher.custom.remove_vmc_linked"],
		"on_cancel":["shaher.custom.update_supplier_status_on_cancel", "shaher.custom.validate_remarks", "shaher.custom.cancel_vehicle_maintenance_check"],
	},
	"Purchase Receipt": {
		"after_insert": "shaher.custom.get_po_qty",
		"on_submit":"shaher.custom.update_approval_date_pr"
	},
	"Material Request": {
		"validate": ["shaher.custom.child_set_value", "shaher.custom.validate_kilometer",],
        "on_submit":"shaher.custom.update_approval_date_mr"
	},
	"Supplier":{
		"after_insert":"shaher.custom.create_user_permission_on_validate"
	},
	"Leave Application":{
		'validate':"shaher.custom.validate_next_due_date"
	},
    # "Attendance":{
		# 'on_update':"shaher.custom.ot_calculation",
    #     'after_insert':"shaher.custom.ot_calculation",
	# },
    "Sales Invoice":{
		'validate':[ "shaher.custom.udpate_date_of_supply","shaher.custom.pdo_validation",],
	},
    "Delivery Note": {
		'validate': "shaher.custom.update_coc_fields"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"shaher.tasks.all"
# 	],
	"cron": {
		"0 2 * * * *": [
			"shaher.shaher.doctype.employee_certification.employee_certification.monthly_expiry_doc"
		],
	},
	"daily": [
		"shaher.alerts.update_employee_certification_status"
		"shaher.shaher.doctype.employee_certification.employee_certification.update_days_left"
# 		"shaher.tasks.daily"
		"shaher.custom.create_scheduled_job",
        "shaher.custom.update_days_left_daily",
	],
# 	"hourly": [
# 		"shaher.tasks.hourly"
# 	],
# 	"weekly": [
# 		"shaher.tasks.weekly"
# 	],
# 	"monthly": [
# 		"shaher.tasks.monthly"
# 	],
}

# Testing
# -------

# before_tests = "shaher.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "shaher.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "shaher.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["shaher.utils.before_request"]
# after_request = ["shaher.utils.after_request"]

# Job Events
# ----------
# before_job = ["shaher.utils.before_job"]
# after_job = ["shaher.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"shaher.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

