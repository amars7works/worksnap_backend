from django.db import models
from django.contrib.auth.models import User


class BankAccountNumbers(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	account_number = models.CharField(max_length=200)
	IFSC_code = models.CharField(max_length=100)

	def __str__(self):
		return "%s"%(self.user)	

class Salary(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	Salary = models.CharField(max_length=50)

	def __str__(self):
		return "%s"%(self.user)	
