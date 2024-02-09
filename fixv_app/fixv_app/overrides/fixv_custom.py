from frappe import throw,_
from frappe.utils import getdate, today

from erpnext.setup.doctype.employee.employee import Employee


class CustomEmployee(Employee):
    def on_update(self):
        if self.final_confirmation_date and getdate(self.final_confirmation_date) < getdate(today()):
            throw(_("Confirmation date cannot be lesser than today."))