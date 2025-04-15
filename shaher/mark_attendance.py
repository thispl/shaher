import frappe
import frappe
from frappe import _
from frappe.utils import date_diff, today, add_days, nowdate
from frappe import _
import math
from frappe.utils.background_jobs import enqueue
from datetime import datetime, time, timedelta
from frappe.utils import cint, flt, formatdate, get_link_to_form, getdate, now
from frappe.utils import getdate, get_datetime
from frappe.utils import time_diff_in_hours
import calendar


def get_dates(from_date,to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates

# @frappe.whitelist()
# def mark_att():
#     from_date = add_days(today(),-1)  
#     to_date = today()
#     dates = get_dates(from_date,to_date)
#     mark_absent(from_date,to_date)
#     ot_calculation(from_date,to_date)

@frappe.whitelist()
def mark_att_enqueue(from_date, to_date):
    frappe.enqueue(
        "shaher.mark_attendance.mark_att",
        queue="long",
        timeout=36000,
        is_async=True,
        now=False,
        job_name="Mark Attendance",
        from_date=from_date,
        to_date=to_date
    )
    return "ok"

@frappe.whitelist()
def mark_att(from_date, to_date):
    checkins = frappe.db.sql(
        """
        SELECT * 
        FROM `tabEmployee Checkin` 
        WHERE skip_auto_attendance = 0 
        AND date(time) BETWEEN '%s' AND '%s' 
        order by time 
        """ %(from_date, to_date), as_dict=True)
    
    for c in checkins:
        employee = frappe.db.exists('Employee',
                                    {'status': 'Active', 'date_of_joining': ['<=', from_date], 'name': c.employee})
        if employee:
            mark_attendance_from_checkin(c.name, c.employee, c.time)
    mark_absent(from_date, to_date)
    # ot_calculation(from_date, to_date)
    calculate_ot_and_wh(from_date, to_date)
    ot_calculation_without_emp(from_date, to_date)
    return "ok"

@frappe.whitelist()
def mark_att_with_employee_enqueue(from_date, to_date, employee):
    frappe.enqueue(
        "shaher.mark_attendance.mark_att_with_employee",
        queue="long",
        timeout=36000,
        is_async=True,
        now=False,
        job_name="Mark Attendance",
        from_date=from_date,
        to_date=to_date,
        employee=employee
    )
    return "ok"


@frappe.whitelist()
def mark_att_with_employee(from_date, to_date, employee):
    checkins = frappe.db.sql(
        """
        SELECT * 
        FROM `tabEmployee Checkin` 
        WHERE date(time) BETWEEN '%s' AND '%s' 
        AND employee ='%s' 
        order by time 
        """ %(from_date, to_date, employee), as_dict=True)

    for c in checkins:
        employee = frappe.db.exists('Employee',
                                        {'status': 'Active', 'date_of_joining': ['<=', from_date], 'name': c.employee})
        if employee:
            mark_attendance_from_checkin(c.name, c.employee, c.time)
    
    mark_absent_with_employee(from_date, to_date, employee)
    # ot_calculation_with_employee(from_date, to_date, employee)
    calculate_ot_and_wh_with_employee(from_date, to_date, employee)
    ot_calculation_emp(from_date, to_date, employee)
    return "ok"

@frappe.whitelist()    
def mark_absent(from_date, to_date):
    dates = get_dates(from_date, to_date)
    for date in dates:
        employee = frappe.db.get_all('Employee',
                                    {'status': 'Active', 'date_of_joining': ['<=', from_date]},
                                    ['*'])
        for emp in employee:
            hh = check_holiday(date,emp.name)
            if not hh:
                if not frappe.db.exists('Attendance',
                                        {'attendance_date': date, 'employee': emp.name, 'docstatus': ('!=', '2')}):
                    att = frappe.new_doc('Attendance')
                    att.employee = emp.name
                    att.status = 'Absent'
                    att.custom_work_place='Office'
                    att.attendance_date = date
                    att.save(ignore_permissions=True)
                    frappe.db.commit()

@frappe.whitelist()    
def mark_absent_with_employee(from_date, to_date, employee):
    dates = get_dates(from_date,to_date)
    for date in dates:
        employee_data = frappe.db.get_all('Employee',
                                          {'employee':employee, 'status':'Active', 'date_of_joining':['<=',from_date]},
                                          ['*'])
        for emp in employee_data:
            hh = check_holiday(date,emp.name)
            if not hh:
                if not frappe.db.exists('Attendance',
                                        {'attendance_date': date, 'employee': emp.name, 'docstatus': ('!=', '2')}):
                    att = frappe.new_doc('Attendance')
                    att.employee = emp.name
                    att.status = 'Absent'
                    att.custom_work_place='Office'
                    att.attendance_date = date
                    att.save(ignore_permissions=True)
                    frappe.db.commit() 

@frappe.whitelist()
def ot_calculation(from_date,to_date):
    att=frappe.db.get_all("Attendance",{'attendance_date':('between',(from_date,to_date)),'docstatus':0},['name'])
    for a in att:
        doc=frappe.get_doc('Attendance',a.name)
        att=getdate(doc.attendance_date)
        hh=check_holiday(att,doc.employee)
        if hh:
            ot=2
        else:
            ot=1.5
        start=frappe.db.get_value("Shift Type",{'name':'G'},['start_time'])
        if isinstance(start, timedelta): 
            start = (datetime.min + start).time()
        start_date=datetime.combine(att,start)
        end_time = datetime.combine(att, time(19, 0, 0))
        in_time = get_datetime(doc.in_time) if doc.in_time else None
        out_time = get_datetime(doc.out_time) if doc.out_time else None
        if in_time and out_time:
            if in_time <= start_date and out_time>end_time:
                doc.custom_overtime_hours=ot
                doc.save(ignore_permissions=True)

@frappe.whitelist()
def ot_calculation_with_employee(from_date, to_date, employee):
    att=frappe.db.get_all("Attendance",{'employee': employee, 'attendance_date':('between',(from_date,to_date)),'docstatus':0},['name'])
    for a in att:
        doc=frappe.get_doc('Attendance',a.name)
        att=getdate(doc.attendance_date)
        hh=check_holiday(att,doc.employee)
        if hh:
            ot=2
        else:
            ot=1.5
        start=frappe.db.get_value("Shift Type",{'name':'G'},['start_time'])
        if isinstance(start, timedelta): 
            start = (datetime.min + start).time()
        start_date=datetime.combine(att,start)
        end_time = datetime.combine(att, time(19, 0, 0))
        in_time = get_datetime(doc.in_time) if doc.in_time else None
        out_time = get_datetime(doc.out_time) if doc.out_time else None
        if in_time and out_time:
            if in_time <= start_date and out_time>end_time:
                doc.custom_overtime_hours=ot
                doc.save(ignore_permissions=True)

@frappe.whitelist()
def check_holiday(date,emp):
    holiday_list = frappe.db.get_value('Employee',emp,'holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
    if holiday:
        return 'H'

def mark_attendance_from_checkin(checkin, employee, time):
    att_date = time.date()
    in_time = ''
    out_time = ''
    checkins = frappe.db.sql("""
                            SELECT name, time, log_type 
                            FROM `tabEmployee Checkin`
                            WHERE employee = '%s' 
                            AND date(time) = '%s' order by time
                            """ %(employee, att_date), as_dict=True)
    
    if checkins:
        in_logs = [c["time"] for c in checkins if c["log_type"] == "IN"]
        out_logs = [c["time"] for c in checkins if c["log_type"] == "OUT"]
        if in_logs:
            in_time = in_logs[0]
        if out_logs:
            out_time = out_logs[-1]
        att = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date, 'docstatus': ["!=", 2]})
        if not att:
            att = frappe.new_doc("Attendance")
            att.employee = employee
            att.attendance_date = att_date
            att.shift = "G"
            att.status = "Absent"
            att.custom_work_place='Office'
            att.in_time = in_time
            att.out_time = out_time
            att.save()
            frappe.db.commit()
            frappe.db.set_value('Employee Checkin', checkin, 'skip_auto_attendance', '1')
            frappe.db.set_value('Employee Checkin', checkin, 'attendance', att.name)
            return att.name
        else:
            att_name = frappe.db.get_value('Attendance',{'employee':employee,'attendance_date':att_date, 'docstatus': 0},['name'])
            if frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date, 'docstatus': 0}):
                att = frappe.get_doc("Attendance",{'employee':employee,'attendance_date':att_date, 'docstatus': 0})
                att.employee = employee
                att.attendance_date = att_date
                att.shift = "G"
                att.custom_work_place='Office'
                att.in_time = in_time
                att.out_time = out_time
                att.save()
                frappe.db.commit()
                frappe.db.set_value('Employee Checkin', checkin, 'skip_auto_attendance', '1')
                frappe.db.set_value('Employee Checkin', checkin, 'attendance', att.name)


