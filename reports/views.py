import time
import requests
import base64
import logging
import ast
from datetime import datetime,timedelta,date
from calendar import monthrange
import xml.etree.ElementTree as ET

from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http.response import JsonResponse
from django.db.models import Q
from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from django.contrib.auth.models import User

from xlsxwriter.workbook import Workbook
from reports.models import ProjectsList,\
							UsersList,\
							UsersSummaryReport,\
							HolidayList,\
							UserDailyReport,\
							UserProfile,\
							RemainingAccruedLeaves,\
							UserXmldata,\
							TotalLeaves
from reports_2.models import BankAccountNumber
# Create your views here.

def user_register(request):
	if request.method == "POST":
		user_name,user_email,password,joined_date = (request.POST['user_name'],
			request.POST['user_email'],
			request.POST['password'],request.POST['joined_date'])
		user_profile = User.objects.create_user(username=user_name,
								 email=user_email,
								 password=password)
		user_profile = UserProfile.objects.create(user_name=user_name,
								 user_email=user_email,
								 password=password,
								 joined_date=joined_date)
		all_users=get_user_names()
		return render(request, 'login.html',{'all_users':all_users})
	else:
		return render(request, 'login.html',{'all_users':all_users})

def login_view(request):
	all_users=get_user_names()
	return render(request, 'login.html',{'all_users':all_users})

def logout_view(request):
	logout(request)
	return redirect("login")

def home(request):
	if request.method == "POST":
		username, password = request.POST['username'], request.POST['password']
		user = authenticate(username = username, password = password)
		if user is not None:
			login(request,user)
			user_name = request.user
			return render(request,'home.html',{'user':user_name})
			# return render(request,'worksnaps_report.html',{'all_users':all_users})
		else:
			return HttpResponse('{"error": "User does not exist"}')
	else:
		user_name = request.user
		return render(request,'home.html',{'user':user_name})

def worksnaps_report_html(request):
	user = request.user
	if user.is_superuser:
		all_users=get_user_names()
		return render(request,'worksnaps_report.html',{'all_users':all_users})
	else:
		return JsonResponse(
			{"Sorry dude you do not have permissions":"To access you must be super user"})

def daily_report_html(request):
	user = request.user
	if user.id == None:
		return JsonResponse(
			{"Sorry dude you do not have permissions":"To access you must be login"})
	else:
		all_users=get_user_names()
		return render(request,'dailyreport.html',{'all_users':all_users})

def registration_html(request):
	all_users=get_user_names()
	return render(request,'register.html',{'all_users':all_users})

def get_data(url):
	'''
		This function will work like get data from worksnaps
		Args: API end point
		Return: JSON data for given end point
	'''
	token = '23Mh2bkhQkUoqlU0KDfpVaYg9wXXsSgHr7YKdSm8'
	project_url = 'https://api.worksnaps.com/api/{}.json'.format(url)
	client_token = '{}:{}'.format(token,"ignored").encode()
	headers = {
		'Authorization':'Basic'+' '+base64.b64encode(client_token).decode('utf-8'),
		'Accept':'application/json',
		'Content-Type':'application/json',
	}
	request_data = requests.get(project_url,headers=headers)
	# print(request_data,"project data")
	request_data_json = request_data.json()

	return request_data_json

def get_summary(user_id,from_date,to_date):
	'''
		This function will work like get the user data from worksnaps
		Args: Worksnaps user id, From date and To date
		Return: JSON data for given user id
	'''
	user_ids = user_id
	name='manager_report'
	token = '23Mh2bkhQkUoqlU0KDfpVaYg9wXXsSgHr7YKdSm8'
	users_url = "https://api.worksnaps.com/api/summary_reports.json"
	client_token = '{}:{}'.format(token,"ignored").encode()
	headers = {
		'Authorization':'Basic'+' '+base64.b64encode(client_token).decode('utf-8'),
		'Accept':'application/json',
		'Content-Type':'application/json',
	}
	params={"from_date":from_date,"to_date":to_date,"user_ids":user_ids,"name":name}
	request_data = requests.get(users_url,headers=headers,params=params)
	request_data_json = request_data.json()
	# print(pprint.pprint(request_data_json))
	return request_data_json

