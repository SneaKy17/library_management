import frappe

def create_library_workspace():
    frappe.set_user("Administrator")

    # Delete existing if any
    if frappe.db.exists("Workspace", "Library Management"):
        frappe.delete_doc("Workspace", "Library Management", force=True)

    workspace = frappe.get_doc({
        "doctype": "Workspace",
        "name": "Library Management",
        "label": "Library Management",
        "title": "Library Management",
        "module": "Library Management",
        "category": "Modules",
        "is_hidden": 0,
        "hide_custom": 0,
        "public": 1,
        "icon": "book",
        "color": "#3498DB",
        "links": [
            {
                "type": "Card Break",
                "label": "Library",
                "hidden": 0
            },
            {
                "type": "Link",
                "label": "Library Member",
                "link_type": "DocType",
                "link_to": "Library Member",
                "hidden": 0
            },
            {
                "type": "Link",
                "label": "Book",
                "link_type": "DocType",
                "link_to": "Book",
                "hidden": 0
            },
            {
                "type": "Link",
                "label": "Book Transaction",
                "link_type": "DocType",
                "link_to": "Book Transaction",
                "hidden": 0
            }
        ]
    })
    workspace.insert(ignore_permissions=True, ignore_if_duplicate=True)
    frappe.db.commit()
    print("Created workspace:", workspace.name)
