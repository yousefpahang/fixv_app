import frappe

def get_project_permission_query(user):
    roles = frappe.get_roles(user)
    
    if "System Manager" in roles:
        condition = ""
    elif "Sales User" in roles:
        condition = """
            (
                `tabProject`.owner = {user}
                OR `tabProject`.project_owner = {user}
                OR `tabProject`.name IN (
                    SELECT parent FROM `tabToDo`
                    WHERE reference_type = 'Project'
                    AND status = 'Open'
                    AND allocated_to = {user}
                )
            )
        """.format(user=frappe.db.escape(user))
    else:
        condition = "1 = 2"
    
    return condition
