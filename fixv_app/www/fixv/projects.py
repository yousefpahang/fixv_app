import frappe

def get_context(context):
    # Fetch projects and their associated tasks
    projects = frappe.get_all('Project', fields=['name', 'project_name', 'status', "customer", "custom_whatsapp", "creation", "expected_start_date", "expected_end_date", "percent_complete" ])
    # frappe.log_error(projects, 'Projects Data')  # Log projects to check if they are fetched
  

    for project in projects:
        project['tasks'] = frappe.get_all('Task', filters={'project': project.name}, fields=["name", "subject", "status", "project", "completed_on", "expected_time", "exp_start_date", "exp_end_date"])
        print("hello")
    context.projects = projects
    # context.my_tasks = my_tasks
    # print("yousef is Loading project.py for My Custom App")
