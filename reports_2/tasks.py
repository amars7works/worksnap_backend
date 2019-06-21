from worksnaps_report.celery import app
from celery.decorators import task
from datetime import datetime
from celery.utils.log import get_task_logger
from reports_2.calculation_helper import add_remaining_leaves

from django.template import Context
from datetime import datetime,date

from reports_2.mailers import send_mails_to_employer, send_mails_to_owner

from celery.task.schedules import crontab
from celery.decorators import periodic_task

logger = get_task_logger(__name__)

@task(name="reports_2.update_employee_leaves")
def get_day_data():
	try:
		today_ist = datetime.now()
		add_remaining_leaves(
		from_date=0,to_date=0,year=str(today_ist.year),month=str(today_ist.month),user_name='all')
	except Exception as e:
		logger.error(e,exc_info=True)

@task(name="reports_2.send_employee_request_mail")
def send_requests_email_to_employer(data, from_email, username):
	"""
		Send email to employer when employee request a leave
		Async.
	"""
	try:
		subject = "S7works leave request from {}"
		template_directory = 'email/requests.html'
		
		send_mails_to_employer(
			subject, 
			template_directory, 
			from_email=from_email, 
			username=username, 
			data=data
		)
		
	except Exception as e:
		logger.error(e, exc_info=True)



@periodic_task(run_every=crontab(hour=0, minute=15, ))
def send_daily_report_count():

	"""
		Send email to the owner at 00:15 of previous days daily report's count
	"""

	print("daily report count email started")

	try:
		template_directory = 'email/dailyReportCount.html'

		send_mails_to_owner(template_directory)

	except Exception as e:
		logger.error(e, exc_info=True)

    





