import frappe
from frappe.utils import today


def seed_data():
    frappe.set_user("Administrator")

    # --- Library Member ---
    members_data = [
        {"first_name": "Alice", "last_name": "Johnson", "email": "alice.johnson@example.com",
         "phone": "9876543210", "membership_type": "Standard",
         "membership_start_date": "2026-01-01", "status": "Active"},
        {"first_name": "Bob", "last_name": "Smith", "email": "bob.smith@example.com",
         "phone": "9123456789", "membership_type": "Premium",
         "membership_start_date": "2026-02-15", "status": "Active"},
        {"first_name": "Carol", "last_name": "Patel", "email": "carol.patel@example.com",
         "phone": "9000011112", "membership_type": "VIP",
         "membership_start_date": "2026-03-10", "status": "Active"},
    ]
    created_members = []
    for m in members_data:
        if not frappe.db.exists("Library Member", {"email": m["email"]}):
            doc = frappe.get_doc({"doctype": "Library Member", **m})
            doc.full_name = f"{doc.first_name} {doc.last_name}"
            doc.insert(ignore_permissions=True)
            created_members.append(doc.name)
            print(f"  Created Library Member: {doc.name} ({doc.full_name})")
        else:
            existing = frappe.db.get_value("Library Member", {"email": m["email"]}, "name")
            created_members.append(existing)
            print(f"  Exists Library Member: {existing}")

    # --- Books ---
    books_data = [
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "isbn": "9780743273565",
         "publisher": "Scribner", "publication_year": 1925, "category": "Fiction",
         "total_copies": 3, "available_copies": 3, "status": "Available"},
        {"title": "Python Crash Course", "author": "Eric Matthes", "isbn": "9781593279288",
         "publisher": "No Starch Press", "publication_year": 2019, "category": "Technology",
         "total_copies": 5, "available_copies": 4, "status": "Available"},
        {"title": "Sapiens", "author": "Yuval Noah Harari", "isbn": "9780062316097",
         "publisher": "Harper", "publication_year": 2015, "category": "History",
         "total_copies": 2, "available_copies": 2, "status": "Available"},
    ]
    created_books = []
    for b in books_data:
        if not frappe.db.exists("Book", {"isbn": b["isbn"]}):
            doc = frappe.get_doc({"doctype": "Book", **b})
            doc.insert(ignore_permissions=True)
            created_books.append(doc.name)
            print(f"  Created Book: {doc.name} ({doc.title})")
        else:
            existing = frappe.db.get_value("Book", {"isbn": b["isbn"]}, "name")
            created_books.append(existing)
            print(f"  Exists Book: {existing}")

    # --- Book Transactions ---
    txn_data = [
        {"member": created_members[0], "book": created_books[0], "transaction_type": "Issue",
         "transaction_date": "2026-05-01", "due_date": "2026-05-15", "status": "Issued"},
        {"member": created_members[1], "book": created_books[1], "transaction_type": "Issue",
         "transaction_date": "2026-05-10", "due_date": "2026-05-24", "status": "Issued"},
        {"member": created_members[0], "book": created_books[2], "transaction_type": "Return",
         "transaction_date": "2026-05-20", "return_date": "2026-05-20", "status": "Returned"},
    ]
    for t in txn_data:
        doc = frappe.get_doc({"doctype": "Book Transaction", **t})
        doc.insert(ignore_permissions=True)
        print(f"  Created Book Transaction: {doc.name}")

    frappe.db.commit()
    print("Done! All test data seeded successfully.")