def create_users(request):
	'''
		This function creates the list of user in DB who are available in Worksnaps
	'''
	user = request.user
	if user.is_superuser:
		users_qs = UsersList.objects.only('user_id')
		users_ids = [single_user.user_id for single_user in users_qs]
		worksnaps_users = get_data('users')
		print(users_ids,"-----")
		for i,value in enumerate(worksnaps_users.get("users")):
				if value.get('id',0) not in users_ids:
					print(value.get('id',0),"cooollllllll")
					UsersList.objects.create(
						user_id=value.get('id',''),user_email=value.get(
						'email',''),user_first_name=value.get(
						'first_name',''),user_last_name=value.get(
						'last_name',''),user_login_as=value.get('login',''))

		return JsonResponse({"Refresh":"Success"})
	else:
		return JsonResponse(
			{"Sorry dude you do not have permissions":"To access you nust be super user"})

def create_project(request):
	'''
		This function creates the list of projects in DB who are available in Worksnaps
	'''
	user = request.user
	if user.is_superuser:
		projects_qs = ProjectsList.objects.only('project_id')
		project_ids = [single_project.project_id for single_project in projects_qs]
		worksnaps_project = get_data('projects')
		for i,value in enumerate(worksnaps_project.get("projects")):
				if value.get('id',0) not in project_ids:
					ProjectsList.objects.create(
						project_id=value.get('id',''),project_name=value.get(
							'name',''),project_description=value.get(
							'description',''),project_status=value.get('status',''))

		return JsonResponse({"Refresh":"Success"})
	else:
		return JsonResponse(
			{"Sorry dude you do not have permissions":"To access you nust be super user"})

def convert_date_str_datetime(date_str):
	'''
		Convert the string date to date time object
		Args: date(in string)
		Return: date(date time object)
	'''
	date_datetime = datetime.strptime(date_str, '%Y-%m-%d')
	return date_datetime

def convert_date_datetime_str(create_datetime_obj):
	'''
		Convert the date object to string date
		Args: date(date time object)
		Return: date(in string)
	'''
	date_str = datetime.strftime(create_datetime_obj, '%Y-%m-%d')
	return date_str

def get_all_users_daily_data(from_date,to_date):
	users_qs = UsersList.objects.only('user_id')
	users_ids = [single_user.user_id for single_user in users_qs]
	current_date = to_date
	from_date = from_date
	while from_date < current_date:
		print(from_date,"from_date")
		to_date_datetime = from_date + timedelta(days = 1)
		from_date_str = convert_date_datetime_str(from_date)
		to_date_str = convert_date_datetime_str(to_date_datetime)
		for user_id in users_ids:
			worksnaps_summary = get_summary(user_id,from_date_str,to_date_str)
			print(worksnaps_summary,"user data")
			print(worksnaps_summary.get("manager_report"),"worksnaps_summary")
			if worksnaps_summary.get("manager_report"):
				print("Entered in to the first loop")
				for i,value in enumerate(worksnaps_summary.get("manager_report")):
					if to_date_str == value.get('date',0):
						UsersSummaryReport.objects.create(
							user_name=value.get('user_name',''),user_id=value.get(
								'user_id',''),date=value.get('date',''),duration=value.get(
								'duration_in_minutes',''),project_name=value.get(
								'project_name',''))
		from_date = from_date + timedelta(days = 1)

def create_users_summary(request):
	'''
		This function will store the all user Worksnaps data for given dates
	'''
	user = request.user
	if user.is_superuser:
		from_date = '2018-07-31'
		to_date = '2018-08-1'
		# summary_qs = UsersSummaryReport.objects.get(date=to_date)
		# users_ids = [single_date.user_id for single_date in summary_qs]
		users_qs = UsersList.objects.only('user_id')
		users_ids = [single_user.user_id for single_user in users_qs]
		current_date = convert_date_str_datetime(to_date)
		from_date = convert_date_str_datetime(from_date)
		while from_date < current_date:
			print(from_date,"from_date")
			to_date_datetime = from_date + timedelta(days = 1)
			from_date_str = convert_date_datetime_str(from_date)
			to_date_str = convert_date_datetime_str(to_date_datetime)
			for user_id in users_ids:
				worksnaps_summary = get_summary(user_id,from_date_str,to_date_str)
				print(worksnaps_summary,"user data")
				print(worksnaps_summary.get("manager_report"),"worksnaps_summary")
				if worksnaps_summary.get("manager_report"):
					print("Entered in to the first loop")
					for i,value in enumerate(worksnaps_summary.get("manager_report")):
						if to_date_str == value.get('date',0):
							UsersSummaryReport.objects.create(
								user_name=value.get('user_name',''),user_id=value.get(
									'user_id',''),date=value.get('date',''),duration=value.get(
									'duration_in_minutes',''),project_name=value.get(
									'project_name',''))
			from_date = from_date + timedelta(days = 1)

		return JsonResponse({"Refresh":"Success"})
	else:
		return JsonResponse(
			{"Sorry dude you do not have permissions":"To access you nust be super user"})

