from django.conf.urls import url
from .views import ApplyLeaveView, leave_details
from reports_2.views import *


urlpatterns = [
	url(r'^apply_leave/', ApplyLeaveView.as_view(), name='user apply for leave'),
	url(r'^get_requests/',leave_details.as_view()),
	url(r'^get_leave_status/', leavestatus, name = "leave"),
]
