import time
import pytz
from datetime import datetime
from django.shortcuts import render

from django.contrib.auth.models import User

from reports.models import UsersList, UsersSummaryReport
from time_entry.tasks import get_time_entries


def create_time_entries(from_date, to_date):
	'''
	Creates time entries in the database
	This can be used as a manual method to pull the data from the worksnaps server when needed.

	Args: From date, to date (format: "yyyy-mm-dd")
	returns: boolean
	'''
	tz = pytz.timezone('Asia/Kolkata') # timezone
	from_timestamp = int(time.mktime(datetime.strptime(from_date,
                                "%Y-%m-%d").astimezone(tz).timetuple())) # date to timestamp

	to_timestamp = int(time.mktime(datetime.strptime(to_date,
                                "%Y-%m-%d").astimezone(tz).timetuple()))

	users = UsersList.objects.all()
	for user in users:
		user_reports = UsersSummaryReport.objects.filter(user_id=user.user_id,
                                        date=from_date)
		user_projects = [user_report.project_id for user_report in user_reports]

		# Each call has to be sent to the celery using delay or apply async.
		celery_tasks = map(lambda project_id: get_time_entries.delay(project_id,
                                                                        user.user_id,
                                                                        from_timestamp,
									to_timestamp),
                                                                        user_projects)
		list(celery_tasks)

	return True
