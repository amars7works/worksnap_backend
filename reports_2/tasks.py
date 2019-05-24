from worksnaps_report.celery import app
from celery.decorators import task
from datetime import datetime
from celery.utils.log import get_task_logger
from reports_2.calculation_helper import add_remaining_leaves

from django.template import Context
from datetime import datetime,date

from reports_2.mailers import send_mails_to_employer

logger = get_task_logger(__name__)

@task(name="reports_2.update_employee_leaves")
def get_day_data():
	try:
		today_ist = datetime.now()
		add_remaining_leaves(
		from_date=0,to_date=0,year=str(today_ist.year),month=str(today_ist.month),user_name='all')
	except Exception as e:
		logger.error(e,exc_info=True)

@task(name="reports.send_employee_request_mail")
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
