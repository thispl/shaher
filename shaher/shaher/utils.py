import frappe
import json
import openpyxl
from six import BytesIO


#Get the below details and set to margin item table while enter the margin item calculation
@frappe.whitelist()
def get_last_valuation_rate(item_code,source_company):
	valuation_rate = 0
	source_warehouse = frappe.db.get_value('Warehouse', {'default_for_stock_transfer':1,'company': source_company }, ["name"])
	latest_vr = frappe.db.sql("""select valuation_rate as vr from tabBin
			where item_code = '%s' and warehouse = '%s' """%(item_code,source_warehouse),as_dict=True)
	# latest_vr = frappe.db.sql("""
	#             SELECT valuation_rate as vr FROM `tabStock Ledger Entry` WHERE item_code = %s AND company=%s AND valuation_rate > 0
	#             ORDER BY posting_date DESC, posting_time DESC, creation DESC LIMIT 1
	#             """, (item_code,source_warehouse),as_dict=True)
	if latest_vr:
		if latest_vr[0]["vr"] > 0:
			valuation_rate = latest_vr[0]["vr"]
		else:
			val_rate = []
			l_vr = frappe.db.sql("""select valuation_rate as vr from tabBin
					where item_code = '%s' """%(item_code),as_dict=True)
			for item in l_vr: 
				if item not in val_rate: 
					val_rate.append(item.vr)
			if len(val_rate) > 1 :
				valuation_rate = max(val_rate)
	else:
		val_rate = []
		l_vr = frappe.db.sql("""select valuation_rate as vr from tabBin
				where item_code = '%s' """%(item_code),as_dict=True)
		for item in l_vr: 
			if item not in val_rate: 
				val_rate.append(item.vr)
		if len(val_rate) > 1 :
			valuation_rate = max(val_rate)
	return valuation_rate