@api_view(['POST'])
def add_holiday_list(request):
	'''
		Able to add the custom holidays from frontend
	'''
	if request.method == 'POST':
		print(request.data,"printinf the date")
		holiday_date = request.data.get("date_h",'')
		holiday_description = request.data.get("holiday_description",'')
		day = request.data.get("day",'')
		HolidayList.objects.create(
			holiday_date=holiday_date,holiday_description=holiday_description,day=day)
	return JsonResponse({"Refresh":"Success"})


def working_days(year,month,from_date,to_date):
	'''
		Calculates the no of working days in a given month
	'''
	monthrang = monthrange(int(year),int(month))
	if monthrang[0] == 6 and monthrang[1] >= 30:
		no_of_working_days =  monthrang[1] - 6
	elif monthrang[0] == 5 and monthrang[1] >= 30:
		no_of_working_days =  monthrang[1] - 6
	elif monthrang[0] == 0:
		no_of_working_days =  monthrang[1] - 6
	else:
		no_of_working_days = monthrang[1] - 5
	holidays = HolidayList.objects.filter(
		Q(holiday_date__gte=from_date) & Q(holiday_date__lte=to_date))
	no_holidays = len(holidays)
	no_of_working_days = no_of_working_days - no_holidays
	return no_of_working_days,monthrang[0],monthrang[1]

def create_datetime_obj(sunday_date_str,year,month):
	'''
		create date objets for give month
	'''
	sun_sat_dates_datetime = []
	secons_sat = sunday_date_str[1]
	sun_sat_dates_datetime.append(date(int(year),int(month),secons_sat-1))
	if month == '6':
		sunday_date_srt = sunday_date_str.pop(-1)
	for single_date in sunday_date_str:
		sun_sat_dates_datetime.append(date(int(year),int(month),single_date))
	return sun_sat_dates_datetime

def get_this_month_holidays(from_date,to_date):
	'''
		Get the holidays for the given month
	'''
	holiday_qs = HolidayList.objects.filter(
		Q(holiday_date__gte=from_date) & Q(
			holiday_date__lte=to_date))
	return [single_holiday.holiday_date for single_holiday in holiday_qs]

def create_month_days(no_days,year,month):
	'''
		Create a list of no of days
		Args: number of days
		Return: list of number of days
	'''
	whole_month_days = []
	for sing_day in range(0,no_days):
		whole_month_days.append(date(int(year),int(month),sing_day+1))
	return whole_month_days

def get_leave_dates(whole_month_days,no_dates):
	'''
		Get user leave dates
		Args:Whole month days(date objects),no of days user worked(date object)
		Return:No of leave dates
	'''
	leave_dates = list(set(whole_month_days) - set(no_dates))
	return leave_dates

def worked_on_weekenddays(user_worked_as_per_working_days,no_dates):
	'''
		Get the user worked on weekend days with dates
		Args:user worked with out weekend days,User worked dates
		Return: worked weekend days
	'''
	worked_weekend_days = list(set(no_dates)-set(user_worked_as_per_working_days))
	return worked_weekend_days

def time_worked_on_weeend_days(user_summary_qs,worked_weekend_days,total_duration):
	'''
		Calculate the time worked on weekend days worked
		Args:month query set,worked weekend days,total time worked
		Return:Time worked on weekend days
	'''
	extra_time_worked = []
	for single_date in user_summary_qs:
		for i,sing_day in enumerate(worked_weekend_days):
			if sing_day == single_date.date:
				extra_time = single_date.duration
				extra_time_worked.append(int(extra_time))
	return sum(extra_time_worked)


def get_user_names():
	user_list = UsersList.objects.all()
	user_name = []
	for single_user in user_list:
		first_name = single_user.user_first_name
		last_name = single_user.user_last_name
		username = first_name+' '+last_name
		user_name.append(username)
	user_name.append("s7_worksnaps")
	return sorted(user_name)

