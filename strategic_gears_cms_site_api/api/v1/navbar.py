import frappe
from frappe.utils.password import check_password

from strategic_gears_cms_site_api.utils import error_response, success_response, translate_keys


@frappe.whitelist(allow_guest=True)
def get_navbar_data(kwargs):
	try:
		user_language = kwargs.get("language")
		parent_categories = frappe.get_all(
			"Category",
			filters={"is_group": 1},
			fields=[
				"category_name",
				"label",
				"custom_url",
				"sequence",
				"slug",
				"redirect_to_external_website",
			],
			order_by="sequence",
		)

		navbar_data = []

		for category in parent_categories:
			parent = None
			navbar_item = {
				"name": category.category_name,
				"label": category.label,
				"url": prepare_url(
					category.slug, parent, category.redirect_to_external_website, category.custom_url
				),
				"seq": category.sequence,
				"slug": category.slug,
				"navbar_values": [],
			}

			child_categories = frappe.get_all(
				"Category",
				filters={"parent_category": category.category_name},
				fields=["category_name", "label", "custom_url", "sequence", "slug"],
				order_by="sequence",
			)

			for child_category in child_categories:
				if user_language == "ar" and child_category.label == "Corporate News":
					continue
				child_navbar_item = {
					"name": child_category.category_name,
					"label": child_category.label,
					"url": prepare_url(child_category.slug, category.slug, None, None),
					"seq": child_category.sequence,
					"slug": child_category.slug,
					"navbar_values": [],
				}
				navbar_item["navbar_values"].append(child_navbar_item)

			navbar_data.append(navbar_item)
		translated_data = translate_keys(navbar_data, user_language)
		return success_response(data=translated_data)
	except Exception as e:
		frappe.logger("Navbar").exception(e)
		return error_response(e)


def prepare_url(prefix, parent=None, redirect_to_external_website=None, custom_url=None):
	if parent:
		return f"/{parent}/{prefix}"
	elif redirect_to_external_website and custom_url:
		return custom_url
	elif prefix:
		return f"/{prefix}"
	else:
		return ""
