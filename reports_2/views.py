from django.shortcuts import render

# Create your views here.
import ast
import json
from django.contrib.auth.models import User
from django.core import serializers
from rest_framework.response import Response
from reports_2.models import ApplyLeave,WorkFromHome
from reports_2.serializer import applyleaveserializer, \
									userserializer,\
									UserDailyReportSerializers									
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime,date
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from django.http import JsonResponse,HttpResponse
from django.conf import settings
from django.core.mail import get_connection, \
								EmailMultiAlternatives, \
								send_mail
from reports.models import UserDailyReport,\
							UsersSummaryReport,\
							UsersList,\
							TotalLeaves
from reports.serializers import UsersSummaryReportSerializers,\
								UserListSerializers
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from reports_2.tasks import send_requests_email_to_employer


class ApplyLeaveView(generics.CreateAPIView):
	permission_classes = (IsAuthenticated,)		
	serializer_class = applyleaveserializer
	
	def post(self,request):
		user_id = request.user.id
		tmp_leave_data = request.data
		tmp_leave_data['user'] = user_id
		tmp_leave_data['created_at'] = date.today()
		
		# Send mail to employer
		send_requests_email_to_employer.delay(tmp_leave_data, request.user.email, request.user.username)

		serializer = applyleaveserializer(data = tmp_leave_data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class leave_details(generics.RetrieveUpdateDestroyAPIView):
	""" only admin can get all employees leave details
	and update leave has been approved or rejected."""
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
		total_leaves = TotalLeaves.objects.all()
		remaining_leaves = {}
		for single_data in total_leaves:
			tests = ast.literal_eval(single_data.data).values()
			for i in tests:
				remaining_leaves[single_data.user.username] = i['accrued_leaves']
		for dt in serializer.data:
			user_obj=User.objects.get(id=dt['user'])
			dt['username'] =  user_obj.username
			dt['remainingleaves'] = remaining_leaves[user_obj.username]
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
			get_status = request.data.get('leave_status')
			if get_status:
				if serializer.is_valid():
					serializer.save()
					return Response(serializer.data)
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			return Response(get_status)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, format=None):
		instance_id = request.data.get('id')
		leave_cancel = self.get_object(instance_id)
		leave_cancel.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class Leave_Approved_List(generics.RetrieveUpdateDestroyAPIView):
	""" admin can approved list of the employees leave """
	permission_classes = (IsAuthenticated,)
	serializer_class = applyleaveserializer

	def get_queryset(self):
		user = self.request.user
		if user.is_superuser:
			local_time = date.today()
			lve_aprd_list = ApplyLeave.objects.filter(leave_status="Approved")
			return lve_aprd_list

	def get(self,request,*args,**kwargs):
		get_data = self.get_queryset()
		serializer = applyleaveserializer(get_data, many=True)
		for dt in serializer.data:
			user_obj=User.objects.get(id=dt['user'])
			dt['username'] =  user_obj.username
		data = serializer.data[:]
		return Response(data, status=status.HTTP_200_OK)

class Leave_Rejected_List(generics.RetrieveUpdateDestroyAPIView):
	""" admin can rejected list of the employees leave """
	permission_classes = (IsAuthenticated,)
	serializer_class = applyleaveserializer

	def get_queryset(self):
		user = self.request.user
		if user.is_superuser:
			leave_rejected_list = ApplyLeave.objects.filter(leave_status="Rejected")
			return leave_rejected_list

	def get(self,request,*args,**kwargs):
		get_data = self.get_queryset()
		serializer = applyleaveserializer(get_data, many=True)
		for dt in serializer.data:
			user_obj=User.objects.get(id=dt['user'])
			dt['username'] =  user_obj.username
		data = serializer.data[:]
		return Response(data, status=status.HTTP_200_OK)

# class emp_details(generics.RetrieveUpdateDestroyAPIView):
# 	serializer_class = userserializer
# 	""" list all employees details display into the admin panel """
# 	def get_queryset(self):
# 		user = self.request.user
# 		if user.is_superuser:
# 			get_all_details = User.objects.all()
# 			return get_all_details
# 	def get(self,request,*args,**kwargs):
# 		user = self.request.user
# 		get_data = self.get_queryset()
# 		serializer = userserializer(get_data, many=True)
# 		data = serializer.data[:]
# 		return Response(data, status=status.HTTP_200_OK)
		
