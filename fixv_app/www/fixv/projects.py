import frappe
from datetime import datetime

def get_context(context):
    if not frappe.session.user or frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    else:
        # Check for user role
        if "System Manager" not in frappe.get_roles(frappe.session.user):
            frappe.throw("You do not have permission to access this page.", frappe.PermissionError)   
        else:    
            # Fetch projects and their associated tasks
            context.projects = frappe.get_all('Project', 
                                      fields=['name', 'project_name', 'status', "customer",
                                               "custom_whatsapp", "creation", "expected_start_date",
                                                 "expected_end_date", "percent_complete", "custom_contact_mobile",
                                                  "priority","custom_expected_revenue", ])
            # frappe.log_error(projects, 'Projects Data')  # Log projects to check if they are fetched
        

            for project in context.projects:
                project['tasks'] = frappe.get_all('Task', filters={'project': project.name}, fields=["name", "subject", "status", "project", "completed_on", "expected_time", "exp_start_date", "exp_end_date"])
                project['tags'] = get_project_tags(project.name)
                project['days_ago'] = get_relative_date(project.creation)
                project['assignees'] = get_assignees(project.name)



def get_project_tags(project_id):
    # Fetch tags related to the project
    return [d.tag for d in frappe.get_list('Tag Link', filters={'document_type': 'Project', 'document_name': project_id}, fields=['tag'])]



def get_relative_date(creation):
    """Calculate how many days ago the project was created, assuming 'creation' is a datetime object."""
    today = datetime.now().date()  # Ensure we're comparing dates, not datetime
    creation_date = creation.date()  # Convert datetime to date for comparison
    delta = today - creation_date

    if delta.days == 0:
        return "Today"
    elif delta.days == 1:
        return "Yesterday"
    else:
        return f"{delta.days} days ago"
    

def get_assignees(project_name):
    """Fetch a list of users assigned to a project."""
    assignees = frappe.get_list('ToDo', 
                                filters={'reference_type': 'Project', 'reference_name': project_name, 'status': 'Open'}, 
                                fields=['owner', 'assigned_by', 'allocated_to'])
    return assignees