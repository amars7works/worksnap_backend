from django.conf.urls import url
from s7_auth import views
from worksnaps_report.schema import schema

urlpatterns = [
	url(r'^user/login/', views.Login.as_view(),name='login_user'),
	url(r'^user/logout/',views.Logout.as_view(), name='logout'),
	url(r'^user/auth_status/',views.user_authentication_status, name='auth_status'),
]
# url(r'^register_form/', views.registration_html,name='register_form'),
# url(r'^summary_report/', views.usersummary.as_view(),name='summary_report'),
