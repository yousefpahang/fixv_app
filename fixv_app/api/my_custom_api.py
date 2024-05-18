import frappe
from frappe import _
from werkzeug.wrappers import Response



@frappe.whitelist()
def update_task_status(task_id):    
    # task_id = frappe.form_dict.get("task_id")
    new_status = frappe.form_dict.get("new_status")
    # new_status = "Open"
    # 

    try:

        # Fetch the task document
        task = frappe.get_doc('Task', task_id)
        if task:
            
            # Update the status
            task.status = new_status
            task.save()
            # return {'status': f'{task.status}'}
            # html_code = f"{task.status}"
            # return Response(html_code, content_type='text/html')

            # Send a success response
            # return {'message': _('Task status updated successfully'), 'status': 'success'}
    except Exception as e:
        # Handle exceptions and send an error response
        frappe.log_error(frappe.get_traceback(), 'update_task_status failed')
        return {'message': str(e), 'status': 'error'}
    # return f"Task ID : {task_id} new_status: {new_status}"


@frappe.whitelist()
def tasks_list():
	tasks_list_html = frappe.render_template("templates/includes/task_list.html") 
	return Response(tasks_list_html)