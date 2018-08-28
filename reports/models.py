from django.db import models

# Create your models here.

class ProjectsList(models.Model):
	project_id = models.CharField(max_length=25)
	project_name = models.CharField(max_length=100)
	project_description = models.TextField(null=True)
	project_status = models.CharField(max_length=25)

	def __str__(self):
		return "%s"%(self.project_name)

