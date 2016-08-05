from django.db import models
from django.core.validators import RegexValidator
import arrow
from timezone_field import TimeZoneField
from django.core.exceptions import ValidationError
from datetime import datetime


NOTIFICATION_CHANNEL_CHOICE = (
	(1, "PHONE NUMBER"),
	(2, "EMAIL"),
	)

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
	channel = models.CharField(max_length=1,choices=NOTIFICATION_CHANNEL_CHOICE, default=2,blank=True,null=False)

	def __unicode__(self):
		return 'Reminder #{0}'.format(self.pk)

	def save(self, *args, **kwargs):
		"""
		Now we need to do is ensure Django calls our 
		schedule_reminder method every time an Reminder object is created or updated.
		"""
		if self.email == u'':
			self.email = None
		if self.phone_number == u'':
			self.phone_number = None

		email,phone_number = self.email,self.phone_number
		choice = 2
		date_time = datetime.combine(self.date,self.time)
		reminder_time = arrow.get(date_time).replace(tzinfo=self.time_zone.zone)

		if reminder_time < arrow.now():
			raise ValidationError({"DateTime Error":"You cannot schedule an reminder for the past. Please check you date, 	time and time_zone"})
		
		if email is not None  and phone_number is not None :
			raise ValidationError({"Email and Phone Number Error":"You can't provide email and phone_number both at the same time"})
		
		if email is None and phone_number is None:
			raise ValidationError({"email":"Email field was empty","phone_number":"Phone number was empty"})

		if phone_number is not None:
			choice = 1

		if choice:
			self.channel = choice
			super(Reminder,self).save(*args,**kwargs)




