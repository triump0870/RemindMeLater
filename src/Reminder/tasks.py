from __future__ import absolute_import

from celery import shared_task
from celery.utils.log import get_task_logger

from django.conf import settings

import arrow

from twilio.rest import TwilioRestClient

from .models import Reminder

client = TwilioRestClient()
logger = get_task_logger(__name__)

@shared_task
def send_sms_reminder(reminder_id):
	"""
	Send a Reminder to phone using Twillo SMS.
	"""
	logger.info("Send SMS")
	# Get the reminder id from the database
	try:
		reminder = Reminder.objects.get(pk=reminder_id)
	except Reminder.DoesNotExist:
		# The reminder we were trying to remind someone about
		# has been deleted, so we don't need to do anything
		return
	reminder_time = arrow.get(reminder.time)
	body = "{0}".format(reminder.message)

	message = client.messages.create(
		body = body,
		to = reminder.phone_number,
		from_ = settings.TWILIO_NUMBER
	)

