from worksnaps_report.celery import app
from celery.decorators import task
from datetime import datetime, date, timedelta
from celery.utils.log import get_task_logger

from time_entry.views import get_time_blocks, get_time_entries
from time_entry.modeks import TimeEntry

logger = get_task_logger(__name__)

@task(name="reports.get_time_entries")
def get_time_entries(project_id, user_id, from_timestamp, to_timestamp):
	"""
		Tasks to get time entries for each user.
	"""
	try:
		type = 'online'
		time_blocks = get_time_blocks()
		time_entries = get_time_entries(project_id, user_id, from_timestamp, to_timestamp)


		print(time_entries.text)
		# logic set 6 time interval as discussed

		logger.info("Time entries successfully pulled")
	except Exception as e:
		logger.error(e, exc_info=True)
