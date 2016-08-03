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

	# def validate(self, data):
	# 	print "Date:",data
	# 	if 'time_zone' not in data:
	# 		time_zone = 'local'
	# 	date_time = datetime.combine(data['date'],data['time'])
	# 	print "DAte_time:",date_time

	# 	date = arrow.get(date_time).replace(tzinfo=time_zone)
	# 	if date < arrow.now():
	# 		raise serializers.ValidationError({"date":"Can't place reminder in the past")
	# 	print "date:",date
	# 	return data


	class Meta:
		model = Reminder
		fields = ('id','task_id','message','phone_number', 'email', 'date','time','completed')

	

