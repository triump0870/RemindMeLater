from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.conf import settings
import logging
from .models import Reminder
from datetime import datetime
import arrow
logger = logging.getLogger("sentry")

@receiver(post_save, sender=Reminder)
def send_email_signal(sender,instance, created, **kwargs):
	if not created:
		return
	self = instance
	date_time = datetime.combine(self.date,self.time)
	reminder_time = arrow.get(date_time).replace(tzinfo=self.time_zone.zone)

	from .tasks import send_sms_reminder, send_mail_reminder
	result = ""
	if self.channel == 1:
		result = send_sms_reminder.apply_async((self.id,),eta=reminder_time)

	elif self.channel == 2:
		result = send_mail_reminder.apply_async((self.id,),eta=reminder_time, serializer = 'json')

	else:
		raise ValidationError("Neither email nor phone_number was provided")

	if result.id:
		instance.task_id = result.id
		instance.save()