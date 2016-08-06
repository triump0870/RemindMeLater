from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.conf import settings
from .models import Reminder
from datetime import datetime
import arrow
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

@receiver(post_save, sender=Reminder)
def send_email_signal(sender,instance, created, **kwargs):
	if not created:
		return
	self = instance
	date_time = datetime.combine(self.date,self.time)
	reminder_time = arrow.get(date_time).replace(tzinfo=self.time_zone.zone)

	from .tasks import send_sms_reminder, send_mail_reminder
	result = ""
	if self.phone_number is not None:
		result = send_sms_reminder.apply_async((self.id,),eta=reminder_time)
		logger.info("SMS Result:",result)
		print "SMS result:",result.state

	if self.email is not None:
		result = send_mail_reminder.apply_async((self.id,),eta=reminder_time, serializer = 'json')
		logger.info("Email Result:",result)
		print "Email result:",result.state

	if result.id:
		instance.task_id = result.id
		instance.save()