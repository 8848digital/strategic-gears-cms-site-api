import frappe
from frappe.utils.password import check_password

from strategic_gears_cms_site_api.utils import error_response, success_response


def get_access_token(kwargs):
	try:
		usr = kwargs.get("usr")
		pwd = kwargs.get("pwd")
		access_api_token = {}
		try:
			check_password(usr, pwd)
		except Exception as e:
			return error_response(e)
		doc = frappe.get_doc("User", {"name": usr})
		api_key = doc.api_key
		api_secret = doc.get_password("api_secret")
		if api_key and api_secret:
			api_token = "token " + api_key + ":" + api_secret
			access_api_token = {"access_token": api_token}
		return success_response(data=access_api_token)
	except Exception as e:
		frappe.logger("Token").exception(e)
		return error_response(e)
