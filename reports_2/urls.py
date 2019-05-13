from django.conf.urls import url
from .views import ApplyLeaveView, leave_details


urlpatterns = [
	url(r'^apply_leave/', ApplyLeaveView.as_view(), name='user apply for leave'),
	url(r'^get_requests/',leave_details.as_view()),
	# url(r'^get_requests/(?P<id>\d+)/$', leave_details.as_view()),
]
