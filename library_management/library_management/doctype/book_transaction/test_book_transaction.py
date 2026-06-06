"""
Unit tests for the Book Transaction DocType.
Run via: bench --site <site> run-tests --app library_management --doctype "Book Transaction"
"""

import unittest

import frappe
from frappe.utils import add_days, today


class TestBookTransaction(unittest.TestCase):
	"""
	Shared fixtures: one Library Member + one Book created once per class,
	cleaned up after all tests in the class have run.
	"""

	member_name = None
	book_name = None

	# ── class-level fixtures ───────────────────────────────────────────────

	@classmethod
	def setUpClass(cls):
		frappe.set_user("Administrator")

		# Create member
		m = frappe.get_doc({
			"doctype": "Library Member",
			"first_name": "TxnTest",
			"last_name": "User",
			"email": "txn_test_suite@example.com",
			"membership_type": "Standard",
			"membership_start_date": today(),
			"status": "Active",
		}).insert(ignore_permissions=True)
		cls.member_name = m.name

		# Create book with 5 copies
		b = frappe.get_doc({
			"doctype": "Book",
			"title": "Transaction Test Book",
			"author": "Test Author",
			"isbn": "TXN-SUITE-ISBN-001",
			"total_copies": 5,
			"status": "Available",
		}).insert(ignore_permissions=True)
		cls.book_name = b.name

	@classmethod
	def tearDownClass(cls):
		# Remove all transactions created during tests
		frappe.db.delete(
			"Book Transaction",
			{"member": cls.member_name, "book": cls.book_name},
		)
		if cls.member_name:
			frappe.delete_doc("Library Member", cls.member_name, force=True)
		if cls.book_name:
			frappe.delete_doc("Book", cls.book_name, force=True)

	# ── per-test fixture ───────────────────────────────────────────────────

	def setUp(self):
		# Reset book copies to 5 before every individual test
		frappe.db.set_value("Book", self.book_name, "available_copies", 5)
		frappe.db.set_value("Book", self.book_name, "status", "Available")
		frappe.db.set_value("Library Member", self.member_name, "status", "Active")

	def tearDown(self):
		# Remove transactions created in this test
		frappe.db.delete(
			"Book Transaction",
			{"member": self.member_name, "book": self.book_name},
		)

	# ── helpers ────────────────────────────────────────────────────────────

	def _make_txn(self, txn_type="Issue", **kwargs):
		doc = frappe.get_doc({
			"doctype": "Book Transaction",
			"member": self.member_name,
			"book": self.book_name,
			"transaction_type": txn_type,
			"transaction_date": today(),
			**kwargs,
		})
		doc.insert(ignore_permissions=True)
		return doc

	# ── tests ──────────────────────────────────────────────────────────────

	def test_transaction_date_auto_set(self):
		"""transaction_date must default to today when not provided."""
		doc = self._make_txn()
		self.assertEqual(str(doc.transaction_date), today())

	def test_due_date_auto_set_14_days(self):
		"""due_date must be auto-set to transaction_date + 14 days on Issue."""
		doc = self._make_txn(txn_type="Issue")
		expected = add_days(today(), 14)
		self.assertEqual(str(doc.due_date), str(expected))

	def test_issue_decrements_available_copies(self):
		"""Issuing a book must decrement Book.available_copies by 1."""
		before = frappe.db.get_value("Book", self.book_name, "available_copies")
		self._make_txn(txn_type="Issue")
		after = frappe.db.get_value("Book", self.book_name, "available_copies")
		self.assertEqual(after, before - 1)

	def test_return_increments_available_copies(self):
		"""Returning a book must increment Book.available_copies by 1."""
		# Issue first
		self._make_txn(txn_type="Issue")
		after_issue = frappe.db.get_value("Book", self.book_name, "available_copies")
		self._make_txn(txn_type="Return")
		after_return = frappe.db.get_value("Book", self.book_name, "available_copies")
		self.assertEqual(after_return, after_issue + 1)

	def test_issue_sets_status_to_issued(self):
		"""An Issue transaction must have status='Issued'."""
		doc = self._make_txn(txn_type="Issue")
		self.assertEqual(doc.status, "Issued")

	def test_return_sets_status_to_returned(self):
		"""A Return transaction must have status='Returned'."""
		doc = self._make_txn(txn_type="Return")
		self.assertEqual(doc.status, "Returned")

	def test_return_sets_return_date_auto(self):
		"""return_date must be auto-set to today when not provided on a Return."""
		doc = self._make_txn(txn_type="Return")
		self.assertEqual(str(doc.return_date), today())

	def test_no_copies_blocks_issue(self):
		"""Issuing a book with 0 available copies must raise ValidationError."""
		frappe.db.set_value("Book", self.book_name, "available_copies", 0)
		with self.assertRaises(frappe.ValidationError):
			self._make_txn(txn_type="Issue")

	def test_all_copies_checked_out_sets_book_status(self):
		"""When the last copy is issued, Book.status must become 'Checked Out'."""
		frappe.db.set_value("Book", self.book_name, "available_copies", 1)
		self._make_txn(txn_type="Issue")
		status = frappe.db.get_value("Book", self.book_name, "status")
		self.assertEqual(status, "Checked Out")

	def test_inactive_member_blocked_from_issue(self):
		"""Issuing to an Inactive member must raise ValidationError."""
		frappe.db.set_value("Library Member", self.member_name, "status", "Inactive")
		with self.assertRaises(frappe.ValidationError):
			self._make_txn(txn_type="Issue")

	def test_suspended_member_blocked_from_issue(self):
		"""Issuing to a Suspended member must raise ValidationError."""
		frappe.db.set_value("Library Member", self.member_name, "status", "Suspended")
		with self.assertRaises(frappe.ValidationError):
			self._make_txn(txn_type="Issue")