def create_from_to_date(year,month):
	monthrang = monthrange(int(year),int(month))
	from_date = year+'-'+month+'-'+'1'
	to_date = year+'-'+month+'-'+'{}'.format(monthrang[1])
	return from_date,to_date

def remove_dates_before_joined(leave_dates,joined_date):
	leave_dates_copy = leave_dates.copy()
	for single_date in leave_dates:
		if single_date < joined_date:
			leave_dates_copy.remove(single_date)
	return leave_dates_copy

def users_summary(from_date,to_date,year,month,user_name):
	'''
		Generate the user month report
		Return:users data(list of dict in side user as key value as user data)
			user_names(list of usernames)
	'''
	if year and month:
		month = month
		year = year
		from_date,to_date = create_from_to_date(year,month)
	if from_date and not year and not month:
		month = from_date.split('-')[1]
		year = from_date.split('-')[0]
	if user_name == 'all':
		# user_names = ["Rajender Reddy Garlapally","Vikash Babu Bendalam","Ananya Dodda",
		# "Mohan Krishna Y","Pavan Chand","Vignan Akoju","Venkatesh Marreboina",
		# "Mounika NagaHarish","Narendra Babu Ballilpalli","Ramya Ketha",'Swapna Bodduluri',
		# "Vinod Kumar Kurra","Mounika Bandaru","Naveen Kumar Katta","Mohiuddin Mohammed",
		# "Dileep Kumar Kommineni","Uday Kumar","kandukuri chary","Mani Sankar Nambaru",
		# "Mahesh Gorage","Atul Kumar","suresh kanchumati"]
		user_names = get_user_names()
	else:
		user_names = []
		user_names.append(user_name)
	data2 = {}
	month_daya,monthrang = monthrange(int(year),int(month))
	wfh_data = parse_xml_data(user_names,monthrang,int(month),int(year))
	print(wfh_data,"wfromdata")
	user_names.remove('s7_worksnaps')
	for user_name in user_names:
		print(user_name,"user name")
		user_summary_qs = UsersSummaryReport.objects.filter(
			Q(date__gte=from_date) & Q(date__lte=to_date),user_name=user_name)
		# print(user_summary_qs,"user summary list")
		total_duration = []
		no_dates = []
		partial_work_dates = []
		extra_work_dates = []
		worked_less = []
		user_wfh = wfh_data.get(user_name)
		user_summary_date_time = {}
		for single_date in user_summary_qs:
			time_done = single_date.duration
			total_duration.append(int(time_done))
			qs_date = single_date.date
			if not user_summary_date_time.get(qs_date):
				user_summary_date_time[qs_date] = time_done
			else:
				user_summary_date_time[qs_date] = int(time_done) + int(
									user_summary_date_time[qs_date])
		#print(user_summary_date_time,"hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
		for key,time_done_per_day in user_summary_date_time.items():
			qs_date_str = convert_date_datetime_str(key)
			user_wfh_date = user_wfh.get(qs_date_str)
			if user_wfh_date:
				user_wfh_ips = user_wfh_date.get('ip_address')
			else:
				user_wfh_ips = None
			if user_wfh_ips:
				wfh_time = len(user_wfh_ips) * 10
			else:
				wfh_time = 0
			if (int(time_done_per_day) > 300 and int(wfh_time) != int(time_done_per_day)):
				no_dates.append(key)
			if int(time_done_per_day) >= 300 and int(time_done_per_day) < 480:
				partial_time = qs_date_str+'-->'+str(int(time_done_per_day))
				partial_work_dates.append(partial_time)
				no_dates.append(key)
			if int(time_done_per_day) >= 480:
				extra_time = qs_date_str+'-->'+str(int(time_done_per_day))
				extra_work_dates.append(extra_time)
				no_dates.append(key)
			if int(time_done_per_day) < 300:
				worked_less.append(key)
		#print(user_name)
		#print(partial_work_dates,"partial work dates")
		#get number of working days
		no_working_days,month_start_day,days_in_month = working_days(year,month,from_date,to_date)
		sunday_start = 7-month_start_day
		list_hanig_sundays = []

		while sunday_start <= 31:
			list_hanig_sundays.append(sunday_start)
			sunday_start = sunday_start + 7
		# create datetime obj of sundays and saturdays
		list_sun_sat = create_datetime_obj(list_hanig_sundays,year,month)
		# get list of holidays
		list_holidays = get_this_month_holidays(from_date,to_date)
		if list_holidays not in list_sun_sat:
			list_sun_sat.extend(list_holidays)

		month_holidays = list(set(list_sun_sat))
		# create whole month datetime obj
		whole_month_days = create_month_days(days_in_month,year,month)

		no_dates_holidays = []
		no_dates_holidays.extend(month_holidays)
		no_dates_holidays.extend(no_dates)

		leave_dates = get_leave_dates(whole_month_days,no_dates_holidays)
		try:
			user_profile = UserProfile.objects.get(user_name=user_name)
			joined_date = user_profile.joined_date
		except:
			joined_date = None
			logging.exception("message")
		leave_dates = remove_dates_before_joined(leave_dates,joined_date)
		no_dates.extend(worked_less)
		user_worked_as_per_working_days = list(set(no_dates)-set(month_holidays))

		worked_weekend_days = worked_on_weekenddays(user_worked_as_per_working_days,no_dates)
		if worked_weekend_days:
			worked_on_weekend_days_holiday = "Yes"
			extra_time_worked = time_worked_on_weeend_days(
				user_summary_qs,worked_weekend_days,total_duration)
		else:
			worked_on_weekend_days_holiday = "No"
			extra_time_worked = 0
		total_time_to_work = (no_working_days-len(leave_dates)) * 480
		total_time_worked = sum(total_duration)
		if (user_name	):
			#pass
			user = User.objects.get(username=user_name)
			try:
				total_leaves_qs = TotalLeaves.objects.get(user=user)
				total_leaves_data = ast.literal_eval(total_leaves_qs.data)
				year_month_data = "{}-{}".format(year,month)
				to_date_obj = convert_date_str_datetime(to_date)
				if (not total_leaves_data.get(str(year_month_data)) and
					joined_date < to_date_obj.date()):
					year_month = "{}-{}".format(year,month)
					total_leaves_data[year_month] = {}
					total_leaves_data[year_month]['month'] = month
					total_leaves_data[year_month]['total_leaves'] = len(leave_dates)
					if int(month) == 1:
						last_month = "{}-{}".format(int(year)-1,12)
					else:
						last_month = "{}-{}".format(year,int(month)-1)
					accrued_leaves = total_leaves_data[str(last_month)]['accrued_leaves'] + 2
					if len(leave_dates) == 0:
						total_leaves_data[year_month]['paid_leaves'] = 0
						total_leaves_data[year_month]['unpaid_leaves'] = 0
					elif len(leave_dates) > accrued_leaves:
						unpaid_leaves = len(leave_dates) - accrued_leaves
						total_leaves_data[year_month]['unpaid_leaves'] = unpaid_leaves
						total_leaves_data[year_month]['paid_leaves'] = accrued_leaves
						accrued_leaves = 0
					elif accrued_leaves >= len(leave_dates):
						total_leaves_data[year_month]['unpaid_leaves'] = 0
						total_leaves_data[year_month]['paid_leaves'] = len(leave_dates)
						accrued_leaves = accrued_leaves - len(leave_dates)
					total_leaves_data[year_month]['accrued_leaves'] = accrued_leaves
					total_leaves_qs.data = total_leaves_data
					total_leaves_qs.save()
			except TotalLeaves.DoesNotExist as e:
				to_date_obj = convert_date_str_datetime(to_date)
				if joined_date < to_date_obj.date():
					#logging.exception("message")
					year_month = "{}-{}".format(year,month)
					total_leaves_dict = {}
					total_leaves_dict[year_month] = {}
					total_leaves_dict[year_month]['month'] = month
					total_leaves_dict[year_month]['total_leaves'] = len(leave_dates)
					joined_day = joined_date.day
					accrued_per_day = 2/days_in_month
					accrued_leaves = ((days_in_month - joined_day)*(accrued_per_day))
					if len(leave_dates) == 0:
						total_leaves_dict[year_month]['paid_leaves'] = 0
						total_leaves_dict[year_month]['unpaid_leaves'] = 0
					elif len(leave_dates) > accrued_leaves:
						unpaid_leaves = len(leave_dates) - accrued_leaves
						total_leaves_dict[year_month]['unpaid_leaves'] = unpaid_leaves
						total_leaves_dict[year_month]['paid_leaves'] = accrued_leaves
						accrued_leaves = 0
					elif accrued_leaves > len(leave_dates):
						total_leaves_dict[year_month]['unpaid_leaves'] = 0
						total_leaves_dict[year_month]['paid_leaves'] = accrued_leaves
					total_leaves_dict[year_month]['accrued_leaves'] = accrued_leaves
					TotalLeaves.objects.create(user=user,data=total_leaves_dict)

		data = {
		'Name': user_name,
		'No of leaves' : len(leave_dates),
		'Leave Dates' : leave_dates,
		'No of working days': no_working_days,
		'No of days worked': len(set(user_worked_as_per_working_days)),
		'Partial work':partial_work_dates,
		'Extra work':extra_work_dates,
		'For Month': month,
		'Worked on weekend days or holidays':worked_on_weekend_days_holiday,
		'Dates Worked on weekend days':worked_weekend_days,
		'Time Worked on weekend days':extra_time_worked,
		"Total time to work":round((total_time_to_work)/(60),0),
		"Total time worked":round((total_time_worked)/(60),0),
		}
		data2[user_name] = data
	return data2,user_names

