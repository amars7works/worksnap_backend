from worksnaps_report.celery import app
from celery.decorators import task
from datetime import datetime
from celery.utils.log import get_task_logger
from reports_2.calculation_helper import add_remaining_leaves
from .mailers import users_queryset

from django.core.mail import get_connection, \
								EmailMultiAlternatives, \
								send_mail, \
								EmailMessage
from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string

logger = get_task_logger(__name__)

@task(name="reports_2.update_employee_leaves")
def get_day_data():
	try:
		today_ist = datetime.now()
		add_remaining_leaves(
		from_date=0,to_date=0,year=str(today_ist.year),month=str(today_ist.month),user_name='all')
	except Exception as e:
		logger.error(e,exc_info=True)

# @task(name="reports_2.request_leave_mail")
# def send_mail_leave_request():
# 		try:
# 			apply_leave_request()
# 			logger.info("sucessful")
# 		except Exception as e:
# 			logger.error(e,exc_info=True)

@task(name="reports_2.send_employee_request_mail")
def send_requests_email_to_employer(data, from_email, username):
	"""
		Send email to employer when employee requests from frontend
		Async.
	"""
	try:
		from_email = settings.EMAIL_HOST_USER
		data['username'] = username
		data['employer_name'] = settings.EMPLOYER_NAME
		# context_data = Context(data)

		html_content = render_to_string('email/requests.html', data)

		request_mail = EmailMessage(
			"S7works leave request from {}".format(username), 
			html_content, 
			"S7works Admin <{}>".format(from_email), 
			settings.EMPLOYER_EMAIL,
			bcc = settings.MANAGER_EMAIL_PROJECT_ONE,
			cc = settings.MANAGER_EMAIL_PROJECT_TWO
		)
		print(data)
		print(EmailMessage)
		request_mail.content_subtype = "html"
		request_mail.send()

	except Exception as e:
		logger.error(e, exc_info=True)

@task(name="reports_2.send_users_daily_reports_mail")
def send_mail_daily_report():
		try:
			users_queryset()
			logger.info("sucessful")
		except Exception as e:
			logger.error(e,exc_info=True)
