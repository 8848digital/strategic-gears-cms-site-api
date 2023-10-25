import frappe
from strategic_gears_cms_site_api.utils import success_response, error_response

@frappe.whitelist(allow_guest=True)
def get_service_list(kwargs):
    try:
        services = frappe.get_list("Services Master",pluck="name",order_by = 'sequence')
        banner=[]
        data = []
        details = []
        service_list=[]
        for service in services:
            banner = frappe.get_list("Banner",filters={"name":service},fields=["banner_name","banner_image"])
            for b in banner:
                banner_data = b
            service_details_list = frappe.get_all("Service Details",filters={"parent":service},pluck="service_detail",order_by = 'sequence')
            service_detail = []
            for service_details in service_details_list:
                get_service_details = frappe.get_all("Service Details Master",filters={"name":service_details},fields=["heading","description"])
                service_detail.append(get_service_details[0])
            service_desc = frappe.get_list("Services Master",filters={"name":service},pluck="description",order_by = 'sequence')
            for service in service_desc:
                desc = service
            details = {"banner_data":banner_data,"description":desc,"services_list":service_detail}
           
            data.append(details)
        return success_response(data)
    except Exception as e:
        frappe.logger("Service_Details").exception(e)
        return error_response(e)
    
@frappe.whitelist(allow_guest=True)
def get_service_details(kwargs):
    try:
        # Check if the 'name' parameter is provided in kwargs
        if 'name' not in kwargs:
            return error_response("Name parameter is missing")

        service_name = kwargs.get('name')

        # Retrieve specific service details
        banner = frappe.get_list("Banner", filters={"name": service_name}, fields=["banner_name", "banner_image"])
        banner_data = banner[0] if banner else {}

        service_desc = frappe.get_list("Services Master", filters={"name": service_name}, pluck="description",order_by = 'sequence')
        desc = service_desc[0] if service_desc else ""

        service_details_list = frappe.get_all("Service Details", filters={"parent": service_name}, pluck="service_detail",order_by = 'sequence')
        service_detail = []

        for service_details in service_details_list:
            get_service_details = frappe.get_all("Service Details Master", filters={"name": service_details}, fields=["heading", "description"])
            service_detail.append(get_service_details[0])

        details = {"banner_data": banner_data, "description": desc, "services_list": service_detail}

        return success_response(details)
    except Exception as e:
        frappe.logger("Specific_Service_Details").exception(e)
        return error_response(e)