def username_excel(sheet1,user_names,cell_format,user_summary):
	row = 1
	column = 0
	updated_user_name = []
	for i,single_user in enumerate(sorted(user_names)):
		print(single_user,"user name")
		#print(type(user_summary),"user summary")
		single_user_summary = user_summary.get(single_user)
		if single_user_summary:
			user_worked_days = single_user_summary.get('No of days worked')

		else:
			user_worked_days = None
		if (single_user != "Ikkurthi Manikanta" and 
			single_user != "Saumya Garg" 
			and single_user != "s7_worksnaps"
			and single_user != "Kusuma Kavya Kandi" and
			single_user != "Sai Bhaskar Ravuri" and
			single_user != "Vignan Akoju" and
			single_user != "Vinod Kumar Kurra" and
			single_user != "suresh kanchumati" and user_worked_days):
			sheet1.write(row,column,single_user)
			updated_user_name.append(single_user)
			row = row + 1
	return updated_user_name

def headers_data(sheet1,headers,cell_format):
	row = 0
	column = 1
	for i,single_header in enumerate(headers):
		sheet1.write(row,column,single_header,cell_format)
		column = column + 1

def change_date_format(dates):
	str_date = []
	if dates:
		for single_date in dates:
			date_time = single_date.isoformat()
			str_date.append(date_time)
		return str_date
	else:
		return '-'

