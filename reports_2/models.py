from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BankAccountNumber(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	account_number = models.CharField(max_length=200)

	def __str__(self):
		return "%s"%(self.user)	
	
class ApplyLeave(models.Model):
	TYPE_OF_REQUEST_CHOICE = (
		("Sick_Leave","Sick Leave Request"),
		("Vacational_Leave","Vacation Leave Request"),
		("General_Leave","General Leave Request"),
		("Night_Shift","Night Shift Request"),
		("Work_From_Home","WorkFromHome Request"),
		)
	leave_status_types = (
		("Pending","Pending"),
		("Approved","Approved"),
		("Rejected","Rejected"),
		)
	
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateField()
	leave_start_date = models.DateTimeField()
	leave_end_date = models.DateTimeField()
	apply_reason = models.TextField(null=True,blank=True)
	# leave_status = models.BooleanField(default=False)
	leave_status = models.CharField(choices = leave_status_types, default="Pending", max_length = 25)
	denied_reason = models.TextField(null=True,blank=True)
	Type_of_Request = models.CharField(
        choices = TYPE_OF_REQUEST_CHOICE,
        max_length = 25)

	def __str__(self):
		return "%s"%(self.user)	

class WorkFromHome(models.Model):
	work_type = (
		("Work From Home","Work From Home"),
		("Work From Office","Work From Office")
		)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateField()
	select_work_type = models.CharField(choices = work_type,max_length = 25)

	def __str__(self):
		return "%s"%(self.user)
