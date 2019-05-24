from django.conf.urls import url
from reports import views
from reports import report
from graphene_django.views import GraphQLView
from worksnaps_report.schema import schema

urlpatterns = [
	url(r'^$',views.login_view,name='login'),
    url(r'^graphql', GraphQLView.as_view(graphiql=True,schema=schema)),
	url(r'^logout$',views.logout_view,name='logout'),
	url(r'^home',views.home,name='home'),
	url(r'^worksnaps_report/', views.worksnaps_report_html,name='worksnaps_report'),
	url(r'^refesh_projects/',views.create_project,name='refresh the projects'),
    url(r'^refesh_users/',views.create_users,name='refresh the users'),
    url(r'^users_summary/',views.create_users_summary,name='users summary reports'),
    url(r'^add_holiday/',views.add_holiday_list,name='add holiday'),
    url(r'^user_report/',views.show_data_in_excel,name='user report'),
    url(r'^daily_report/', report.daily_report.as_view(),
    	name='create daily report'),
    url(r'^user_register/', views.user_register,
        name='user_register'),
    url(r'^register_form/', views.registration_html,name='register_form'),
     url(r'^summary_report/', views.usersummary.as_view(),name='summary_report'),
]

# url(r'^daily_report/', views.daily_report_html,name='daily_report'),