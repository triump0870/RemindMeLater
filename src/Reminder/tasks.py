from __future__ import absolute_import

from celery import task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import send_mail

from .models import Reminder
from twilio.rest import TwilioRestClient 
 
logger = get_task_logger(__name__)

@task()
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
	body = "{0}".format(reminder.message)
	try:
		client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN) 
	 
		client.messages.create(
			to=reminder.phone_number, 
			from_=settings.TWILIO_NUMBER, 
			body=body,  
		)
		logger.info("SMS Successfully send")
		return Reminder.objects.filter(id=reminder_id).update(completed=True)
	except Exception as e:
		logger.info("There is some problem while sending SMS\n",e)
		return e 


@task()
def send_mail_reminder(reminder_id):
	logger.info("Send Email")

	try:
		reminder = Reminder.objects.get(pk=reminder_id)
	except Reminder.DoesNotExist:
		return
	body = "{0}".format(reminder.message)
	try:
		send_mail("[Remind Me Later] App Notification",body,settings.DEFAULT_FROM_EMAIL,[reminder.email])
		
		logger.info("Email Successfully send")
		return Reminder.objects.filter(id=reminder_id).update(completed=True)
	except Exception as e:
		logger.info("There is some problem while sending email\n",e)
		return e

