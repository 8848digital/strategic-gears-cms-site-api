import frappe

from strategic_gears_cms_site_api.utils import error_response, success_response, translate_keys


@frappe.whitelist(allow_guest=True)
def get_team_member(kwargs):
	try:
		user_language = kwargs.get("language")
		banner = frappe.get_all(
			"Banner",
			filters={"banner_name": "OUR TEAM"},
			fields=[
				"banner_name",
				"banner_text",
				"banner_background_image",
				"banner_height",
				"banner_font_size",
				"banner_alignment",
			],
		)
		banner_data = banner[0]

		team_details = frappe.get_all(
			"Team Details",
			filters={"parent": "Our Team"},
			fields=["team_member_name", "sequence"],
			order_by="sequence",
		)
		team_member = []

		for single_member in team_details:
			team_member_dict = {}

			speciality = frappe.get_all(
				"Speciality Details",
				filters={"parent": single_member.team_member_name},
				pluck="speciality_name",
			)

			doc = frappe.get_doc("Team Member", single_member.team_member_name)
			team_member_image = doc.image
			team_member_name = doc.employee_name
			team_member_designation = doc.designation
			team_member_description = doc.description

			team_member_dict = {
				"name": single_member.team_member_name,
				"sequence": single_member.sequence,
				"team_member_image": team_member_image,
				"team_member_name": team_member_name,
				"team_member_designation": team_member_designation,
				"team_member_speciality": speciality,
				"team_member_description": team_member_description,
			}
			team_member.append(team_member_dict)

		data = {"banner_data": banner_data, "team_members_data": team_member}
		translated_data = translate_keys(data, user_language)
		return success_response(data=translated_data)
	except Exception as e:
		frappe.logger("Team").exception(e)
		return error_response(e)


@frappe.whitelist(allow_guest=True)
def home_page_team_member(kwargs):
	try:
		user_language = kwargs.get("language")
		team_details = frappe.get_all(
			"Team Details",
			filters={"parent": "Our Team", "show_on_website": 1},
			fields=["team_member_name", "sequence"],
			order_by="sequence",
		)
		team_members_data = []

		for member in team_details:
			team_member = frappe.get_list(
				"Team Member",
				filters={"name": member.team_member_name},
				fields=["employee_name", "designation", "image"],
			)
			translated_data = translate_keys(team_member, user_language)
			team_members_data.extend(translated_data)

		return success_response(data=team_members_data)

	except Exception as e:
		frappe.logger("Team").exception(e)
		return error_response(e)