@frappe.whitelist()
def update_detail_stock(item_details, company):
    item_details = json.loads(item_details)
    house = frappe.db.sql("""SELECT name from `tabWarehouse` WHERE name LIKE %s""",("%Stores%",), as_dict=True)
    data = ''
    data += '<h4><center><b>STOCK DETAILS</b></center></h4>'
    data += '<h6>Note:</h6>'
    data += '<table style="font-size:10px; width:100%;" >'

    col_count = 0
    data += '<tr>'

    for h in house:
        data += '<td>{}</td>'.format(h["name"])
        col_count += 1

        if col_count % 5 == 0:
            data += '</tr><tr>'

    if col_count % 5 != 0:
        remaining_cols = 5 - (col_count % 5)
        data += '<td></td>' * remaining_cols
        data += '</tr>'
    data += '</table>'
    data += '<table class="table table-bordered" style = font-size:10px>'
    data += '<td colspan=1 style="width:12%;padding:1px;border:1px solid black;background-color:#b81a0f;color:white;"><center><b>ITEM CODE</b></center></td>'
    data += '<td colspan=1 style="width:20%;padding:1px;border:1px solid black;background-color:#b81a0f;color:white;"><center><b>ITEM NAME</b></center></td>'
    data += '<td colspan=1 style="width:70px;padding:1px;border:1px solid black;background-color:#b81a0f;color:white;"><center><b>STOCK</b></center></td>'
    # comp = frappe.db.get_list("Company","name")
    comp = frappe.db.sql("""select name from `tabCompany`""",as_dict=1)
    for co in comp:
        st = 0
        ware = frappe.db.sql(
                    """SELECT name FROM `tabWarehouse` WHERE company = %s AND disabled != 1 AND name LIKE %s""",
                    (co.name, "%Stores%"),
                    as_dict=True
                )        # ware = frappe.db.get_list("Warehouse",{"company":co.name,"default_for_stock_transfer":1},['name'])
        for w in ware:

            data += '<td colspan=1 style="width:70px;padding:1px;border:1px solid black;background-color:#b81a0f;color:white;"><center><b>%s</b></center></td>'%(w.name.split("-")[-1]) 
    data += '<td colspan=1 style="width:180px;padding:1px;border:1px solid black;background-color:#b81a0f;color:white;"><center><b>TO RECEIVE</b></center></td>'
    data += '<td colspan=1 style="width:180px;padding:1px;border:1px solid black;background-color:#b81a0f;color:white;"><center><b>TO SELL</b></center></td>'
    warehouses = []  
    for j in item_details:
        country = frappe.get_value("Company",{"name":company},["country"])

        warehouse_stock = frappe.db.sql("""
        select sum(b.actual_qty) as qty from `tabBin` b join `tabWarehouse` wh on wh.name = b.warehouse join `tabCompany` c on c.name = wh.company where c.country = '%s' and b.item_code = '%s'
        """ % (country,j["item_code"]),as_dict=True)[0]

        if not warehouse_stock["qty"]:
            warehouse_stock["qty"] = 0
        
        
        new_po = frappe.db.sql("""select sum(`tabPurchase Order Item`.qty) as qty,sum(`tabPurchase Order Item`.received_qty) as d_qty from `tabPurchase Order` 
        left join `tabPurchase Order Item` on `tabPurchase Order`.name = `tabPurchase Order Item`.parent
        where `tabPurchase Order Item`.item_code = '%s' and `tabPurchase Order`.docstatus = 1 and `tabPurchase Order`.status != 'Closed' """ % (j["item_code"]), as_dict=True)[0]
        if not new_po['qty']:
            new_po['qty'] = 0
        if not new_po['d_qty']:
            new_po['d_qty'] = 0
        in_transit = new_po['qty'] - new_po['d_qty']


        
        total = warehouse_stock["qty"] + in_transit

        stocks = frappe.db.sql("""select actual_qty,warehouse,stock_uom,stock_value from tabBin
        where item_code = '%s' """%(j["item_code"]),as_dict=True)

        pos = frappe.db.sql("""select `tabPurchase Order Item`.item_code as item_code,`tabPurchase Order Item`.item_name as item_name,`tabPurchase Order`.supplier as supplier,sum(`tabPurchase Order Item`.qty) as qty,`tabPurchase Order Item`.rate as rate,`tabPurchase Order`.transaction_date as date,`tabPurchase Order`.name as po from `tabPurchase Order`
        left join `tabPurchase Order Item` on `tabPurchase Order`.name = `tabPurchase Order Item`.parent
        where `tabPurchase Order Item`.item_code = '%s' and `tabPurchase Order`.docstatus != 2 order by rate asc limit 1""" % (j["item_code"]), as_dict=True)
    
        new_so = frappe.db.sql("""select sum(`tabSales Order Item`.qty) as qty,sum(`tabSales Order Item`.delivered_qty) as d_qty from `tabSales Order`
        left join `tabSales Order Item` on `tabSales Order`.name = `tabSales Order Item`.parent
        where `tabSales Order Item`.item_code = '%s' and `tabSales Order`.docstatus = 1 and `tabSales Order`.status != "Closed" """ % (j["item_code"]), as_dict=True)[0]
        if not new_so['qty']:
            new_so['qty'] = 0
        if not new_so['d_qty']:
            new_so['d_qty'] = 0
        del_total = new_so['qty'] - new_so['d_qty']
        i = 0
        for po in pos:
            data += '<tr>'
            data += '<td style="text-align:center;border: 1px solid black" colspan=1>%s</td>' % (j["item_code"])
            data += '<td style="text-align:center;border: 1px solid black" colspan=1>%s</td>' % (j["item_name"])
            data += '<td style="text-align:center;border: 1px solid black" colspan=1>%s</td>' % (warehouse_stock['qty'] or 0				)
            comp = frappe.db.sql("""select name from `tabCompany`""",as_dict=1)
            for co in comp:
                st = 0
                ware = frappe.db.sql("""select name from `tabWarehouse` where company = %s AND disabled != 1 and name like %s """,(co.name, "%Stores%"),as_dict=1)
                for w in ware:
                    sto = frappe.db.get_value("Bin",{"item_code":j["item_code"],"warehouse":w.name},['actual_qty'])
                    if not sto:
                        sto = 0
                    st += sto
                    data += '<td style="text-align:center;border: 1px solid black" colspan=1>%s</td>' %(st)
            data += '<td style="text-align:center;border: 1px solid black" colspan=1>%s</td>'%(in_transit or 0)
            data += '<td style="text-align:center;border: 1px solid black" colspan=1>%s</td>'%(del_total or 0)
            data += '</tr>'
        i += 1
    data += '</tr>'
    data += '</table>'
    return data


@frappe.whitelist()
def make_item_sheet():
    args = frappe.local.form_dict
    filename = args.name
    test = build_xlsx_response(filename)

def build_xlsx_response(filename):
    xlsx_file = make_xlsx(filename)
    frappe.response['filename'] = filename + '.xlsx'
    frappe.response['filecontent'] = xlsx_file.getvalue()
    frappe.response['type'] = 'binary' 	
    
