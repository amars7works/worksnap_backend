
from reports_2.models import ApplyLeave
from reports.models import UserDailyReport
from django.core.mail import get_connection, \
								EmailMultiAlternatives, \
								send_mail

from django.http import JsonResponse,HttpResponse

# @send_leave_request
def apply_leave_request():
	today = date.today()
	obj=ApplyLeave.objects.filter(created_at=today)
	if obj:
		msg="request {}".format(date.today())
		msg=msg+'''
			http://localhost:8000/biggboss/reports_2/applyleave/
		'''
			
		return requestleavemail(msg)
	else:
		print("no data")


def requestleavemail(msg):
	subject="request {}".format(date.today())
	from_email = settings.EMAIL_HOST_USER
	to = "sai@s7works.io"
	cc = "vikramp@s7works.io,supraja@s7works.io"
	rcpt = cc.split(",")  + [to]
	res = send_mail(subject,msg,from_email,rcpt)
	if(res==1):
		print("Mail sent successfully")
	else:
		print("Failed to send mail")
	return HttpResponse(msg)


# @send_user_daily_report_mail
def users_queryset():
	obj=UserDailyReport.objects.filter(created_at=date.today())
	filter_keys={'username','what_was_done_this_day','what_is_your_plan_for_the_next_day'}
	a={}
	msg="Daily Report {}".format(date.today())
	for u in obj:
		a[u.username]={key:value for key,value in u.__dict__.items() if key in filter_keys}
		msg=msg+'''
		user={},
		what was done this day={},
		what is your plan for the next day={}
		'''
		msg=msg.format(a[u.username]['username'],
					   a[u.username]['what_was_done_this_day'],
					   a[u.username]['what_is_your_plan_for_the_next_day'])
	return dailyreportsmail(msg)


def dailyreportsmail(msg):
	subject="Daily Report {}".format(date.today())
	from_email = settings.EMAIL_HOST_USER
	to="gowtham@s7works.io"
	res=send_mail(subject,msg,from_email,[to])
	if res==1:
		print("Mail sent successfully")
	else:
		print("Failed to send mail")
	return HttpResponse(msg)