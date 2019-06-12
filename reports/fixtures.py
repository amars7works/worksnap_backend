from reports.models import *


def add_project_id_to_summary_reports():
	"""
		Adding project id to summary reports
	"""
	reports = UsersSummaryReport.objects.all()
	for report in reports:
		try:
			report.project_id = ProjectsList.objects.filter(project_name=report.project_name)[0].project_id
			report.save()
		except Exception as e:
			if report.project_name == "Slickdeals":
				report.project_id = "54697"
				report.save()
			elif report.project_name == "siorna medical":
				report.project_id = "60222"
				report.save()
			print("error", e, "project_name", report.project_name)

	return True