def show_data(sheet1,user_names,headers,user_summary,cell_format):
	row = 1
	column = 0
	row_data = 1
	column_data = 1
	for key, user_data in sorted(user_summary.items()):
		user_data_worked = user_data.get('No of days worked')
		if (key != "Ikkurthi Manikanta" 
			and key != "Saumya Garg" 
			and key != "s7_worksnaps"
			and key != "Kusuma Kavya Kandi" and
                        key != "Sai Bhaskar Ravuri" and
                        key != "Vignan Akoju" and
                        key != "Vinod Kumar Kurra" and
                       	key != "suresh kanchumati" and user_data_worked):
			sheet1.write(row_data,column_data,user_data.get('Bank Account Nos',''),cell_format)
			column_data = column_data + 1
			sheet1.write(row_data,column_data,user_data.get('No of working days',"-"),cell_format)
			column_data = column_data + 1
			sheet1.write(row_data,column_data,user_data.get('No of days worked',"-"),cell_format)
			column_data = column_data + 1
			sheet1.write(row_data,column_data,user_data.get('No of leaves',"-"),cell_format)
			column_data = column_data + 1
			leave_dates = change_date_format(user_data.get('Leave Dates',"-"))
			sheet1.write(row_data,column_data,str(leave_dates),cell_format)
			column_data = column_data + 1
			sheet1.write(row_data,column_data,user_data.get('No of remainig leaves',''),cell_format)
			column_data = column_data + 1
			sheet1.write(row_data,column_data,user_data.get('Total time to work',"-"),cell_format)
			column_data = column_data + 1
			sheet1.write(row_data,column_data,user_data.get('Total time worked',"-"),cell_format)
			column_data = column_data + 1
			sheet1.write(row_data,column_data,user_data.get('Worked on weekend days or holidays',"-"),cell_format)
			column_data = column_data + 1
			sheet1.write(row_data,column_data,user_data.get('Time Worked on weekend days',"-"),cell_format)
			column_data = column_data + 1
			weekend_days = change_date_format(user_data.get('Dates Worked on weekend days',"-"))
			sheet1.write(row_data,column_data,str(weekend_days),cell_format)
			column_data = column_data + 1
			partial_work = user_data.get('Partial work','-')
			sheet1.write(row_data,column_data,str(partial_work))
			column_data = column_data + 1
			extra_work = user_data.get('Extra work','-')
			sheet1.write(row_data,column_data,str(extra_work))
			column_data = column_data + 1
			row_data = row_data + 1
			column_data = 1

