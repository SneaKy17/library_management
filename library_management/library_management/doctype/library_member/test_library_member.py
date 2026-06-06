"""
Unit tests for the Library Member DocType.
Run via: bench --site <site> run-tests --app library_management --doctype "Library Member"
"""

import unittest

import frappe
from frappe.utils import add_days, today


class TestLibraryMember(unittest.TestCase):

	# ── helpers ────────────────────────────────────────────────────────────

	def _make_member(self, email="lm_test_1@example.com", **kwargs):
		doc = frappe.get_doc({
			"doctype": "Library Member",
			"first_name": "Test",
			"last_name": "Member",
			"email": email,
			"membership_type": "Standard",
			"membership_start_date": today(),
			"status": "Active",
			**kwargs,
		})
		doc.insert(ignore_permissions=True)
		return doc

	def _cleanup(self, *emails):
		for email in emails:
			name = frappe.db.get_value("Library Member", {"email": email}, "name")
			if name:
				frappe.delete_doc("Library Member", name, force=True)

	# ── tests ──────────────────────────────────────────────────────────────

	def test_full_name_auto_set(self):
		"""full_name must be auto-populated as 'First Last' on save."""
		doc = self._make_member(
			email="lm_test_fn@example.com",
			first_name="Alice",
			last_name="Smith",
		)
		self.assertEqual(doc.full_name, "Alice Smith")
		self._cleanup("lm_test_fn@example.com")

	def test_full_name_updates_on_rename(self):
		"""full_name must update if first_name or last_name changes."""
		doc = self._make_member(
			email="lm_test_rename@example.com",
			first_name="Bob",
			last_name="Jones",
		)
		doc.last_name = "Williams"
		doc.save(ignore_permissions=True)
		self.assertEqual(doc.full_name, "Bob Williams")
		self._cleanup("lm_test_rename@example.com")

	def test_status_default_is_active(self):
		"""Default status must be 'Active'."""
		doc = self._make_member(email="lm_test_status@example.com")
		self.assertEqual(doc.status, "Active")
		self._cleanup("lm_test_status@example.com")

	def test_email_uniqueness_enforced(self):
		"""Inserting two members with the same email must raise an error."""
		self._make_member(email="lm_test_dup@example.com")
		with self.assertRaises(Exception):
			self._make_member(
				email="lm_test_dup@example.com",
				first_name="Duplicate",
				last_name="User",
			)
		self._cleanup("lm_test_dup@example.com")

	def test_end_date_before_start_raises(self):
		"""Saving with membership_end_date < membership_start_date must raise."""
		with self.assertRaises(frappe.ValidationError):
			self._make_member(
				email="lm_test_dates@example.com",
				membership_start_date=today(),
				membership_end_date=add_days(today(), -10),
			)
		self._cleanup("lm_test_dates@example.com")

	def test_valid_date_range_passes(self):
		"""A valid date range (end > start) must save without errors."""
		doc = self._make_member(
			email="lm_test_validdate@example.com",
			membership_start_date=today(),
			membership_end_date=add_days(today(), 365),
		)
		self.assertIsNotNone(doc.name)
		self._cleanup("lm_test_validdate@example.com")
