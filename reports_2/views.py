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
from datetime import datetime,date, timedelta
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
							TotalLeaves,\
							ProjectsList
from reports.serializers import UsersSummaryReportSerializers,\
								UserListSerializers
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from reports_2.tasks import send_requests_email_to_employer
from django.db.models import Q
from xlsxwriter.workbook import Workbook
from reports_2.mailers import send_mails_to_employer, send_mails_to_owner

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
	""" 
	Only admin can see and approve employees leave requests.
	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = applyleaveserializer

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
			try:
				dt['remainingleaves'] = remaining_leaves[user_obj.username]
			except:
				dt['remainingleaves'] = 'NA'

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
		date = request.GET.get('Select_date',None)
		selectworktype = request.query_params.get('Select_work_request',None)
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
		
		row_data = 1
		column_data = 0

		response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		response['Content-Disposition'] = "attachment; filename=WorkFromHome.xlsx"
		book = Workbook(response,{'in_memory': True})

		work_sheet = book.add_worksheet('WorkFromHome {}'.format(date))
		cell_format = book.add_format()
		cell_format.set_bold(True)
		cell_format.set_bg_color('#85C1E9')
		cell_format.set_align('center')
		cell_format.set_font_size()
		column_data +=1
		work_sheet.write(row_data,column_data,'Employee Id',cell_format)
		column_data1 = column_data + 1
		work_sheet.write(row_data,column_data1,'Employee Name',cell_format)
		column_data2 = column_data1 + 1
		work_sheet.write(row_data,column_data2,'Create Date',cell_format)
		column_data3 = column_data2 + 1
		work_sheet.write(row_data,column_data3,'Work Type',cell_format)
		work_sheet.set_column(1, 15, 15)
		
		emp_id = []
		emp_name= []
		date = []
		work_type = []
		for u in workhome_list:
			emp_id.append(u['user_id'])
			emp_name.append(u['username'])
			date.append(str(u['created_at']))
			work_type.append(u['select_work_type'])

		for row_data,(ids,empname) in enumerate(zip(emp_id, emp_name)):
			row_data += 2
			work_sheet.write(row_data,column_data,ids)
			work_sheet.write(row_data,column_data1,empname)
    	
		for row_data,(created_date,work_type) in enumerate(zip(date, work_type)):
			row_data += 2
			work_sheet.write(row_data,column_data2,created_date)
			work_sheet.write(row_data,column_data3,work_type)

		book.close()	
		
		return response
		# return Response(workhome_list, status=status.HTTP_200_OK)

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

class emp_names(APIView):
	"""getting employee names from user model and append to list"""
	def get(self,request):
		usernames = User.objects.all().values('username','id')

		return Response(usernames,status=status.HTTP_200_OK)

class daily_reportss(APIView):

	""" parameters: from_date,to_date,name,project_name	"""
	def get(self,request,format = "json"):

		from_date = request.GET.get('from_date',None)
		to_date = request.GET.get('to_date',from_date)
		user_name = request.GET.get('name',None)
		project_name = request.GET.get('project_name',None)

		response = []
		if project_name and from_date:
			usersummaryreport = UsersSummaryReport.objects.filter(project_name=project_name,date=from_date)
			usersummaryreport_users = [users.user_name for users in usersummaryreport]
			daily_reports=UserDailyReport.objects.filter(username__in=usersummaryreport_users)
			for reports_values in daily_reports.values():
				response.append(reports_values)
		elif user_name:
			daily_reports = UserDailyReport.objects.filter(created_at__range=[from_date,to_date],username=user_name)
			for reports_values in daily_reports.values():
				response.append(reports_values)
		else:
			daily_reports = UserDailyReport.objects.filter(created_at=from_date)
			for reports_values in daily_reports.values():
				response.append(reports_values)
		return Response(response,status=status.HTTP_200_OK)

class project_names(APIView):
	def get(self,request):
		all_projects_names = ProjectsList.objects.all().values('project_name')

		return Response(all_projects_names,status=status.HTTP_200_OK)

class totalleaves(APIView):
	"""
		Total_leaves model to get total_leaves.
		print all users(user_id,user_name and total_leaves).
		or filter by user_id
		parameters : SUBMIT
	"""
	def get(self,request):
		emp_ids =request.GET.get('SUBMIT',[])
		t_leaves = {}
		if emp_ids:
			totalleaves = TotalLeaves.objects.filter(user=emp_ids)
			for single_data in totalleaves:
				tests = ast.literal_eval(single_data.data).values()
				for i in tests:
					t_leaves[single_data.user.id] = {
														'user_name':single_data.user.username,
														'user_id':single_data.user.id,
														'total_leaves':i['total_leaves']
													}
		else:
			totalleaves = TotalLeaves.objects.all()
			for single_data in totalleaves:
				tests = ast.literal_eval(single_data.data).values()
				for i in tests:
					t_leaves[single_data.user.id] = {
														'user_name':single_data.user.username,
														'user_id':single_data.user.id,
														'total_leaves':i['total_leaves']
													}
		
		return Response(t_leaves.values(), status=status.HTTP_200_OK)

class filtered_daily_user(generics.RetrieveUpdateDestroyAPIView):

	def get_queryset(self):
		user = self.request.user
		if user.is_superuser:
			yesterday = str(date.today() - timedelta(days = 1))
			yesterday = '2019-04-30'
			emp_details = UsersSummaryReport.objects.filter(date=yesterday)
			return emp_details

	def get(self,request,*args,**kwargs):
		get_data = self.get_queryset()

		serializer = UsersSummaryReportSerializers(get_data, many=True)
		presentUser = []
		for serializerdata in serializer.data:
			presentUser.append(serializerdata['user_name'])

		presentUser = list(dict.fromkeys(presentUser))
		submittedUser = []
		notSubmittedUser = []
		daily_report_yesterday = UserDailyReport.objects.filter(created_at= '2019-04-30')#=str(date.today() - timedelta(days = 1)))
		
		reportPeople = [user.username for user in daily_report_yesterday]

		response = []
		for user in presentUser:
			if user in reportPeople:
				submittedUser.append(user)
			else:
				notSubmittedUser.append(user)

		response = {
			'submitted': submittedUser,
			'notSubmitted': notSubmittedUser
		}
		return Response(response,status=status.HTTP_200_OK)	

class DailyReportCount(APIView): 
	""" parameters: Select date,Select work request,SUBMIT
		-getting data from db based on the created_at,select_work_type-
		and return to the workhome_list
	"""

	def get (self,request,*args,**kwargs):
		template_directory = 'email/dailyReportCount.html'
		send_mails_to_owner(template_directory)
		response = []
		return Response(response,status=status.HTTP_200_OK)
		

def dailyReportEmployeeCount(self):
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
		
		return response

def hello(self):
	print('hello')