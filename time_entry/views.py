import time
import pytz
from datetime import datetime
from django.shortcuts import render

from django.contrib.auth.models import User

from reports.models import UsersList, UsersSummaryReport
from time_entry.tasks import get_time_entries

# Create your views here.
def get_time_entries(project_id, user_id, from_timestamp, to_timestamp):
	'''
		This function will work like get the user data from worksnaps
		Args: Worksnaps user id, From date and To date
		Return: XML data for given user id
	'''
	user_ids = user_id
	token = '23Mh2bkhQkUoqlU0KDfpVaYg9wXXsSgHr7YKdSm8'
	users_url = "https://api.worksnaps.com:443/api/projects/{}/users/{}/time_entries.xml?".format(project_id,user_id)

	client_token = '{}:{}'.format(token,"ignored").encode()

	headers = {
		'Authorization': 'Basic'+' '+base64.b64encode(client_token).decode('utf-8'),
		'Accept': 'application/json',
		'Content-Type': 'application/json',
	}
	params = {
		'from_timestamp': start_timestamp,
		'to_timestamp': end_timestamp
	}
	request_data = requests.get( users_url,headers=headers,params=params )

	return request_data

def create_time_entries(from_date, to_date):
	tz = pytz.timezone('Asia/Kolkata')
	from_timestamp = int(time.mktime(datetime.strptime(from_date,
				"%Y-%m-%d").astimezone(tz).timetuple()))

	to_timestamp = int(time.mktime(datetime.strptime(to_date,
                                "%Y-%m-%d").astimezone(tz).timetuple()))

	users = UsersList.objects.all()
	for user in users:
		user_reports = UsersSummaryReport.objects.filter(user_id=user.user_id,
					date=from_date)
		user_projects = [user_report.project_id for user_report in user_reports]

		# Each call has to be sent to the celery using delay or apply async.
		for project_id in user_projects:
			get_time_entries(project_id, user.user_id, from_timestamp, to_timestamp)

	return True


def get_time_blocks():
	"""
                Time blocks
                10 - 11 AM  --> 36000 - 39600
                12 - 1 PM   --> 43200 - 46800
                3 - 4 PM    --> 54000 - 57600
                5 - 6 PM    --> 61200 - 64800
                8 - 9 PM    --> 72000 - 75600
                10 - 11 PM  --> 79200 - 82800
        """
        time_blocks = [
                [36000, 39600]
                [43200, 46800]
                [54000, 57600]
                [61200, 64800]
                [72000, 75600]
                [79200, 82800]
        ]
	return time_blocks
