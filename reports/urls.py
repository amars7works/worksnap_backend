from django.conf.urls import url
from reports import views

urlpatterns = [
	url(r'^$',views.home),
	url(r'^worksnaps_report/', views.worksnaps_report_html),
	url(r'^refesh_projects/',views.create_project,name='refresh the projects'),
    url(r'^refesh_users/',views.create_users,name='refresh the users'),
    url(r'^users_summary/',views.create_users_summary,name='users summary reports'),
    url(r'^add_holiday/',views.add_holiday_list,name='add holiday'),
    url(r'^user_report/',views.show_data_in_excel,name='user report')
	]