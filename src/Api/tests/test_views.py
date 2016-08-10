from __future__ import unicode_literals

import sys
import json
import arrow
import logging
from datetime import datetime,time,timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError 

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from Api.serializers import ReminderSerializer
from Api.views import reminder_list, reminder_detail
from Reminder.models import Reminder

logger = logging.getLogger(__name__)

DELTA = lambda x:timedelta(minutes=x)
NOW = arrow.now()
POSITIVE_DATE =  NOW.date().isoformat()
NEGATIVE_DATE = (NOW+DELTA(-24*60)).date().isoformat()
POSITIVE_TIME = (NOW+DELTA(10)).time().isoformat()
NEGATIVE_TIME = (NOW + DELTA(-1)).time().isoformat()
MESSAGE = "This is a test"
EMAIL = "b4you0870@gmail.com"
PHONE_NUMBER = "+919148912120"

factory = APIRequestFactory()


class APITestCase(TestCase):
    """
    Testing the APIs
    """

    def test_reminder_list(self):
        response = self.client.get('/apis/reminders',follow=True)
        self.assertEqual(response.status_code, 200)

    def test_reminder_with_blank_fields(self):
    	response = self.client.post('/apis/reminders', {})
    	serializer = ReminderSerializer(data=response.data)
    	self.assertEqual(response.status_code, 400)
    	self.assertFalse(serializer.is_valid())

    def test_reminder_with_blank_phone_and_email_fields(self):
    	response = self.client.post('/apis/reminders',{"message":MESSAGE,"date":POSITIVE_DATE,"time":POSITIVE_TIME})
    	serializer = ReminderSerializer(data=response.data)
    	self.assertEqual(response.status_code, 400)
    	self.assertFalse(serializer.is_valid())

    def test_reminder_with_invalid_phone_number(self):
    	response = self.client.post('/apis/reminders',{"message":MESSAGE,"date":POSITIVE_DATE,"time":POSITIVE_TIME,"phone_number":"9148912120"})
        serializer = ReminderSerializer(data=response.data)
    	self.assertEqual(response.status_code, 400)
    	self.assertFalse(serializer.is_valid())
        self.assertEqual(response.data['phone_number'][0],"Phone number must be entered in the format: '+919876543210'. Up to 15 digits allowed.")

    def test_reminder_with_invalid_email_field(self):
    	response = self.client.post('/apis/reminders',{"message":MESSAGE,"date":POSITIVE_DATE,"time":POSITIVE_TIME,"email":"abc.com"})
        serializer = ReminderSerializer(data=response.data)
    	self.assertEqual(response.status_code, 400)
    	self.assertFalse(serializer.is_valid())
        self.assertEqual(response.data['email'][0],"Enter a valid email address.")

    def test_reminder_with_date_in_past(self):
    	response = self.client.post('/apis/reminders',{"message":"Hehere","date":NEGATIVE_DATE,"time":POSITIVE_TIME,"email":EMAIL})
        serializer = ReminderSerializer(data=response.data)
    	self.assertEqual(response.status_code, 400)
    	self.assertEqual(response.data['date']['date'],"Can't place reminder in the past")

    def test_reminder_with_time_in_past(self):
    	response = self.client.post('/apis/reminders',{"message":MESSAGE,"date":POSITIVE_DATE,"time":NEGATIVE_TIME,"email":EMAIL})
    	serializer = ReminderSerializer(data=response.data)
    	self.assertEqual(response.status_code, 400)
    	self.assertFalse(serializer.is_valid())
    	self.assertEqual(response.data['time']['time'],"Can't place reminder in the past",msg="Passed")

    def test_reminder_with_all_fields(self):
        response = self.client.post('/apis/reminders',{"message":MESSAGE,"date":POSITIVE_DATE,"time":POSITIVE_TIME,"email":EMAIL})
        serializer = ReminderSerializer(data=response.data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(serializer.is_valid())
        self.assertIn('task_id',response.data)