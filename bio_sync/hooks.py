# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "bio_sync"
app_title = "Bio Sync"
app_publisher = "Sammish"
app_description = "Attendance Synchronization"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "sammish.thundiyil@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/bio_sync/css/bio_sync.css"
# app_include_js = "/assets/bio_sync/js/bio_sync.js"

# include js, css files in header of web template
# web_include_css = "/assets/bio_sync/css/bio_sync.css"
# web_include_js = "/assets/bio_sync/js/bio_sync.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "bio_sync.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "bio_sync.install.before_install"
# after_install = "bio_sync.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "bio_sync.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

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

# scheduler_events = {
# 	"all": [
# 		"bio_sync.tasks.all"
# 	],
# 	"daily": [
# 		"bio_sync.tasks.daily"
# 	],
# 	"hourly": [
# 		"bio_sync.tasks.hourly"
# 	],
# 	"weekly": [
# 		"bio_sync.tasks.weekly"
# 	]
# 	"monthly": [
# 		"bio_sync.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "bio_sync.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "bio_sync.event.get_events"
# }

