from django.conf.urls import url
from .views import ApplyLeaveView, leave_details


urlpatterns = [
	url(r'^api/apply_leave/', ApplyLeaveView.as_view(), name='user apply for leave'),
	url(r'^api/leave/',leave_details.as_view()),
	url(r'^api/leave/(?P<id>\d+)/$', leave_details.as_view()),
]
