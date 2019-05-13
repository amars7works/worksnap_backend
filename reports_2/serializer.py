from rest_framework import serializers
from reports_2.models import ApplyLeave

class applyleaveserializer(serializers.ModelSerializer):

	class Meta:
		model = ApplyLeave
		fields = '__all__'
	
	def update(self, instance, validated_data):
		instance.user = validated_data.get('user', instance.user)
		# instance.created_at = validated_data.get('created_at', instance.created_at)
		# instance.leave_start_date = validated_data.get('leave_start_date', instance.leave_start_date)
		# instance.leave_end_date = validated_data.get('leave_end_date', instance.leave_end_date)
		# instance.apply_reason = validated_data.get('apply_reason', instance.apply_reason)
		instance.leave_status = validated_data.get('leave_status', instance.leave_status)
		instance.denied_reason = validated_data.get('denied_reason', instance.denied_reason)
		# instance.Type_of_Request = validated_data.get('Type_of_Request', instance.Type_of_Request)
		instance.save()
		return instance