def calculate_ot_and_wh(from_date, to_date):
    
    attendance = frappe.db.get_all("Attendance",
        filters={'attendance_date': ["Between", [from_date, to_date]], "docstatus": 0},
        fields=["*"]
    )

    shift_wh = frappe.db.get_value("Shift Type", {"name": "G"}, ["custom_total_working_hours"])
    
    if shift_wh:
        total_wh = shift_wh.total_seconds() / 3600.0

    for att in attendance:
        if att.in_time and att.out_time and att.shift:
            wh = time_diff_in_hours(att.out_time, att.in_time)
            in_time = datetime.strptime(str(att.in_time), "%Y-%m-%d %H:%M:%S")
            out_time = datetime.strptime(str(att.out_time), "%Y-%m-%d %H:%M:%S")

            time_diff = out_time - in_time

            total_seconds = time_diff.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)

            total_working_hours = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

            if wh >= total_wh:
                status = "Present"
            elif wh >= (total_wh / 2):
                status = "Half Day"
            else:
                status = "Absent"

            att_doc = frappe.get_doc("Attendance", att.name)
            att_doc.working_hours = wh
            att_doc.custom_total_working_hours = total_working_hours
            att_doc.status = status
            att_doc.save()

    frappe.db.commit()


def calculate_ot_and_wh_with_employee(from_date, to_date, employee):
    
    attendance = frappe.db.get_all("Attendance", 
        filters={'attendance_date': ["Between", [from_date, to_date]], "employee": employee, "docstatus": 0},
        fields=["*"]
    )

    shift_wh = frappe.db.get_value("Shift Type", {"name": "G"}, ["custom_total_working_hours"])
    
    if shift_wh:
        total_wh = shift_wh.total_seconds() / 3600.0

    for att in attendance:
        if att.in_time and att.out_time and att.shift:
            wh = time_diff_in_hours(att.out_time, att.in_time)
            in_time = datetime.strptime(str(att.in_time), "%Y-%m-%d %H:%M:%S")
            out_time = datetime.strptime(str(att.out_time), "%Y-%m-%d %H:%M:%S")

            time_diff = out_time - in_time

            total_seconds = time_diff.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)

            total_working_hours = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

            if wh >= total_wh:
                status = "Present"
            elif wh >= (total_wh / 2):
                status = "Half Day"
            else:
                status = "Absent"

            att_doc = frappe.get_doc("Attendance", att.name)
            att_doc.working_hours = wh
            att_doc.custom_total_working_hours = total_working_hours
            att_doc.status = status
            att_doc.save()

    frappe.db.commit()


