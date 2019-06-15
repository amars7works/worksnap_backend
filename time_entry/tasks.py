import xml.etree.ElementTree as ET
import pytz

from worksnaps_report.celery import app
from celery.decorators import task
from datetime import datetime, date, timedelta
from celery.utils.log import get_task_logger


from time_entry.views import get_time_entries_data, get_time_blocks
from time_entry.models import TimeEntry



logger = get_task_logger(__name__)

@task(name="time_entry.store_time_entries")
def get_time_entries(project_id, user_id, from_timestamp, to_timestamp):
	"""
		Tasks to get time entries for each user.
	"""
	try:
		type = 'online'
		time_blocks = get_time_blocks()

		time_range_data = map(lambda time_block: save_time_entry(project_id,
										 user_id,
										 from_timestamp,
										 type, time_block), time_blocks)

		list(time_range_data)

		logger.info("Time entries successfully pulled")
	except Exception as e:
		logger.error(e, exc_info=True)


def save_time_entry(project_id, user_id, from_timestamp, type, time_block):
	try:
		from_time_range = int(from_timestamp) + int(time_block[0]) # Custom time range -> start time 
		to_time_range = int(from_timestamp) + int(time_block[1]) # Custom time range -> end time
		time_entries = get_time_entries_data(project_id, user_id, from_time_range, to_time_range, type)

		entry_xml_from_string = ET.fromstring(time_entries.text)

		for time_entry in entry_xml_from_string.findall('time_entry'):
			entry_id = time_entry.find('id').text
			type = time_entry.find('type').text
			fromtimestamp = convert_timestamp(time_entry.find('from_timestamp').text)
			logged_timestamp = convert_timestamp(time_entry.find('logged_timestamp').text)
			duration = time_entry.find('duration_in_minutes').text
			project_id = time_entry.find('project_id').text
			user_id =  time_entry.find('user_id').text
			user_ip = time_entry.find('user_ip').text
			activity_level = time_entry.find('activity_level').text

			TimeEntry.objects.create(entry_id=entry_id,
						 type=type,
						 from_timestamp=fromtimestamp,
						 logged_timestamp=logged_timestamp,
						 duration=duration,
						 project_id=project_id,
						 user_id=user_id,
						 user_ip=user_ip,
						 activity_level=activity_level)

	except Exception as e:
		print("Error", e)


def convert_timestamp(timestamp):
	"""
		Converts timestamp to readable date (IST)
	"""
	ist = pytz.timezone('Asia/Kolkata')

	utcdate = pytz.utc.localize(datetime.utcfromtimestamp(int(timestamp)))
	return ist.normalize(utcdate)

