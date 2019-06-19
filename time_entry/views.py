import time
import pytz
import base64
import requests
from datetime import datetime
from django.shortcuts import render

from django.contrib.auth.models import User

from reports.models import UsersList, UsersSummaryReport

# Create your views here.
def get_time_entries_data(project_id, user_id, from_timestamp, to_timestamp, type):
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
		'from_timestamp': from_timestamp,
		'to_timestamp': to_timestamp,
		'time_entry_type': type
	}
	request_data = requests.get( users_url,headers=headers,params=params )

	return request_data

def get_time_blocks():
	'''
                Time blocks
                10 - 11 AM  --> 36000 - 39600 secs
                12 - 1 PM   --> 43200 - 46800 secs
                3 - 4 PM    --> 54000 - 57600 secs
                5 - 6 PM    --> 61200 - 64800 secs
                8 - 9 PM    --> 72000 - 75600 secs
                10 - 11 PM  --> 79200 - 82800 secs
	'''
	time_blocks = [
		[36000, 39600],
                [43200, 46800],
                [54000, 57600],
                [61200, 64800],
                [72000, 75600],
                [79200, 82800],
	]
	return time_blocks