@frappe.whitelist()
def ot_calculation_without_emp(from_date,to_date):
    att=frappe.db.get_all("Attendance",{'docstatus':0,'attendance_date':('between',(from_date,to_date))},['employee','attendance_date','custom_work_place','in_time','out_time','name'])
    for a in att:
        doc=frappe.get_doc("Attendance",a.name)
        if doc.in_time and doc.out_time:
            basic=frappe.db.get_value("Employee",{'name':doc.employee},['custom_basic'])
            if doc.custom_work_place:
                if doc.custom_work_place=='Office':
                    wh=int(9)
                else:
                    wh=int(10)
            else:
                doc.custom_work_place='Office'
                wh=int(9)
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
                    if not hh:
                        ot_hrs=time_diff_in_hours(out_time,end_date)
                    else:
                        ot_hrs=time_diff_in_hours(out_time,in_time)
                    if basic>0:
                        per_hour=basic/total_days_in_month/wh
                        ot_amount=per_hour*float(ot)
                        tot_ot=ot_amount*ot_hrs               
                    else:
                        tot_ot=0
                else:
                    ot_hrs=0
                    tot_ot=0
            else:
                ot_hrs=0
                tot_ot=0
            doc.custom_overtime_hours=ot_hrs
            doc.custom_overtime_amount=tot_ot
        doc.save(ignore_permissions=True)
        if doc.status=='Present':
            doc.submit()
        frappe.db.commit()




@frappe.whitelist()
def ot_calculation_emp(from_date,to_date,employee):
    att=frappe.db.get_all("Attendance",{'docstatus':0,'attendance_date':('between',(from_date,to_date)),'employee':employee},['employee','attendance_date','custom_work_place','in_time','out_time','name'])
    for a in att:
        doc=frappe.get_doc("Attendance",a.name)
        if doc.in_time and doc.out_time and doc.custom_work_place:
            basic=frappe.db.get_value("Employee",{'name':doc.employee},['custom_basic'])
            if doc.custom_work_place:
                if doc.custom_work_place=='Office':
                    wh=int(9)
                else:
                    wh=int(10)
            else:
                doc.custom_work_place='Office'
                wh=int(9)
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
                    if not hh:
                        ot_hrs=time_diff_in_hours(out_time,end_date)
                    else:
                        ot_hrs=time_diff_in_hours(out_time,in_time)
                    if basic>0:
                        per_hour=basic/total_days_in_month/wh
                        ot_amount=per_hour*float(ot)
                        tot_ot=ot_amount*ot_hrs               
                    else:
                        tot_ot=0
                else:
                    ot_hrs=0
                    tot_ot=0
            else:
                ot_hrs=0
                tot_ot=0
            doc.custom_overtime_hours=ot_hrs
            doc.custom_overtime_amount=tot_ot
        doc.save(ignore_permissions=True)
        if doc.status=='Present':
            doc.submit()
        frappe.db.commit()

