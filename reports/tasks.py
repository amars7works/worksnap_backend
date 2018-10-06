from worksnaps_report.celery import app
from celery.decorators import task
from datetime import datetime, timedelta
from celery.utils.log import get_task_logger
from reports.views import get_all_users_daily_data
logger = get_task_logger(__name__)

@task(name="reports.get_users_data")
def get_day_data():
	try:
		today_ist = datetime.now()
		yesterday = (today_ist - timedelta(days=1))
		day_before_yesterday = (yesterday - timedelta(days=1))
		get_all_users_daily_data(day_before_yesterday,yesterday)
	except Exception as e:
		logger.error(e,exc_info=True)
