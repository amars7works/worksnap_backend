from rest_framework import serializers
from reports.models import ProjectsList,\
							UsersList,\
							UsersSummaryReport,\
							HolidayList,\
							UserDailyReport,\
							UserProfile,\
							RemainingAccruedLeaves

class UsersSummaryReportSerializers(serializers.ModelSerializer):
	class Meta:
		model = UsersSummaryReport
		fields = ('user_name', 'date', 'duration',
                  'project_name')

