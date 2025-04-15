# Copyright (c) 2025, gifty.p@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _



def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = []
	columns += [
	_("ID") + ":Link/First Aid:150",
	_("Employee ID") + ":Link/Employee:180",
	_("Employee Name") + ":Data:200",
	_("Department") + ":Link/Department:120",
	_("Date") + ":Date:130",
	_("Cost incured") + ":Currency:130",
	_("Blood Relation") + ":Check:100",
	_("Name") + ":Data:200",
	_("Relation") + ":Data:180",]
	return columns



def get_data(filters):     
    data = []     
    conditions = []  
    values = [filters.from_date, filters.to_date]  

    if filters.department:         
        conditions.append("department = %s")
        values.append(filters.department)  

    if filters.employee:         
        conditions.append("employee = %s")  
        values.append(filters.employee)  

    where_clause = f" AND {' AND '.join(conditions)}" if conditions else ""  

    query = f"""
        SELECT * FROM `tabFirst Aid` 
        WHERE date BETWEEN %s AND %s {where_clause}
    """  

    first_aid = frappe.db.sql(query, tuple(values), as_dict=True)  

    for f in first_aid:         
        row = [
			f.get("name", ""),              
            f.get("employee", ""),             
            f.get("employee_name", ""),             
            f.get("department", ""),             
            f.get("date", ""),             
            f.get("total_cost", 0),             
            f.get("for_blood_relation", ""),             
            f.get("name1", ""),  
            f.get("relation", "")  
        ]     
        data.append(row)     

    return data  
