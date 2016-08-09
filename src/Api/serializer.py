from datetime import datetime
import arrow
import re

from rest_framework import serializers

from Reminder.models import Reminder

class ReminderSerializer(serializers.ModelSerializer):
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
		if phone_number is not None:
			regex =re.compile('^\+1?\d{12,15}$')
			phone = regex.match(phone_number)
			if phone is None:
				raise serializers.ValidationError({"phone_number":"Phone number must be entered in the format: '+919876543210'. Up to 15 digits allowed."})
		
		if not email and not phone_number:
			raise serializers.ValidationError({"phone_number":"Phone number was not provided","email":"Email was not provided"})
		
		return data

	class Meta:
		model = Reminder
		fields = ('id','task_id','message','phone_number', 'email', 'date','time','completed')

	

