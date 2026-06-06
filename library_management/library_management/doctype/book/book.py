import frappe
from frappe.model.document import Document


class Book(Document):

	def before_save(self):
		# Default available_copies to total_copies when first set
		if self.total_copies is not None and self.available_copies is None:
			self.available_copies = self.total_copies

	def validate(self):
		if self.total_copies is not None and self.total_copies < 0:
			frappe.throw("Total Copies cannot be negative.", title="Invalid Value")

		if self.available_copies is not None and self.available_copies < 0:
			frappe.throw("Available Copies cannot be negative.", title="Invalid Value")

		if (
			self.total_copies is not None
			and self.available_copies is not None
			and self.available_copies > self.total_copies
		):
			frappe.throw(
				"Available Copies cannot exceed Total Copies.",
				title="Invalid Value"
			)

		# Auto-derive status from available_copies (only if not in Maintenance)
		if self.status != "Maintenance" and self.available_copies is not None:
			if self.available_copies <= 0:
				self.status = "Checked Out"
			else:
				self.status = "Available"
