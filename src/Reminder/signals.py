from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import logging
from .models import Reminder
from datetime import datetime
import arrow
logger = logging.getLogger("sentry")

@receiver(post_save, sender=Reminder)
def send_email_signal(sender,instance, created, **kwargs):
	if created:
		print "Post save called"
		self = instance
		date_time = datetime.combine(self.date,self.time)
		reminder_time = arrow.get(date_time).replace(tzinfo=self.time_zone.zone)

		from .tasks import send_sms_reminder, send_mail_reminder
		# result=''
		# result = send_sms_reminder.apply_async((self.pk,),eta=reminder_time,serializer = 'json')
		# else:
		result = send_mail_reminder.apply_async((self.id,),eta=reminder_time, serializer = 'json')
		instance.task_id = result.id
		instance.save()