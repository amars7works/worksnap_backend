from django.conf.urls import url
from auth import views
from worksnaps_report.schema import schema

urlpatterns = [
	url(r'^auth_status/',views.check_authentication_status, name='auth_status'),
]
# url(r'^register_form/', views.registration_html,name='register_form'),
# url(r'^summary_report/', views.usersummary.as_view(),name='summary_report'),
