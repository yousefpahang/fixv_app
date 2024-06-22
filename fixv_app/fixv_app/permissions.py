import frappe

def get_project_permission_query(user):
    roles = frappe.get_roles(user)
    
    if "System Manager" in roles:
        condition = ""
    elif "Technician" in roles:
        print('\n\n testing new permission\n\n')
        condition = """(tabProject.owner = {user} OR (tabProject.custom_opportunity_owner = {user} ))""".format(user=frappe.db.escape(user))
        # condition = """(tabProject.custom_opportunity_owner = {user} )""".format(user=frappe.db.escape(user))
        # """(tabLead.owner = '{user}' or tabLead.lead_owner = '{user}')
        #  or (tabLead.name in (select tabLead.name from tabLead where (tabLead._assign = '["{user}"]' )))""".format(user=frappe.db.escape(user))

        # condition = """(tabProject.name in (select tabProject.name from tabProject where (tabProject._assign = '[{user}]' )) )""".format(user=frappe.db.escape(user))
        print(f'Condition:\n {condition}')
        # condition = "1 = 2"
    else:
        condition = "1 = 2"
    
    return condition


def get_quotation_permission_query(user):
    roles = frappe.get_roles(user)

    if "System Manager" in roles:
        condition = ""
    elif "Technician" in roles:
        condition = """
                   (
                       `tabQuotation`.owner = {user}
                       OR `tabQuotation`.name IN (
                           SELECT reference_name FROM `tabToDo`
                           WHERE reference_type = 'Quotation'
                           AND allocated_to = {user}
                       )
                   )
               """.format(user=frappe.db.escape(user))
    else:
        condition = "1 = 2"

    return condition
