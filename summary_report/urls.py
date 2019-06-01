from django.conf.urls import url
from summary_report.views import *

urlpatterns = [
		url(r'^export/', show_data_in_excel, name="monthly summary_report"),
		# url(r'^test/', salary_perday, name="monthly summary_report")
]