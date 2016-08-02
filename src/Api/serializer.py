from rest_framework import serializers
from Reminder.models import Reminder

class ReminderSerializer(serializers.HyperlinkedModelSerializer):
	# email_id = serializers.EmailField()
	# date_time = serializers.DateTimeField()
	class Meta:
		extra_kwargs = {'url': {'view_name': 'api:reminder-detail'}} 
		model = Reminder
		fields = ('url','id','message','phone_number', 'email', 'time','created')

class ReminderDetailSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Reminder
		fields = ('url','id')