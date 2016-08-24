from __future__ import absolute_import

from celery import task
from twilio.rest import TwilioRestClient
from celery.utils.log import get_task_logger

from django.conf import settings
from django.core.mail import send_mail

from .models import Reminder

logger = get_task_logger(__name__)

@task()
def reminder_task(reminder_id):
    """
    Semd Reminder based on the provided channel.
    """
    try:
        reminder = Reminder.objects.get(pk=reminder_id)
        if reminder.phone_number:
            send_sms_reminder(reminder)

        if reminder.email:
            send_email_reminder(reminder)

        return "SUCCESS"

    except Reminder.DoesNotExist:
        return "FAILED"


def send_sms_reminder(reminder):
    """
    Send a Reminder to phone using Twillo SMS.
    """
    logger.info("Send SMS")
    body = "{0}".format(reminder.message)

    try:
        client = TwilioRestClient(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            to=reminder.phone_number,
            from_=settings.TWILIO_NUMBER,
            body=body,
        )
        logger.info("SMS Successfully send")
        return Reminder.objects.filter(id=reminder.id).update(completed=True)

    except Exception as e:
        logger.info("There is some problem while sending SMS\n", e)
        return e


def send_email_reminder(reminder):
    """
    Send a Reminder to email address using Amazon SES.
    """
    logger.info("Send Email")
    body = "{0}".format(reminder.message)

    try:
        send_mail("[Remind Me Later] App Notification", body,
                  settings.DEFAULT_FROM_EMAIL, [reminder.email])
        logger.info("Email Successfully send")
        return Reminder.objects.filter(id=reminder.id).update(completed=True)

    except Exception as e:
        logger.info("There is some problem while sending email\n", e)
        return e
