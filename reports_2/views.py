from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from reports_2.models import ApplyLeave
from reports_2.serializer import applyleaveserializer
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime,date
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from django.http import JsonResponse,HttpResponse
from worksnaps_report import settings
from django.core.mail import get_connection, EmailMultiAlternatives, send_mail
from reports.models import UserDailyReport
from reports.views import store_daily_report

class ApplyLeaveView(generics.CreateAPIView):
	permission_classes = (IsAuthenticated,)		
	serializer_class = applyleaveserializer
	
	def post(self,request):
	    serializer = applyleaveserializer(data = request.data)
	    if serializer.is_valid():
	        serializer.save()
	        return Response(serializer.data, status=status.HTTP_201_CREATED)
	    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class leave_details(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = applyleaveserializer

	# def get_queryset(self):
	# 	user = self.request.user
	# 	local_time = datetime.now()
	# 	return ApplyLeave.objects.filter(leave_start_date__gte=local_time,leave_status=False,user=user)
	def get_queryset(self):
		user = self.request.user
		if user.is_superuser:
			get_all_details = ApplyLeave.objects.all()
			return get_all_details

	def get(self,request,*args,**kwargs):
		get_data = self.get_queryset()
		serializer = applyleaveserializer(get_data, many=True)
		data = serializer.data[:]
		return Response(data, status=status.HTTP_200_OK)

	
	def get_object(self, id):
		try:
			return ApplyLeave.objects.get(id=id)
		except ApplyLeave.DoesNotExist:
			raise Http404

	def put(self, request):
		user = request.user
		if user.is_superuser:
			instance_id = request.data.get('id')
			user = self.get_object(instance_id)
			serializer = applyleaveserializer(instance=user, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, format=None):
		instance_id = request.data.get('id')
		leave_cancel = self.get_object(instance_id)
		leave_cancel.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

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
	obj=UserDailyReport.objects.filter(cretaed_at=date.today())
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
		msg=msg.format(a[u.username]['username'],a[u.username]['what_was_done_this_day'],a[u.username]['what_is_your_plan_for_the_next_day'])
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