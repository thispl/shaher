
import frappe
from datetime import time
from frappe.utils import now_datetime
from datetime import datetime, timedelta
from datetime import date
from frappe.permissions import has_permission

@frappe.whitelist()
def get_workspace_image_for_now():
    now = now_datetime().time()
    doc = frappe.get_doc("Workspace Settings", "Workspace Settings")

    for row in doc.workspace_settings:
        # Convert start_time and end_time from timedelta to time
        start = (datetime.min + row.start_time).time() if isinstance(row.start_time, timedelta) else row.start_time
        end = (datetime.min + row.end_time).time() if isinstance(row.end_time, timedelta) else row.end_time

        if start <= end:
            # Normal case: same day
            if start <= now <= end:
                return {
                    "image": row.image,
                    "description": row.description,
                    "event": row.event
                }
        else:
            # Overnight case: e.g. 20:00 to 05:00
            if now >= start or now <= end:
                return {
                    "image": row.image,
                    "description": row.description,
                    "event": row.event
                }

    return {}



@frappe.whitelist()
def get_today_birthdays():
    today = datetime.today()
    day = today.strftime("%d")
    month = today.strftime("%m")

    employees = frappe.db.sql(
        """
        SELECT name, employee_name, image, designation, department, date_of_birth, user_id
        FROM `tabEmployee`
        WHERE status = 'Active'
        AND DATE_FORMAT(date_of_birth, '%%m') = %s
        AND DATE_FORMAT(date_of_birth, '%%d') = %s
        ORDER BY employee_name ASC
        """,
        (month, day),
        as_dict=True
    )
    return employees




@frappe.whitelist()
def get_today_joiners():
    today = date.today().strftime('%Y-%m-%d')
    employees = frappe.db.sql("""
        SELECT name, employee_name, image, designation, department,user_id
        FROM `tabEmployee`
        WHERE status = 'Active' AND date_of_joining = %s
    """, (today,), as_dict=True)
    return employees



@frappe.whitelist()
def get_today_work_anniversaries():
    today = datetime.today()
    month_day = today.strftime("%m-%d")  

    employees = frappe.db.sql(
        """
        SELECT name, employee_name, image, designation, department, date_of_joining, user_id
        FROM `tabEmployee`
        WHERE status = 'Active'
        AND DATE_FORMAT(date_of_joining, '%%m-%%d') = %s
        AND DATEDIFF(CURDATE(), date_of_joining) >= 365
        ORDER BY employee_name ASC
        """,
        (month_day,),
        as_dict=True
    )
    return employees



@frappe.whitelist()
def get_announcements(user):
    today = frappe.utils.nowdate()
    notes = []

    announcements = frappe.db.get_all(
        'Announcements',
        filters={'expire_notification_on': ['>=', today]},
        fields=['title', 'content', 'expire_notification_on', 'name', 'creation'],
        order_by='modified desc'
    )

    for a in announcements:
        doc = frappe.get_doc('Announcements', a.name)
        seen_users = [row.user for row in doc.seen_by_table]

        if user not in seen_users:
            notes.append({
                "title": a.title,
                "content": a.content,
                "expire_notification_on": a.expire_notification_on,
                "name": a.name,
                "creation": a.creation
            })

    return notes

    
@frappe.whitelist()
def send_birthday_wish_email(user, recipients, subject, message):
    employee_name = frappe.db.get_value("Employee", user, "employee_name") or "Team Member"

    content = f"""
        <p>Dear {employee_name},</p>
        <p style="font-size:16px;">{message}</p>
        <p>🎉 Warm wishes from the <strong>Teampro</strong> Family!</p>
    """

    frappe.sendmail(
        recipients=[recipients],
        subject=subject,
        message=content
    )

    return "Sent"


@frappe.whitelist()
def mark_announcement_seen(announcement_name, user):
    doc = frappe.get_doc("Announcements", announcement_name)

    if not any(row.user == user for row in doc.seen_by_table):
        doc.append("seen_by_table", {"user": user})
        doc.save(ignore_permissions=True)
        frappe.db.commit()
import frappe

@frappe.whitelist()
def get_fav_documents(user):
    docs = frappe.get_all(
        'Favourite Doctypes',
        filters={'enabled': 1, 'add_to_favourite': 1},
        fields=['name', 'route', 'background_color', 'add_to_favourite', 'logo_color', 'icon','link_type','modules']
    )
    
    
    
    return docs

@frappe.whitelist()
def add_fav_documents(name):
    frappe.db.set_value('Favourite Doctypes', name, 'add_to_favourite', 1)
    frappe.db.commit()
    return {"status": "success", "name": name}

@frappe.whitelist()
def remove_fav_documents(name):
    frappe.db.set_value('Favourite Doctypes', name, 'add_to_favourite', 0)
    frappe.db.commit()
    return {"status": "success", "name": name}




@frappe.whitelist()
def get_all_doctypes(user):
    doctypes = frappe.get_all(
        'Favourite Doctypes',
        filters={'enabled': 1},
        fields=['name', 'route', 'background_color', 'add_to_favourite', 'logo_color', 'icon', 'link_type','modules'],
        order_by="modules"
    )

    allowed_docs = []

    for doc in doctypes:
        frappe.errprint(doc)
        frappe.errprint(user)
        if not doc.get("link_type"):
            continue

        # Special case: Employee
        if doc.link_type == "Employee":
            employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
            frappe.errprint(employee)
            if employee:
                frappe.errprint(employee)
                emp_doc = frappe.get_doc("Employee", employee)
                if frappe.has_permission("Employee", emp_doc, "read", user=user):
                    allowed_docs.append(doc)
            continue

        # General case
        if frappe.has_permission(doc.name, user=user, ptype="read"):
            allowed_docs.append(doc)

    return allowed_docs
