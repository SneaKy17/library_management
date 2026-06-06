"""
library_management/tasks.py
Scheduled background jobs for the Library Management app.
Registered via hooks.py → scheduler_events.
"""

import frappe
from frappe.utils import today


def mark_overdue_transactions():
	"""
	Daily scheduled task.
	Scans all Book Transactions with status='Issued' whose due_date
	has already passed and marks them as 'Overdue'.
	"""
	overdue_txns = frappe.get_all(
		"Book Transaction",
		filters={
			"status": "Issued",
			"transaction_type": "Issue",
			"due_date": ["<", today()],
		},
		fields=["name", "member", "book", "due_date"],
	)

	if not overdue_txns:
		frappe.logger().info("[Library Management] No overdue transactions found.")
		return

	for txn in overdue_txns:
		frappe.db.set_value("Book Transaction", txn["name"], "status", "Overdue")
		frappe.logger().info(
			f"[Library Management] Marked {txn['name']} as Overdue "
			f"(member={txn['member']}, book={txn['book']}, "
			f"due={txn['due_date']})."
		)

	frappe.db.commit()
	frappe.logger().info(
		f"[Library Management] Daily job complete — "
		f"{len(overdue_txns)} transaction(s) marked Overdue."
	)
