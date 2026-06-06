import frappe

def create_test_member():
    try:
        doc = frappe.get_doc({
            'doctype': 'Library Member',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'membership_start_date': frappe.utils.today(),
            'status': 'Active'
        })
        doc.insert(ignore_permissions=True, ignore_if_duplicate=True)
        frappe.db.commit()
        print('SUCCESS: Created Library Member:', doc.name)
    except Exception as e:
        print('ERROR:', str(e))
