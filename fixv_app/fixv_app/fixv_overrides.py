import frappe
from frappe.model.documeent import Document

class myBank(Document):
    def validate(self):
        if len(self.swift_number) < 11:
            frappe.msgprint("Swift number should be less than 11")