def leavestatus(request):
	""" employee leave status response """
	get_details = ApplyLeave.objects.all()
	for status in get_details:
		leave_status = status.leave_status
		if leave_status == "Pending":
			return HttpResponse("Pending")
		elif leave_status == "Approved":
			return HttpResponse("Approved")
		else:
			return HttpResponse("Rejected")
	return HttpResponse(status)


class DailyReportView(generics.CreateAPIView):
	permission_classes = (IsAuthenticated,)		
	serializer_class = UserDailyReportSerializers

	def post(self,request):
		username = request.user.username
		temp_data = request.data
		temp_data['username'] = username
		temp_data['created_at'] = date.today()
		serializer = UserDailyReportSerializers(data = temp_data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class emp_list(generics.RetrieveUpdateDestroyAPIView):
	# """ get data from UserSummaryReport model,
	# 	filter data by using date,
	# 	total present/leave employees list on a particular date
	# """
	permission_classes = (IsAuthenticated,)
	serializer_class = UsersSummaryReportSerializers

	def get_queryset(self):
		user = self.request.user
		if user.is_superuser:
			date = self.request.GET.get('date', None)
			emp_details = UsersSummaryReport.objects.filter(date=date)
			return emp_details

	def get(self,request,*args,**kwargs):
		get_data = self.get_queryset()
		date = self.request.GET.get('date', None)
		empty_dict = {}
		dummy_list=[]
		submitted_users = []
		employee_data = {}
		serializer = UsersSummaryReportSerializers(get_data, many=True)
		usernames_list = [u for u in UsersList.objects.all()]
		for serializerdata in serializer.data:
			submitted_users.append(serializerdata['user_id'])
			serializerdata['status'] = "Present"
			if serializerdata['user_id'] not in list(employee_data.keys()):
				employee_data[serializerdata['user_id']]=serializerdata
			else:
				employee_data[serializerdata['user_id']]['duration']= str(int(employee_data[serializerdata['user_id']]['duration'])+int(serializerdata['duration']))

		for user in usernames_list:
			if user.user_id not in submitted_users:
				employee_data[user.user_id] = {
				'user_id':user.user_id,
				'date' : date,
				'user_name' : user.user_first_name+ " " +user.user_last_name,
				'status' : "Absent"
					}
		return Response(employee_data.values(), status=status.HTTP_200_OK)

class emp_details(generics.RetrieveUpdateDestroyAPIView):
	
	serializer_class = UserListSerializers

	def get_queryset(self):
		user = self.request.user
		if user.is_superuser:
			emp_details = UsersList.objects.all()
			return emp_details
	def get(self,request,*args,**kwargs):
		get_data = self.get_queryset()
		serializer = UserListSerializers(get_data, many=True)
		data = serializer.data[:]
		return Response(data, status=status.HTTP_200_OK)

class emp_names_list(APIView):
	"""getting employee names from user model and append to list"""
	def get(self,request):
		usernames = User.objects.all()
		usernames_list = []
		for username in usernames:
			usernames_list.append(username.username)
		return Response(usernames_list,status=status.HTTP_200_OK)

class WorkFromHomes(APIView): 
	""" parameters: Select date,Select work request,SUBMIT
		-getting data from db based on the created_at,select_work_type-
		and return to the workhome_list
	"""
	def get(self,request,format = "json"):
		date = request.GET.get('Select date',None)
		selectworktype = request.query_params.get('Select work request',None)
		empnames = request.GET.get('SUBMIT',[])
		empname= empnames.split(",")
		workhome = WorkFromHome.objects.filter(created_at=date,
								select_work_type=selectworktype)

		workhome_list = []
		for workhome_data in workhome.values():
			if empname:
				workhome_list.append(workhome_data)

		for single_data in workhome_list:
			user_obj=User.objects.get(id=single_data['user_id'])
			single_data['username'] =  user_obj.username

		return Response(workhome_list, status=status.HTTP_200_OK)

	def post(self,request,format = "json"):
		""" parameters : select_date,select_work_request,submit
		"""
		date = request.data.get('select_date')
		selectworktype = request.data.get('select_work_request')
		user_ids = request.data.get('submit',[])
		for userids in user_ids:
			workhome = WorkFromHome.objects.create(user=User(id=userids),created_at=date,
								select_work_type=selectworktype)
		
		return Response(status=status.HTTP_200_OK)