# -*- coding: utf-8 -*-
# Copyright (c) 2024, Nikhil Saklani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

app_name = "library_management"
app_title = "Library Management"
app_publisher = "Nikhil Saklani"
app_description = "Library Management System built on Frappe/ERPNext"
app_email = "nikhilsaklani@example.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/library_management/css/library_management.css"
# app_include_js = "/assets/library_management/js/library_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/library_management/css/library_management.css"
# web_include_js = "/assets/library_management/js/library_management.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Fixtures
# --------
# export "Module Def" records that match "Library Management" to be checked in
fixtures = []

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------
# Runs mark_overdue_transactions every day to flag past-due book issues.

scheduler_events = {
	"daily": [
		"library_management.tasks.mark_overdue_transactions"
	]
}