def make_xlsx(data, sheet_name=None, wb=None, column_widths=None):
    args = frappe.local.form_dict
    column_widths = column_widths or []
    if wb is None:
        wb = openpyxl.Workbook()
    ws = wb.create_sheet(sheet_name, 0)
    if args.doctype == "Quotation":
        doc = frappe.get_doc(args.doctype,args.name)
        if doc:
            ws.append(["Item Code","Item Name","Brand","Qty","UOM","Rate","Amount"])
            for i in doc.items:
                ws.append([i.item_code,i.item_name,i.brand,i.qty,i.uom,i.rate,i.amount])
    # if args.doctype == "Sales Invoice":
    #     doc = frappe.get_doc(args.doctype,args.name)
    #     if doc:
    #         ws.append(["Item Code","Item Name","Qty","UOM","Rate","Amount"])
    #         for i in doc.items:
    #             ws.append([i.item_code,i.item_name,i.qty,i.uom,i.rate,i.amount])
    # if args.doctype == "Sales Order":
    #     doc = frappe.get_doc(args.doctype,args.name)
    #     if doc:
    #         ws.append(["Item Code","Item Name","Delivery Date","Qty","UOM","Rate","Amount"])
    #         for i in doc.items:
    #             ws.append([i.item_code,i.item_name,i.delivery_date,i.qty,i.uom,i.rate,i.amount])
    # if args.doctype == "Delivery Note":
    #     doc = frappe.get_doc(args.doctype,args.name)
    #     if doc:
    #         ws.append(["Item Code","Item Name","Qty","UOM","Rate","Amount"])
    #         for i in doc.items:
    #             ws.append([i.item_code,i.item_name,i.qty,i.uom,i.rate,i.amount])
    # if args.doctype == "Landed Cost Voucher":
    #     doc = frappe.get_doc(args.doctype,args.name)
    #     if doc:
    #         ws.append(["Item Code","Description","Qty","Current Rate After LCV"])
    #         for i in doc.items:
    #             ws.append([i.item_code,i.description,i.qty,i.current_rate_after_lcv])
    # if args.doctype == "Project Budget":
    #     doc = frappe.get_doc(args.doctype,args.name)
    #     if doc:
    #         ws.append(["Item Code","Item Name","Unit","Qty"])
    #         for i in doc.item_table:
    #             ws.append([i.item,i.item_name,i.unit,i.qty])
                
    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    return xlsx_file


