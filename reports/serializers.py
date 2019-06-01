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
		fields = ('user_id','user_name', 'date', 'duration',)

class UserListSerializers(serializers.ModelSerializer):
	class Meta:
		model = UsersList
		fields = ('user_id','user_email', 'user_first_name', 'user_last_name',)