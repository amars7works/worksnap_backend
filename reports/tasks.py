from worksnaps_report.celery import app
from celery.decorators import task
from datetime import datetime, date, timedelta
from celery.utils.log import get_task_logger
from reports.views import get_all_users_daily_data
from reports.models import UserDailyReport

from reports_2.mailers import send_mails_to_employer

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

@task(name="reports.send_users_daily_reports_mail")
def send_mail_daily_report():
	try:
		today_date = date.today()
		daily_reports = UserDailyReport.objects.filter(created_at=today_date).values()

		subject = "Daily Reports"
		data = {}
		data['daily_reports'] = daily_reports

		template_directory = 'email/daily_reports.html'

		if daily_reports:
			send_mails_to_employer(
				subject,
				template_directory,
				data=data
			)

		logger.info("Sucessful")
	except Exception as e:
		logger.error(e,exc_info=True)
