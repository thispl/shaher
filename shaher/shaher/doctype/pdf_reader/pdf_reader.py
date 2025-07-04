# Copyright (c) 2025, Amar Karthick P and contributors
# For license information, please see license.txt

import frappe
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io
import os

from frappe.model.document import Document

class PDFReader(Document):
	pass

@frappe.whitelist()
def fill_service_entry(file_url, service_entry_text, date_text):
	try:
		# Define A4 dimensions
		width, height = A4

		# Get the file document and its path
		file_doc = frappe.get_doc("File", {"file_url": file_url})
		original_path = frappe.get_site_path("public", file_doc.file_url.lstrip("/"))

		# Prepare output filename and path
		output_filename = "filled_" + os.path.basename(file_doc.file_url)
		output_path = frappe.get_site_path("public", "files", output_filename)

		# Create an overlay PDF in memory
		packet = io.BytesIO()
		can = canvas.Canvas(packet, pagesize=A4)

		# Example: CSS-like positioning
		# Move 100 pts from top, 150 pts from left
		service_entry_x = 200
		service_entry_y = height - 770  # top: 100pt

		date_x = 425
		date_y = height - 783

		# Draw the values
		can.setFont("Helvetica", 9)
		can.drawString(service_entry_x, service_entry_y, service_entry_text)
		can.drawString(date_x, date_y, date_text)
		can.save()
		packet.seek(0)

		# Merge overlay onto original PDF
		overlay_pdf = PdfReader(packet)
		original_pdf = PdfReader(open(original_path, "rb"))
		writer = PdfWriter()

		page = original_pdf.pages[0]
		page.merge_page(overlay_pdf.pages[0])
		writer.add_page(page)

		# Save the new PDF
		with open(output_path, "wb") as f:
			writer.write(f)

		# Return the public file URL
		return "/files/" + output_filename

	except Exception as e:
		frappe.throw(f"Failed to fill PDF: {e}")
		
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfdoc
import io

@frappe.whitelist()
def generate_fillable_pdf():
	# Create in-memory PDF
	buffer = io.BytesIO()
	can = canvas.Canvas(buffer, pagesize=A4)

	# Create form fields
	form = can.acroForm
	form.textfield(name='name', tooltip='Enter Name', x=100, y=700, width=300, height=20)
	form.textfield(name='email', tooltip='Enter Email', x=100, y=650, width=300, height=20)

	can.drawString(100, 720, "Name:")
	can.drawString(100, 670, "Email:")

	can.save()
	buffer.seek(0)

	# Save to /public/files
	filename = "fillable_form.pdf"
	filepath = frappe.get_site_path("public", "files", filename)

	with open(filepath, "wb") as f:
		f.write(buffer.read())

	# Return the public URL
	return f"/files/{filename}"

import frappe
import io
import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

@frappe.whitelist()
def generate_fillable_certificate(file_url):
	try:
		width, height = A4

		file_doc = frappe.get_doc("File", {"file_url": file_url})
		original_path = frappe.get_site_path("public", file_doc.file_url.lstrip("/"))
		output_filename = "fillable_" + os.path.basename(file_doc.file_url)
		output_path = frappe.get_site_path("public", "files", output_filename)

		packet = io.BytesIO()
		can = canvas.Canvas(packet, pagesize=A4)

		form = can.acroForm

		# form.textfield(
		# 	name='service_entry',
		# 	tooltip='Enter Service Entry Sheet No',
		# 	x=190, y=70,
		# 	width=120, height=20,
		# 	# borderColor=colors.black,
		# 	fillColor=None,
		# 	textColor=colors.black,
		# 	fontSize=10
		# )

		form.textfield(
			name='service_entry',
			tooltip='Enter Service Entry Sheet No',
			x=190, y=70,
			width=120, height=20,
			borderColor=colors.black,
			fillColor=colors.white,
			textColor=colors.black,
			fontName="Helvetica",
			fontSize=10,
			forceBorder=True
		)

		form.textfield(
			name='service_entry_date',
			tooltip='Enter Date',
			x=423, y=53,
			width=100, height=17,
			borderColor=colors.black,
			fillColor=colors.white,
			textColor=colors.black,
			fontName="Helvetica",
			fontSize=10,
			forceBorder=True
		)

		can.showPage()
		can.save()
		packet.seek(0)

		overlay_pdf = PdfReader(packet)
		original_pdf = PdfReader(open(original_path, "rb"))
		writer = PdfWriter()

		page = original_pdf.pages[0]
		page.merge_page(overlay_pdf.pages[0])
		writer.add_page(page)

		with open(output_path, "wb") as f:
			writer.write(f)

		return f"/files/{output_filename}"

	except Exception as e:
		frappe.throw(f"Error generating editable PDF: {e}")