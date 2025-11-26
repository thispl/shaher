from datetime import datetime
import frappe
import xml.etree.ElementTree as ET
import calendar

@frappe.whitelist()
def parse_uploaded_xml(file_name):
    # Get the file path from File doctype
    # file_name = "PO_4501010486.XML"
    file_doc = frappe.get_doc("File", {"file_url": file_name})
    file_path = frappe.get_site_path('public', 'files', file_doc.file_name)

    # Parse the XML
    tree = ET.parse(file_path)
    root = tree.getroot()
    po = root.find('PurchaseOrder')
    customer_po_no = po.findtext('ID')
    po_date_text = po.findtext('BuyerPostingDateTime')
    po_date = po_date_text.split('T')[0]
    so = frappe.new_doc("Sales Order")
    so.customer = "Petroleum Development Oman LLC"
    so.custom_department = 'PDO - SUTC'
    so.company = 'SHAHER UNITED TRADING & CONTRACTING COMPANY'
    so.naming_series = "SO-PDO-.{custom_company_shortcode}.-.YYYY.-"
    so.selling_price_list = 'PDO Price List'
    so.po_no = customer_po_no
    so.po_date = po_date
    so.transaction_date = po_date
    so.project = 'PDO (C311636) UIE Contract'
    i=0
    date_obj = datetime.today()

    year = date_obj.year
    month = date_obj.month
    last_day = calendar.monthrange(year, month)[1]

    for item in po.findall('Item'):
        product = item.find('Product')
        ScheduleLine = item.find('ScheduleLine')
        Quantity  =ScheduleLine.find('Quantity') if ScheduleLine is not None else None
        base_quantity = Quantity.text if Quantity is not None else None
        unit_code = Quantity.attrib.get('unitCode') if Quantity is not None else None
        # StartDateTime = DeliveryPeriod.findtext('StartDateTime')
        # dn_date = StartDateTime.split('T')[0] if StartDateTime is not None else None
        note = product.findtext('Note') if product is not None else None
        buyer_id = product.findtext('BuyerID') if product is not None else None
        HierarchyRelationship = item.find('HierarchyRelationship')
        po_li = HierarchyRelationship.findtext('ParentItemSellerID') if HierarchyRelationship is not None else None
        price = item.find('Price')
        netpriceunit = price.find('NetUnitPrice') if price is not None else None
        base_quantity_elem = netpriceunit.find('BaseQuantity') if netpriceunit is not None else None
        base_rate = netpriceunit.findtext('Amount') if netpriceunit is not None else None

        # base_quantity = base_quantity_elem.text if base_quantity_elem is not None else None
        # unit_code = base_quantity_elem.attrib.get('unitCode') if base_quantity_elem is not None else None
        amount = price.findtext('NetAmount') if price is not None else None
        if buyer_id:
            i += 1
            if not frappe.db.exists("Item",{'custom_service_entry':buyer_id}):
                item_doc = frappe.new_doc("Item")
                item_doc.item_code = buyer_id
                item_doc.item_group = 'Services - PDO'
                item_doc.is_stock_item = 0
                item_doc.item_name = note
                item_doc.custom_service_entry = buyer_id
                item_doc.save(ignore_permissions=True)
                item_code = item_doc.name
            else:
                item_code = frappe.db.get_value("Item",{'custom_service_entry':buyer_id},['name'])
            so.append('items',{
                'custom_po_li':po_li + '.' + str(i) if po_li is not None else str(i),
                'item_code':item_code,
                'item_name':note,
                'description':note,
                "uom":unit_code,
                'qty':base_quantity,
                'rate':base_rate,
                'amount':amount
            })
        else:
            i = 0
    so.delivery_date=datetime(year, month, last_day).date()
    so.save(ignore_permissions=True)

    return so.name
