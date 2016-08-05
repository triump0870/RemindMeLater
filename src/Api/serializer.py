from rest_framework import serializers
from Reminder.models import Reminder
import arrow
from datetime import datetime

class ReminderSerializer(serializers.ModelSerializer):
	# email_id = serializers.EmailField()
	def validate_date(self,date):
		if date < datetime.now().date():
			raise serializers.ValidationError({"date":"Can't place reminder in the past"})
		return date

	def validate_time(self,time):
		if time < datetime.now().time():
			raise serializers.ValidationError({"time":"Can't place reminder in the past"})
		return time


	def validate(self, data):
		phone_number,email = data['phone_number'],data['email']
		if not email and not phone_number:
			raise serializers.ValidationError({"phone_number":"Phone number was not provided","email":"Email was not provided"})
		if (email and phone_number):
			raise serializers.ValidationError({"Email and Phone Number":"Provide either phone_number or email. Not both at the same time")
		return data


	class Meta:
		model = Reminder
		fields = ('id','task_id','message','phone_number', 'email', 'date','time','completed','channel')

	

