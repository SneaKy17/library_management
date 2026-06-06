import frappe
from frappe.model.document import Document


class BookTransaction(Document):
	def validate(self):
		if not self.transaction_date:
			self.transaction_date = frappe.utils.today()
