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
            project_id = frappe.form_dict.project_id
            if project_id:
                project = frappe.get_doc("Project", project_id)
                if project:
                    project_dict = project.as_dict()
                    context.project = project_dict
                    # Now you can add the 'tasks' key to the 'project_dict'
                    project_dict['tasks'] = frappe.get_all('Task', filters={'project': project.name}, fields=["name", "subject", "status", "project", "completed_on", "expected_time", "exp_start_date", "exp_end_date"])
                    project_dict['tags'] = get_project_tags(project.name)
                    project_dict['days_ago'] = get_relative_date(project.creation)
                    project_dict['assignees'] = get_assignees(project.name)
                    project_dict['tasks_status'] = get_task_status_options()

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

import frappe

def get_task_status_options():
    # Get the DocType for Task
    task_meta = frappe.get_meta('Task')

    # Fetch the options for the 'status' field
    status_options = task_meta.get_field('status').options.split('\n')

    return status_options



