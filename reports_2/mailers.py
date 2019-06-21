from reports_2.models import ApplyLeave
from reports.models import UserDailyReport
from django.core.mail import get_connection, \
								EmailMultiAlternatives, \
								send_mail, \
								EmailMessage

from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime,date, timedelta
from reports.serializers import UsersSummaryReportSerializers,\
								UserListSerializers
from reports.models import UserDailyReport, UsersSummaryReport, UsersList,TotalLeaves,ProjectsList
from xlsxwriter.workbook import Workbook


def send_mails_to_employer(subject, template_directory, username="Admin", data=None, from_email=None):
	from_email = settings.EMAIL_HOST_USER
	data['username'] = username
	data['employer_name'] = settings.EMPLOYER_NAME
	subject_mail = subject.format(username)

	html_content = render_to_string(template_directory, data)

	request_mail = EmailMessage(
			subject_mail, 
			html_content,
			"S7works Admin <{}>".format(from_email), 
			settings.EMPLOYER_EMAIL,
			bcc = settings.MANAGER_EMAIL_PROJECT_ONE,
			cc = settings.MANAGER_EMAIL_PROJECT_TWO
		)
	request_mail.content_subtype = "html"
	request_mail.send()

def send_mails_to_owner(template_directory, username="Admin", from_email=None):
	
	from_email = settings.EMAIL_HOST_USER
	date_yesterday = str(date.today() - timedelta(days = 1))
	data = {'date': '',
			'recipent': ''
			}
	data['date'] = date_yesterday
	data['recipent'] = username

	subject_mail = "Daily Report Employee status for {}".format(date_yesterday)

	html_content = render_to_string(template_directory, data)

	request_mail = EmailMessage(
			subject_mail, 
			html_content,
			"S7works Admin <{}>".format(from_email), 
			settings.EMPLOYER_EMAIL,
			bcc = settings.MANAGER_EMAIL_PROJECT_ONE,
			cc = settings.MANAGER_EMAIL_PROJECT_TWO
		)
	request_mail.content_subtype = "html"
	request_mail.attach('dailyReportCount.xlsx',dailyReportEmployeeCount())
	request_mail.send()

def dailyReportEmployeeCount():
		yesterday = str(date.today() - timedelta(days = 1))
		yesterday = '2019-04-30'
		get_data = UsersSummaryReport.objects.filter(date=yesterday)

		serializer = UsersSummaryReportSerializers(get_data, many=True)
		presentUser = []
		for serializerdata in serializer.data:
			presentUser.append(serializerdata['user_name'])

		presentUser = list(dict.fromkeys(presentUser))
		submittedUser = []
		notSubmittedUser = []
		daily_report_yesterday = UserDailyReport.objects.filter(created_at='2019-04-30')#str(date.today() - timedelta(days = 1)))
		
		reportPeople = [user.username for user in daily_report_yesterday]

		response = []
		for user in presentUser:
			if user in reportPeople:
				submittedUser.append(user)
			else:
				notSubmittedUser.append(user)


		row_data = 0
		column_data = 0

		response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		response['Content-Disposition'] = "attachment; filename=DailyReportCount.xlsx"
		book = Workbook(response,{'in_memory': True})

		work_sheet = book.add_worksheet('dailyReportCount {}'.format(str(date.today() - timedelta(days = 1))))
		cell_format = book.add_format()
		cell_format.set_bold(True)
		cell_format.set_bg_color('#38EA3E')
		cell_format.set_align('center')
		cell_format.set_font_size()
		work_sheet.write(row_data,column_data,'Employee (Submitted)',cell_format)
		cell_format.set_bold(False)
		row_data += 1
		for user in submittedUser:
			work_sheet.write(row_data,column_data,user)
			row_data += 1

		column_data = 1
		row_data = 0
		cell_format_notsub = book.add_format()
		cell_format_notsub.set_bold(True)
		cell_format_notsub.set_bg_color('#E52802')
		cell_format_notsub.set_align('center')
		cell_format_notsub.set_font_size()
		work_sheet.write(row_data,column_data,'Employee (Not Submitted)',cell_format_notsub)
		cell_format.set_bold(False)
		row_data += 1
		for user in notSubmittedUser:
			work_sheet.write(row_data,column_data,user)
			row_data += 1

		work_sheet.set_column(0, 1, 40)
		
		book.close()	
		
		return response['Content-Disposition']
# # @send_leave_request
# def apply_leave_request():
# 	today = date.today()
# 	obj=ApplyLeave.objects.filter(created_at=today)
# 	if obj:
# 		msg="request {}".format(date.today())
# 		msg=msg+'''
# 			http://localhost:8000/biggboss/reports_2/applyleave/
# 		'''
			
# 		return requestleavemail(msg)
# 	else:
# 		print("no data")


# def requestleavemail(msg):
# 	subject="request {}".format(date.today())
# 	from_email = settings.EMAIL_HOST_USER
# 	to = "sai@s7works.io"
# 	cc = "vikramp@s7works.io,supraja@s7works.io"
# 	rcpt = cc.split(",")  + [to]
# 	res = send_mail(subject,msg,from_email,rcpt)
# 	if(res==1):
# 		print("Mail sent successfully")
# 	else:
# 		print("Failed to send mail")
# 	return HttpResponse(msg)


# # @send_user_daily_report_mail
# def users_queryset():
# 	obj=UserDailyReport.objects.filter(created_at=date.today())
# 	filter_keys={'username','what_was_done_this_day','what_is_your_plan_for_the_next_day'}
# 	a={}
# 	msg="Daily Report {}".format(date.today())
# 	for u in obj:
# 		a[u.username]={key:value for key,value in u.__dict__.items() if key in filter_keys}
# 		msg=msg+'''
# 		user={},
# 		what was done this day={},
# 		what is your plan for the next day={}
# 		'''
# 		msg=msg.format(a[u.username]['username'],
# 					   a[u.username]['what_was_done_this_day'],
# 					   a[u.username]['what_is_your_plan_for_the_next_day'])
# 	return dailyreportsmail(msg)


# def dailyreportsmail(msg):
# 	subject="Daily Report {}".format(date.today())
# 	from_email = settings.EMAIL_HOST_USER
# 	to="gowtham@s7works.io"
# 	res=send_mail(subject,msg,from_email,[to])
# 	if res==1:
# 		print("Mail sent successfully")
# 	else:
# 		print("Failed to send mail")
# 	return HttpResponse(msg)