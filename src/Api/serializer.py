from rest_framework import serializers
from Reminder.models import Reminder

class ReminderSerializer(serializers.ModelSerializer):
	# email_id = serializers.EmailField()
	# date_time = serializers.DateTimeField()
	class Meta:
		model = Reminder
		fields = ('id','message','phone_number', 'email', 'date','time','completed')