@frappe.whitelist()
def get_item_margin(item_details,company,discount_amount):
    item_details = json.loads(item_details)
    data_4 = ''
    data_4 += '''<table class="table">
    <tr>
    <th style="padding:1px;border: 1px solid black;font-size:14px;background-color:#FF4500;color:white;" colspan =9 ><center><b>MARGIN</b></center></th>
    </tr>'''

    data_4+='''<tr>
    <td colspan=1 style="border: 1px solid black;font-size:12px;"><b>ITEM</b></td>
    <td colspan=1 style="border: 1px solid black;font-size:12px;"><b>ITEM NAME</b></td>
    <td colspan=1 style="border: 1px solid black;font-size:12px;"><b><center>QTY</center></b></td>
    <td colspan=1 style="border: 1px solid black;font-size:12px;"><b><center>Cost</center></b></td>
    <td colspan=1 style="border: 1px solid black;font-size:12px;"><b><center>Rate</center></b></td>
    <td colspan=1 style="border: 1px solid black;font-size:12px;"><b><center>Cost Amount</center></b></td>
    <td colspan=1 style="border: 1px solid black;font-size:12px;"><b><center>Selling Amount</center></b></td>
    <td colspan=1 style="border: 1px solid black;font-size:12px;"><b><center>Profit Amount</center></b></td>
    <td colspan=1 style="border: 1px solid black;font-size:12px;"><b><center>Profit %</center></b></td>
    </tr>'''
    cost_amount = 0
    total_selling_price = 0
    rate = 0
    cost = 0
    selling_amount = 0
    profit_amount_ = 0
    selling_amount_ = 0
    qty_tot = 0
    tot_per = 0
    no_item = 0
    for i in item_details:
        qty_tot += i["qty"]
        rate += i["base_net_rate"]
        selling_amount += i["base_net_amount"]
        total_selling_price = (i["base_net_rate"] * i["qty"]) + total_selling_price
        
        warehouse_stock = frappe.db.sql("""
            SELECT valuation_rate as vr 
            FROM `tabBin` b 
            JOIN `tabWarehouse` wh ON wh.name = b.warehouse
            JOIN `tabCompany` c ON c.name = wh.company
            WHERE b.item_code = %s AND c.name = %s
            """, (i["item_code"], company), as_dict=True)
        
        if warehouse_stock:
            warehouse_stock = warehouse_stock[0]
            if not warehouse_stock["vr"]:
                warehouse_stock["vr"] = 0
        else:
            if frappe.db.get_value("Item Price",{'item_code':i["item_code"],'price_list':'Standard Buying'}):
                std_selling=frappe.db.get_value("Item Price",{'item_code':i["item_code"],'price_list':'Standard Buying'},['price_list_rate'])
                if std_selling:
                    warehouse_stock = {"vr": std_selling}
                else:
                    warehouse_stock = {"vr": 0}
            else:
                warehouse_stock = {"vr": 0}

        cost += warehouse_stock["vr"]
        cost_amount = (warehouse_stock["vr"] * i["qty"]) + cost_amount
        cost_amount_ = (warehouse_stock["vr"] * i["qty"])
        
        tot = cost_amount - total_selling_price
        tot_diff = cost_amount_ - i["base_net_amount"]
        
        if cost_amount_ > 0:
            tot_ = tot_diff / cost_amount_ * 100
            tot_per += tot_
            
            data_4 += '''<tr>
                <td colspan=1 style="border: 1px solid black;font-size:12px;">{}</td>
                <td colspan=1 style="border: 1px solid black;font-size:12px;">{}</td>
                <td colspan=1 style="border: 1px solid black;font-size:12px; text-align: right">{}</td>
                <td colspan=1 style="border: 1px solid black;font-size:12px; text-align: right">{}</td>
                <td colspan=1 style="border: 1px solid black;font-size:12px; text-align: right">{}</td>
                <td colspan=1 style="border: 1px solid black;font-size:12px; text-align: right">{}</td>
                <td colspan=1 style="border: 1px solid black;font-size:12px; text-align: right">{}</td>
                <td colspan=1 style="border: 1px solid black;font-size:12px; text-align: right">{}</td>
                <td colspan=1 style="border: 1px solid black;font-size:12px; text-align: right">{}</td>
            </tr>'''.format(i["item_code"], i["description"], i["qty"], round(warehouse_stock["vr"], 2), round(i["base_net_rate"], 2), round(cost_amount_, 2), round(i["base_net_amount"], 2), round(-tot_diff, 2), round(-tot_, 2))
    
    if cost_amount_ == 0:
        total_margin_internal = (total_selling_price - cost_amount_)/100

    else:
        total_margin_internal = (-tot / cost_amount)*100

        data_4 += '''<tr>
        <td colspan=2 style="border: 1px solid black;padding:1px;font-size:14px;text-align: right"><b>Total </b></td>
        <td style="border: 1px solid black;padding:1px;font-size:12px;text-align: right"><b>%s</b></td>
        <td style="border: 1px solid black;padding:1px;font-size:12px;text-align: right"><b>%s</b></td>
        <td style="border: 1px solid black;padding:1px;font-size:12px;text-align: right"><b>%s</b></td>
        <td style="border: 1px solid black;padding:1px;font-size:12px;text-align: right"><b>%s</b></td>
        <td style="border: 1px solid black;padding:1px;font-size:12px;text-align: right"><b>%s</b></td>
        <td style="border: 1px solid black;padding:1px;font-size:12px;text-align: right"><b>%s</b></td>
        <td style="border: 1px solid black;padding:1px;font-size:12px;text-align: right"><b>%s</b></td>
        </tr>'''%(qty_tot,round(cost,2),round(rate,2),round(cost_amount,2),round(selling_amount,2),round(-tot,2),round(total_margin_internal,2))
        
        total_amount = float(discount_amount) + float(selling_amount)
        data_4+= '''<tr>
        <td colspan=2 style="border: 1px solid black;padding:1px;font-size:12px;text-align: right"><b>Before Applying Discount</b></td>
        <td style="border: 1px solid black;padding:1px;font-size:12px;text-align: right"><b>%s</b></td>
        <td colspan=2 style="border: 1px solid black;padding:1px;font-size:12px;text-align: right"><b>Discount Amount </b></td>
        <td style="border: 1px solid black;padding:1px;font-size:12px;text-align: right"><b>%s</b></td>
        <td colspan=2 style="border: 1px solid black;padding:1px;font-size:12px;text-align: right"><b>After Applying Discount</b></td>
        <td style="border: 1px solid black;padding:1px;font-size:12px;text-align: right"><b>%s</b></td>
        </tr>'''%(total_amount,discount_amount,selling_amount)
        
    
    return data_4
