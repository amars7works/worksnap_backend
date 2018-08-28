from django.contrib import admin
from reports.models import ProjectsList
# Register your models here.

class ProjectsListAdmin(admin.ModelAdmin):
	list_display = ('project_name','project_id','project_status')

	search_fields = ('project_name','project_id',)

admin.site.register(ProjectsList,ProjectsListAdmin)