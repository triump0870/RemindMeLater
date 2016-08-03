from django.db import models
from django.core.validators import RegexValidator
import arrow
from timezone_field import TimeZoneField
from django.core.exceptions import ValidationError
from datetime import datetime

# Create your models here.
class Reminder(models.Model):
	task_id = models.CharField(max_length=50, blank=True, editable=False)
	message = models.CharField(max_length=500)
	date = models.DateField(editable=True)
	time = models.TimeField(editable=True)
	created = models.DateTimeField(auto_now_add=True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(max_length=15,validators=[phone_regex], blank=True, null=True)
	email = models.EmailField(max_length=100, blank=True, null=True)
	completed = models.BooleanField(default=False)
	time_zone = TimeZoneField(default='Asia/Kolkata')

	def __unicode__(self):
		return 'Reminder #{0}'.format(self.pk)

	def clean(self):
		"""Checks that appointments are not scheduled in the past"""
		date_time = datetime.combine(self.date,self.time)
		reminder_time = arrow.get(date_time).replace(tzinfo=self.time_zone.zone)
		
		if reminder_time < arrow.now():
			raise ValidationError('You cannot schedule an reminder for the past. Please check your time and time_zone')

	def schedule_reminder(self):
		"""
		Schedule a celery task to send the reminder
		"""
		date_time = datetime.combine(self.date,self.time)
		reminder_time = arrow.get(date_time).replace(tzinfo=self.time_zone.zone)

		from .tasks import send_sms_reminder
		result = send_sms_reminder.apply_async((self.pk,),eta=reminder_time,serializer = 'json')

		return result.id

	def save(self, *args, **kwargs):
		"""
		Now we need to do is ensure Django calls our 
		schedule_reminder method every time an Reminder object is created or updated.
		"""
		# Check if we have scheduled a celery task for this reminder before
		print 
		if self.task_id:
			#Revoke that remnder if its time has changed 
			celery_app.control.revoke(self.task_id)

		# save our reminder, which populates self.pk,
		# which is used in schedule_reminder

		# Schedule a reminder task for this reminder
		self.task_id = self.schedule_reminder()

		# Save our reminder again with the task_id
		print "Args:%s,Kwargs:%s"%(args,kwargs)
		print self.task_id
		super(Reminder, self).save(*args, **kwargs)