def get_remaining_leaves():
	'''
		this function will return the remaing leaves of all employees
	'''
	remaining_leaves = TotalLeaves.objects.all()
	# print(reminig_leaves)
	# ordered = sorted(reminig_leaves, key=operator.attrgetter('user'))
	# print(ordered)
	return remaining_leaves

def get_bankaccount_nos():
	'''
		this function will return the users bank account numbers
	'''
	account_nos = BankAccountNumber.objects.all()
	return account_nos

def store_remaining_leaves(sheet1,remainig_leave,user_names,month,year):
	row_data = 0
	column_data = 6
	year_month = "{}-{}".format(year,month)
	user_names_copy = user_names.copy()
	if len(user_names_copy) > 1 and 's7_worksnaps' in user_names_copy:
		user_names_copy.remove('s7_worksnaps')
	for i,username in enumerate(user_names_copy):
		row_data = row_data + 1
		user = User.objects.get(username=username)
		try:
			total_leaves = TotalLeaves.objects.get(user=user)
		except TotalLeaves.DoesNotExist as e:
			total_leaves = None
		if total_leaves:
			accured_leaves_month = ast.literal_eval(total_leaves.data).get(year_month,None)
		else:
			accured_leaves_month = None
		if accured_leaves_month:
			accrued_leaves = accured_leaves_month.get('accrued_leaves')
			loss_of_pay = accured_leaves_month.get('unpaid_leaves')
			sheet1.write(row_data,column_data,accrued_leaves)
			sheet1.write(row_data,column_data+10,loss_of_pay)

def wfh_data_refined(data):
	data_in_list = []
	offline_dates = []
	for date,single_data in data.items():
		if single_data.get('ip_address'):
			no_min = str(len(single_data.get('ip_address'))*10)
			user_date = single_data.get('date')
			data_in_str = user_date+'-->'+no_min
			data_in_list.append(data_in_str)
		if single_data.get('offline_time'):
			no_min = str(len(single_data.get('offline_time'))*10)
			user_date = single_data.get('date')
			data_in_str = user_date+'-->'+no_min
			offline_dates.append(data_in_str)
	return data_in_list,offline_dates

def store_wfh_data(sheet1,users_wfh_data,user_names):
	row_data = 0
	column_data = 14
	user_names_copy = user_names.copy()
	if len(user_names_copy) > 1 and 's7_worksnaps' in user_names_copy:
		user_names_copy.remove('s7_worksnaps')
	for i,username in enumerate(user_names_copy):
		row_data = row_data + 1
		single_user_data = users_wfh_data.get(username)
		if single_user_data:
			final_data,offline_time = wfh_data_refined(single_user_data)
			sheet1.write(row_data,column_data,str(final_data))
			sheet1.write(row_data,column_data+1,str(offline_time))

def store_bankaccount_nos(sheet1,account_nos,user_names):
        row_data = 0
        column_data = 1
        user_names_copy = user_names.copy()
        if len(user_names_copy) > 1 and 's7_worksnaps' in user_names_copy:
                user_names_copy.remove('s7_worksnaps')
        for i,username in enumerate(user_names_copy):
                row_data = row_data + 1
                for single_user in account_nos:
                        if username == single_user.user.username:
                                sheet1.write(row_data,column_data,single_user.account_number)

