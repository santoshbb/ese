# -*- coding: utf-8 -*-
# Copyright (c) 2017, VHRS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import json
import frappe
import time
from datetime import datetime, timedelta
from frappe.utils.data import today, get_timestamp, formatdate
from werkzeug.wrappers import Response
from frappe.core.doctype.sms_settings.sms_settings import send_sms



@frappe.whitelist(allow_guest=True)
def attendance():
    # restrict request from list of IP addresses
    # create the custom response
    response = Response()
    response.mimetype = 'text/plain'
    response.charset = 'utf-8'
    response.data = "ok"
    try:
        userid = frappe.form_dict.get("userid")
        employee = frappe.db.get_value("Employee", {
            "biometric_id": userid, 'status': 'Active'})
        if employee:
            date = time.strftime("%Y-%m-%d", time.gmtime(
                int(frappe.form_dict.get("att_time"))))
            name, company = frappe.db.get_value(
                "Employee", employee, ["employee_name", "company"])
            attendance_id = frappe.db.get_value("Attendance", {
                "employee": employee, "attendance_date": date})
            is_leave = check_leave_record(employee, date)
            if is_leave == 'On Leave':
                attendance = frappe.new_doc("Attendance")
                in_time = time.strftime("%H:%M:%S", time.gmtime(
                    int(frappe.form_dict.get("att_time"))))
                attendance.update({
                    "employee": employee,
                    "employee_name": name,
                    "attendance_date": date,
                    "status": "On Leave",
                    "in_time": "00:00:00",
                    "out_time": "00:00:00",
                    "company": company
                })
                attendance.save(ignore_permissions=True)
                attendance.submit()
                frappe.db.commit()
                return response
            else:
                if attendance_id:
                    attendance = frappe.get_doc("Attendance", attendance_id)
                    out_time = time.strftime("%H:%M:%S", time.gmtime(
                        int(frappe.form_dict.get("att_time"))))
                    if not attendance.in_time:
                        attendance.in_time = out_time
                    else:
                        times = [out_time, attendance.in_time]
                        attendance.out_time = max(times)
                        attendance.in_time = min(times)
                    send_present_alert(employee,name,attendance.in_time,date,out_time)
                    attendance.db_update()
                    frappe.db.commit()
                    # return employee,name,attendance.in_time,date,out_time
                    
                    return response
                else:
                    attendance = frappe.new_doc("Attendance")
                    in_time = time.strftime("%H:%M:%S", time.gmtime(
                        int(frappe.form_dict.get("att_time"))))
                    attendance.update({
                        "employee": employee,
                        "employee_name": name,
                        "attendance_date": date,
                        "status": "Present",
                        "in_time": in_time,
                        "company": company
                    })
                    attendance.save(ignore_permissions=True)
                    attendance.submit()
                    frappe.db.commit()
                    send_present_alert(employee, name, in_time, date)
                    return response
        else:
            employee = frappe.form_dict.get("userid")
            date = time.strftime("%Y-%m-%d", time.gmtime(
                int(frappe.form_dict.get("att_time"))))
            ure_id = frappe.db.get_value("Unregistered Employee", {
                "employee": employee, "attendance_date": date})
            if ure_id:
                attendance = frappe.get_doc(
                    "Unregistered Employee", ure_id)
                out_time = time.strftime("%H:%M:%S", time.gmtime(
                    int(frappe.form_dict.get("att_time"))))
                times = [out_time, attendance.in_time]
                attendance.out_time = max(times)
                attendance.in_time = min(times)
                attendance.db_update()
                frappe.db.commit()
            else:
                attendance = frappe.new_doc("Unregistered Employee")
                in_time = time.strftime("%H:%M:%S", time.gmtime(
                    int(frappe.form_dict.get("att_time"))))
                attendance.update({
                    "employee": employee,
                    "attendance_date": date,
                    "stgid": frappe.form_dict.get("stgid"),
                    "in_time": in_time,
                })
                attendance.save(ignore_permissions=True)
                frappe.db.commit()
            return response
    except frappe.ValidationError as e:
        log_error("ValidationError", e)
        return response


def log_error(method, message):
    # employee = message["userid"]
    message = frappe.utils.cstr(message) + "\n" if message else ""
    d = frappe.new_doc("Error Log")
    d.method = method
    d.error = message
    d.insert(ignore_permissions=True)


def check_leave_record(employee, date):
    leave_record = frappe.db.sql("""select leave_type, half_day from `tabLeave Application`
    where employee = %s and %s between from_date and to_date and status = 'Approved'
    and docstatus = 1""", (employee, date), as_dict=True)
    if leave_record:
        if leave_record[0].half_day:
            status = 'Half Day'
        else:
            status = 'On Leave'
            leave_type = leave_record[0].leave_type

        return status

# def test_sms():
    # send_present_alert('EMP/0001', 'Ahmed', '08:13:47','08:13:47','08:13:47')

def send_present_alert(employee, name, in_time,date,out_time):
    recipients = frappe.get_value("Employee", employee, "cell_number")
    if recipients:
        if not in_time:
            in_time ="NIL"
        if not out_time:
            out_time = "NIL"    
        message="""Attendance Alert for %s
        Dear %s,
        Info:
        In Time:%s 
        Out Time:%s
        ESE ERP""" % (formatdate(date),name, in_time,out_time)
        rcv = []
        rcv.append(recipients)
        sender = 'ESE ERP SYS'
        send_sms(rcv, message,sender_name=sender)
