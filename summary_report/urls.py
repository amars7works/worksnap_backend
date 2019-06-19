from django.conf.urls import url
from summary_report.views import *

urlpatterns = [
		url(r'^export/', show_data_in_excel, name="monthly summary_report"),
		# url(r'^test/', monthly_amount_calc, name="monthly summary_report")
]