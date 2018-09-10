import requests
import base64
from datetime import datetime,timedelta,date
from calendar import monthrange

from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http.response import JsonResponse
from django.db.models import Q
from django.shortcuts import render, HttpResponse

from reports.models import ProjectsList,UsersList,UsersSummaryReport,HolidayList
# Create your views here.

def home(request):
	return render(request,'home.html')

def worksnaps_report_html(request):
	return render(request,'worksnaps_report.html')
def daily_report_html(request):
	return render(request,'dailyreport.html')

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

def convert_date_datetime_str(datetime_obj):
	'''
		Convert the date object to string date
		Args: date(date time object)
		Return: date(in string)
	''' 
	date_str = datetime.strftime(datetime_obj, '%Y-%m-%d')
	return date_str	

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


def working_days():
	'''
		Calculates the no of working days in a given month
	'''
	monthrang = monthrange(2018,8)
	if monthrang[0] == 6 and monthrang[1] >= 30:
		no_of_working_days =  monthrang[1] - 6
	elif monthrang[0] == 5 and monthrang[1] >= 31:
		no_of_working_days =  monthrang[1] - 6
	elif monthrang[0] == 0:
		no_of_working_days =  monthrang[1] - 6
	else:
		no_of_working_days = monthrang[1] - 5
	holidays = HolidayList.objects.filter(
		Q(holiday_date__gte='2018-08-1') & Q(holiday_date__lte='2018-08-31'))
	no_holidays = len(holidays)
	no_of_working_days = no_of_working_days - no_holidays
	return no_of_working_days,monthrang[0],monthrang[1]

def create_datetime_obj(sunday_date_str):
	'''
		create date objets for give month
	'''
	sun_sat_dates_datetime = []
	secons_sat = sunday_date_str[1]
	sun_sat_dates_datetime.append(date(2018,8,secons_sat-1))
	for single_date in sunday_date_str:
		sun_sat_dates_datetime.append(date(2018,8,single_date))
	return sun_sat_dates_datetime

def get_this_month_holidays():
	'''
		Get the holidays for the given month
	'''
	holiday_qs = HolidayList.objects.filter(
		Q(holiday_date__gte='2018-08-1') & Q(
			holiday_date__lte='2018-08-31'))
	return [single_holiday.holiday_date for single_holiday in holiday_qs]

def create_month_days(no_days):
	'''
		Create a list of no of days
		Args: number of days
		Return: list of number of days
	'''
	whole_month_days = []
	for sing_day in range(0,no_days):
		whole_month_days.append(date(2018,8,sing_day+1))
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

def users_summary(request):
	'''
		Generate the user month report
	'''
	user = request.user
	if user.is_superuser: 
		user_names = ["Rajender Reddy Garlapally","Vikash Babu Bendalam","Ananya Dodda",
		"Mohan Krishna Y","Pavan Chand","Vignan Akoju","Venkatesh Marreboina",
		"Mounika NagaHarish","Narendra Babu Ballilpalli","Ramya Ketha",'Swapna Bodduluri',
		"Vinod Kumar Kurra","Mounika Bandaru","Naveen Kumar Katta","Mohiuddin Mohammed",
		"Dileep Kumar Kommineni","Uday Kumar","kandukuri chary","Mani Sankar Nambaru",
		"Mahesh Gorage","Atul Kumar","suresh kanchumati"]
		data2 = {}	
		for user_name in user_names:
			user_summary_qs = UsersSummaryReport.objects.filter(
				Q(date__gte='2018-08-1') & Q(date__lte='2018-08-31'),user_name=user_name)
			# print(user_summary_qs,"user summary list")
			total_duration = []
			no_dates = []
			for single_date in user_summary_qs:
				time_done = single_date.duration
				total_duration.append(int(time_done))
				no_dates.append(single_date.date)
			
			no_working_days,month_start_day,days_in_month = working_days()
			sunday_start = 7-month_start_day
			list_hanig_sundays = []
			
			while sunday_start <= 31:
				list_hanig_sundays.append(sunday_start)
				sunday_start = sunday_start + 7
			
			list_sun_sat = create_datetime_obj(list_hanig_sundays)
			list_holidays = get_this_month_holidays()
			
			if list_holidays not in list_sun_sat:
				list_sun_sat.extend(list_holidays)
			
			month_holidays = list(set(list_sun_sat))
			whole_month_days = create_month_days(days_in_month)
			
			no_dates_holidays = []
			no_dates_holidays.extend(month_holidays)
			no_dates_holidays.extend(no_dates)
			
			leave_dates = get_leave_dates(whole_month_days,no_dates_holidays)
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
			
			data = {
			'Name': user_name,
			'No of leaves' :  len(leave_dates),
			'Leave Dates' : leave_dates,
			'No of working days in August': no_working_days,
			'No of days worked': len(set(user_worked_as_per_working_days)),
			'For Month':'August',
			'Worked on weekend days or holidays':worked_on_weekend_days_holiday,
			'Dates Worked on weekend days':worked_weekend_days,
			'Time Worked on weekend days':extra_time_worked,
			"Total time to work":total_time_to_work,
			"Total time worked":total_time_worked,
			}
			data2[user_name] = data

		return JsonResponse(data2)
	else:
		return JsonResponse(
			{"Sorry dude you do not have permissions":"To access you nust be super user"})