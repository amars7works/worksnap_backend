from django.conf.urls import url
from reports_2.views import *


urlpatterns = [
	# url(r'^s7_login/', Login.as_view(),name='login_user'),
	# url(r'^logout/',Logout.as_view(), name='logout'),
	url(r'^apply_leave/', ApplyLeaveView.as_view(), name='user apply for leave'),
	url(r'^get_requests/',leave_details.as_view()),
	url(r'^get_leave_status/', leavestatus, name = "leave status"),
	# url(r'^emp_list/', emp_details.as_view(), name='Employee List'),
	url(r'^user_daily_report/', DailyReportView.as_view(), name='Daily Report'),
	url(r'^leave_approved_list/', Leave_Approved_List.as_view(), name='Approved List'),
	url(r'^leave_rejected_list/', Leave_Rejected_List.as_view(), name='Rejected List'),	
	url(r'^get_emp_list/', emp_details.as_view(), name='Employee List'),
	url(r'^present_or_leave_list/', emp_list.as_view(), name='working emp List'),
	url(r'^emp_name/', emp_names_list.as_view(), name='Employee Names'),
	url(r'^workfromhome/', WorkFromHomes.as_view(), name='Work From Home'),
	# (?# url(r'^leaves_filter/', totalleaves.as_view(), name='leaves filter'),)
	url(r'^daily_reportss/', daily_reportss.as_view(), name='daily_reportss'),


]
