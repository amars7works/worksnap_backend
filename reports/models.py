from django.db import models

# Create your models here.

class ProjectsList(models.Model):
	project_id = models.CharField(max_length=25)
	project_name = models.CharField(max_length=100)
	project_description = models.TextField(null=True)
	project_status = models.CharField(max_length=25)

	def __str__(self):
		return "%s"%(self.project_name)

class UsersList(models.Model):
	user_id = models.CharField(max_length=25)
	user_email = models.CharField(max_length=100)
	user_first_name = models.CharField(max_length=25)
	user_last_name = models.CharField(max_length=25)
	user_login_as = models.CharField(max_length=25)

	def __str__(self):
		return "%s"%(self.user_email)

class UsersSummaryReport(models.Model):
	user_name = models.CharField(max_length=100)
	user_id = models.CharField(max_length=10)
	date = models.DateField()
	duration = models.CharField(max_length=25)
	project_name = models.CharField(max_length=200)

	def __str__(self):
		return "%s,%s"%(self.date,self.user_name)

class HolidayList(models.Model):
	holiday_date = models.DateField()
	day = models.CharField(max_length=20)
	holiday_description = models.TextField(null=True)

	def __str__(self):
		return "%s"%(self.holiday_date)
