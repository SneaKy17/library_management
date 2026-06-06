import frappe
from frappe.model.document import Document


class Book(Document):
	def before_save(self):
		if self.total_copies is not None and self.available_copies is None:
			self.available_copies = self.total_copies
