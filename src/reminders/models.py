from __future__ import absolute_import

import arrow
import logging
from datetime import datetime
from timezone_field import TimeZoneField

from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from RemindMeLater.settings import celery_app

logger = logging.getLogger(__name__)

# Create your models here.


class Reminder(models.Model):
    task_id = models.CharField(max_length=50, blank=True, editable=False)
    message = models.CharField(max_length=500)
    date = models.DateField(editable=True)
    time = models.TimeField(editable=True)
    created = models.DateTimeField(auto_now_add=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{12,15}$',
        message="Phone number must be entered in the format: '+919876543210'.",
        code='Invalid Phone number')
    phone_number = models.CharField(
        max_length=15,
        validators=[phone_regex],
        blank=True,
        null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    completed = models.BooleanField(default=False, editable=False)
    time_zone = TimeZoneField(default='Asia/Kolkata')

    def __unicode__(self):
        return 'Reminder #{0}'.format(self.pk)

    def schedule_reminder(self):
        """
        Creates the celery async tasks.
        """
        date_time = datetime.combine(self.date, self.time)
        reminder_time = arrow.get(date_time).replace(
            tzinfo=self.time_zone.zone)
        from .tasks import reminder_task

        result = reminder_task.apply_async((self.pk,), eta=reminder_time, serializer='json')
        logger.info(result)

        return result.id

    def save(self, *args, **kwargs):
        """
        Now we need to do is ensure Django calls our
        schedule_reminder method every time an Reminder object is created or updated.
        """
        if self.task_id:
            celery_app.control.revoke(self.task_id)

        super(Reminder, self).save(*args, **kwargs)

        if self.id and not self.completed:
            if self.email == u'':
                self.email = None
            if self.phone_number == u'':
                self.phone_number = None

            email, phone_number = self.email, self.phone_number
            choice = 2
            date_time = datetime.combine(self.date, self.time)
            reminder_time = arrow.get(date_time).replace(
                tzinfo=self.time_zone.zone)

            if reminder_time < arrow.now():
                raise ValidationError(
                    {"DateTime Error": "You cannot schedule an reminder for the past.\
                    Please check you date, time and time_zone"})

            if email is None and phone_number is None:
                raise ValidationError(
                    {"email": "Email field was empty", "phone_number": "Phone number was empty"})

            self.task_id = self.schedule_reminder()

            
