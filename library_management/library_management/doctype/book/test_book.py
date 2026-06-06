"""
Unit tests for the Book DocType.
Run via: bench --site <site> run-tests --app library_management --doctype "Book"
"""

import unittest

import frappe


class TestBook(unittest.TestCase):

	# ── helpers ────────────────────────────────────────────────────────────

	def _make_book(self, isbn="BOOK-TEST-001", **kwargs):
		doc = frappe.get_doc({
			"doctype": "Book",
			"title": "Test Book",
			"author": "Test Author",
			"isbn": isbn,
			"total_copies": 5,
			**kwargs,
		})
		doc.insert(ignore_permissions=True)
		return doc

	def _cleanup(self, *isbns):
		for isbn in isbns:
			name = frappe.db.get_value("Book", {"isbn": isbn}, "name")
			if name:
				frappe.delete_doc("Book", name, force=True)

	# ── tests ──────────────────────────────────────────────────────────────

	def test_available_copies_defaults_to_total(self):
		"""available_copies must default to total_copies on first insert."""
		doc = self._make_book(isbn="BOOK-TEST-D1", total_copies=4)
		self.assertEqual(doc.available_copies, 4)
		self._cleanup("BOOK-TEST-D1")

	def test_status_defaults_to_available(self):
		"""Status must be 'Available' when there are copies in stock."""
		doc = self._make_book(isbn="BOOK-TEST-D2", total_copies=2)
		self.assertEqual(doc.status, "Available")
		self._cleanup("BOOK-TEST-D2")

	def test_zero_copies_sets_checked_out(self):
		"""available_copies=0 must auto-set status to 'Checked Out'."""
		doc = self._make_book(isbn="BOOK-TEST-D3", total_copies=3, available_copies=0)
		self.assertEqual(doc.status, "Checked Out")
		self._cleanup("BOOK-TEST-D3")

	def test_negative_total_copies_raises(self):
		"""Negative total_copies must raise a ValidationError."""
		with self.assertRaises(frappe.ValidationError):
			self._make_book(isbn="BOOK-TEST-E1", total_copies=-1)
		self._cleanup("BOOK-TEST-E1")

	def test_negative_available_copies_raises(self):
		"""Negative available_copies must raise a ValidationError."""
		with self.assertRaises(frappe.ValidationError):
			self._make_book(isbn="BOOK-TEST-E2", total_copies=5, available_copies=-1)
		self._cleanup("BOOK-TEST-E2")

	def test_available_exceeds_total_raises(self):
		"""available_copies > total_copies must raise a ValidationError."""
		with self.assertRaises(frappe.ValidationError):
			self._make_book(isbn="BOOK-TEST-E3", total_copies=3, available_copies=10)
		self._cleanup("BOOK-TEST-E3")

	def test_isbn_uniqueness_enforced(self):
		"""Two books with the same ISBN must raise an error."""
		self._make_book(isbn="BOOK-TEST-U1")
		with self.assertRaises(Exception):
			self._make_book(isbn="BOOK-TEST-U1", title="Duplicate")
		self._cleanup("BOOK-TEST-U1")

	def test_maintenance_status_not_overridden(self):
		"""Status='Maintenance' must not be auto-overridden by copy count logic."""
		doc = self._make_book(
			isbn="BOOK-TEST-M1",
			total_copies=3,
			available_copies=3,
			status="Maintenance",
		)
		self.assertEqual(doc.status, "Maintenance")
		self._cleanup("BOOK-TEST-M1")
