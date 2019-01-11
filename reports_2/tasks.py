from worksnaps_report.celery import app
from celery.decorators import task
from datetime import datetime
from celery.utils.log import get_task_logger
from reports_2.calculation_helper.py import add_remaining_leaves
logger = get_task_logger(__name__)

@task(name="reports_2.update_employee_leaves")
def get_day_data():
	try:
		today_ist = datetime.now()
		add_remaining_leaves(
		from_date=0,to_date=0,year=str(today_ist.year),month=str(today_ist.month),user_name='all')
	except Exception as e:
		logger.error(e,exc_info=True)

