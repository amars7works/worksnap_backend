from django.db import models
from datetime import datetime

class TimeEntry(models.Model):
	entry_id = models.CharField(max_length=50)
	type = models.CharField(max_length=10)
	from_timestamp = models.DateTimeField(default=datetime.now)
	logged_timestamp = models.DateTimeField(default=datetime.now)
	duration = models.CharField(max_length=4)
	project_id = models.CharField(max_length=20)
	user_id = models.CharField(max_length=20)
	user_ip = models.CharField(max_length=20)

	def __str__(self):
                return "%s"%(self.user_id)

class WhitelistIpAddress(models.Model):
	ipaddress = models.CharField(max_length=20)

	def __str__(self):
		return "%s"%(self.ipaddress)
