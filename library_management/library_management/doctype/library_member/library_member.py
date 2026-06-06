import frappe
from frappe.model.document import Document


class LibraryMember(Document):

	def before_save(self):
		self.full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()

	def validate(self):
		# Ensure membership end date is not before start date
		if (
			self.membership_end_date
			and self.membership_start_date
			and self.membership_end_date < self.membership_start_date
		):
			frappe.throw(
				"Membership End Date cannot be before Membership Start Date.",
				title="Invalid Date Range"
			)
