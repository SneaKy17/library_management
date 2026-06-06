import frappe
from frappe.model.document import Document
from frappe.utils import today, add_days


class BookTransaction(Document):

	def validate(self):
		# Auto-set transaction date if missing
		if not self.transaction_date:
			self.transaction_date = today()

		if self.transaction_type == "Issue":
			# Only validate availability on new Issue records
			if self.is_new():
				self._validate_member_active()
				self._validate_book_available()
			# Auto-set due date to 14 days from transaction date
			if not self.due_date:
				self.due_date = add_days(self.transaction_date, 14)
			self.status = "Issued"

		elif self.transaction_type == "Return":
			# Auto-set return date if not provided
			if not self.return_date:
				self.return_date = today()
			self.status = "Returned"

	def after_insert(self):
		"""Sync Book.available_copies after a new transaction is created."""
		if self.transaction_type == "Issue":
			self._decrement_available_copies()
		elif self.transaction_type == "Return":
			self._increment_available_copies()

	# ──────────────────────────────────────────────
	# Validation helpers
	# ──────────────────────────────────────────────

	def _validate_member_active(self):
		"""Ensure the member is Active before issuing a book."""
		member_status = frappe.db.get_value("Library Member", self.member, "status")
		if member_status != "Active":
			frappe.throw(
				f"Member <b>{self.member}</b> is not Active "
				f"(current status: <b>{member_status}</b>). "
				"Cannot issue a book to an inactive member.",
				title="Member Not Active"
			)

	def _validate_book_available(self):
		"""Ensure at least one copy is available before issuing."""
		available = frappe.db.get_value("Book", self.book, "available_copies") or 0
		if available <= 0:
			frappe.throw(
				f"Book <b>{self.book}</b> has no available copies.",
				title="No Copies Available"
			)

	# ──────────────────────────────────────────────
	# Copy-count sync helpers
	# ──────────────────────────────────────────────

	def _decrement_available_copies(self):
		"""Decrement available_copies by 1 when a book is issued."""
		book = frappe.get_doc("Book", self.book)
		book.available_copies = max(0, (book.available_copies or 0) - 1)
		if book.available_copies == 0:
			book.status = "Checked Out"
		book.save(ignore_permissions=True)

	def _increment_available_copies(self):
		"""Increment available_copies by 1 when a book is returned."""
		book = frappe.get_doc("Book", self.book)
		book.available_copies = min(
			book.total_copies or 0,
			(book.available_copies or 0) + 1
		)
		if book.available_copies > 0 and book.status == "Checked Out":
			book.status = "Available"
		book.save(ignore_permissions=True)
