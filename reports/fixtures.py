from django.contrib.auth.models import User

from reports.models import *


def add_project_id_to_summary_reports():
	'''
		Adding project id to summary reports
	'''
	reports = UsersSummaryReport.objects.all()
	for report in reports:
		try:
			report.project_id = ProjectsList.objects.filter(project_name=report.project_name)[0].project_id
			report.save()
		except Exception as e:
			if report.project_name == 'Slickdeals':
				report.project_id = '54697'
				report.save()
			elif report.project_name == 'siorna medical':
				report.project_id = '60222'
				report.save()
			print('error', e, 'project_name', report.project_name)

	return True


def change_usernames_in_corresponding_tables():
	'''
		Changing usernames in all tables.
	'''
	users = UsersList.objects.all()

	try:
		for user in users:
			uu = User.objects.get(email=user.user_email)

			summary_report = UsersSummaryReport.objects.filter(user_id=user.user_id)
			reports = map(lambda report: username_change(report, user.user_login_as), summary_report)
			list(reports)

			daily_report = UserDailyReport.objects.filter(username=uu.username)
			daily_reports = map(lambda report: report_username_change(report, user.user_login_as), daily_report)
			list(daily_reports)

			try:
				profile = UserProfile.objects.get(user_name=uu.username)
				username_change(profile, user.user_login_as)
			except:
				print("profile error")

			uu.username = user.user_login_as
			uu.save

	except Exception as e:
		print('error -->', e)

def username_change(report, username):
	report.user_name = username
	report.save()

def report_username_change(report, username):
	report.username = username
	report.save()