def show_data_in_excel(request):
	month = request.GET.get("month",0)
	year = request.GET.get("year",2018)
	from_date = request.GET.get("from_date",0)
	to_date = request.GET.get("to_date",0)
	user_name = request.GET.get("user_name",0)
	month_start,monthrang = monthrange(int(year),int(month))
	if user_name == "all":
		user_summary,user_names = users_summary(from_date,to_date,year,month,user_name)
	else:
		user_summary,user_names = users_summary(from_date,to_date,year,month,user_name)
	# print(user_summary,"Data")

	# filename = '{}_raw_data_{}_to_{}.xlsx'.format(request.user.username,
	# 	from_date.strftime('%b_%d_%Y'),to_date.strftime('%b_%d_%Y'))
	response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	response['Content-Disposition'] = "attachment; filename=Worksnaps Report.xlsx"
	book = Workbook(response,{'in_memory': True})
	headers = ['Bank Account Nos','No of working days','No of days worked','No of leaves','Leave Dates',
	'No of Accrued_leaves','Total time to work','Total time worked','Worked on weekend days or holidays',
	'Time Worked on weekend days','Dates Worked on weekend days','Partial work','Extra work',
	'Work from home dates and time','Offline time','Loss of pay days']
	
	sheet1 = book.add_worksheet('{}-{}'.format(month,year))
	sheet1.freeze_panes(1, 1)
	sheet1.set_column('A:A',25)
	sheet1.set_row(0, 40)
	sheet1.set_column(1, 9, 15)
	cell_format = book.add_format()
	cell_format.set_text_wrap()
	cell_format.set_align('left')
	#print(user_summary,"user summary")
	updated_user_name = username_excel(sheet1,user_names,cell_format,user_summary)
	headers_data(sheet1,headers,cell_format)
	show_data(sheet1,user_names,headers,user_summary,cell_format)
	remainig_leave = get_remaining_leaves()
	user_names = get_user_names()
	account_nos = get_bankaccount_nos()
	if user_name == "all":
		store_remaining_leaves(sheet1,remainig_leave,updated_user_name,month,year)
		store_bankaccount_nos(sheet1,account_nos,updated_user_name)
		users_wfh_data = parse_xml_data(updated_user_name,monthrang,month,year)
		store_wfh_data(sheet1,users_wfh_data,updated_user_name)
	else:
		user_names = []
		user_names.append(user_name)
		store_remaining_leaves(sheet1,remainig_leave,user_names,month,year)
		store_bankaccount_nos(sheet1,account_nos,user_names)
		users_wfh_data = parse_xml_data(user_names,monthrang,month,year)
		store_wfh_data(sheet1,users_wfh_data,user_names)
	book.close()

	return response

def store_daily_report(request):
	if request.method == "POST":
		username = request.user
		cretaed_at = request.POST.get("cretaed_at","Not filled anything")
		q1 = request.POST.get("q1","Not filled anything")
		q2 = request.POST.get("q2","Not filled anything")
		q3 = request.POST.get("q3","Not filled anything")
		q4 = request.POST.get("q4","Not filled anything")
		q5 = request.POST.get("q5","Not filled anything")
		UserDailyReport.objects.create(
			username=username,cretaed_at=cretaed_at,what_was_done_this_day=q1,
			what_is_your_plan_for_the_next_day = q2,
			what_are_your_blockers = q3,
			do_you_have_enough_tasks_for_next_three_days = q4,
			if_you_get_stuck_are_you_still_able_to_work_on_something_else = q5)
		messages.success(request, 'Daily report submitted')
		all_users=get_user_names()
		return render(request,'dailyreport.html',{'all_users':all_users})
	else:
		messages.error(request, 'Daily report did not submit')
		all_users=get_user_names()
		return render(request,'dailyreport.html',{'all_users':all_users})

def parse_xml_data(user_names,monthrange,selected_month,year):
	end_date = int(monthrange)
	from_date = datetime(int(year),int(selected_month),1,0,0,0)
	to_date = datetime(int(year),int(selected_month),end_date,0,0,0)
	work_from_home = {}
	for single_user in user_names:
		work_from_home[single_user] = {}
		current_date = from_date
		while current_date <= to_date:
			try:
				user = User.objects.get(username=single_user)
			except:
				user = None
			if user:
				xml_data_qs = UserXmldata.objects.filter(user=user,date=current_date.date())
				from_date_str = convert_date_datetime_str(current_date)
				work_from_home[single_user][from_date_str] = {}
				work_from_home[single_user][from_date_str]['date'] = from_date_str
				work_from_home[single_user][from_date_str]['ip_address'] = []
				work_from_home[single_user][from_date_str]['offline_time'] = []
				work_from_home[single_user][from_date_str]['user'] = single_user
				for single_data in xml_data_qs:
					str_xml_data = single_data.xml_data
					root_xml = ET.fromstring(str_xml_data)
					office_ip = root_xml[0][10].text
					if office_ip != '183.82.115.50' and office_ip != None:
						work_from_home[single_user][from_date_str]['ip_address'].append(
												office_ip)
					elif office_ip == None:
						work_from_home[single_user][from_date_str]['offline_time'].append(
													office_ip)
			current_date = current_date + timedelta(days=1)
	#print(work_from_home)
	return work_from_home

