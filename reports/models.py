from django.db import models
from django.contrib.auth.models import User
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

class UserDailyReport(models.Model):
	username = models.CharField(max_length=100)
	cretaed_at = models.DateField()
	what_was_done_this_day = models.TextField()
	what_is_your_plan_for_the_next_day = models.TextField()
	what_are_your_blockers = models.TextField()
	do_you_have_enough_tasks_for_next_three_days = models.TextField()
	if_you_get_stuck_are_you_still_able_to_work_on_something_else = models.TextField()

	def __str__(self):
		return "%s"%(self.username)

class UserProfile(models.Model):
	user_name = models.CharField(max_length=100)
	user_email = models.EmailField(max_length=70,blank=True)
	password = models.TextField()
	joined_date = models.DateField()

	def __str__(self):
		return "%s"%(self.user_name)

class RemainingAccruedLeaves(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	remaining_leaves = models.FloatField()
	till_date = models.DateField(null=True)
	def __str__(self):
		return "%s"%(self.user)

class UserXmldata(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateField()
	xml_data = models.TextField()

	def __str__(self):
		return "%s"%(self.user)

class TotalLeaves(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	data = models.TextField()

	def __str__(self):
		return "%s"%(self.user)
