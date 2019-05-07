from django.conf.urls import url
from .views import ApplyLeaveView, leave_details


urlpatterns = [
	url('apply_leave/', ApplyLeaveView.as_view(), name='user apply for leave'),
	url('leave/',leave_details.as_view()),
]
