from __future__ import unicode_literals

import sys
import json
import copy
import arrow
import logging
from datetime import datetime, time, timedelta

from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient

from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from reminders.models import Reminder
from apis.views import ReminderList, ReminderDetail
from apis.serializers import ReminderSerializer

logger = logging.getLogger(__name__)

if sys.version_info[:2] >= (3, 4):
    JSON_ERROR = 'JSON parse error - Expecting value:'
else:
    JSON_ERROR = 'JSON parse error - No JSON object could be decoded'


def delta_datetime(delta=0):
    time = datetime.now() + timedelta(minutes=delta)
    return time


def sanitise_json_error(error_dict):
    """
    Exact contents of JSON error messages depend on the installed version
    of json.
    """
    ret = copy.copy(error_dict)
    chop = len(JSON_ERROR)
    ret['detail'] = ret['detail'][:chop]
    return ret


class ReminderApiTestCase(TestCase):
    """
    Test case covers API for getting details of the reminders such as:
    GET /api/reminders
    GET /api/reminders/<pk>

    Test case covers API for submitting new reminders:
    POST /api/reminders
    """

    def setUp(self):
        self.message = "This is a Test"
        self.phone_number = "+919148912120"
        self.email = "b4you0870@gmail.com"
        self.positive_date = delta_datetime().date().isoformat()
        self.negative_date = delta_datetime(-24 * 60).date().isoformat()
        self.negative_time = delta_datetime(-10).time().isoformat()
        self.positive_time = delta_datetime(+10).time().isoformat()

    def test_get_reminder_list(self):
        response = self.client.get('/apis/reminders', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_reminder_details(self):
        expected_results = {
            'id': 1,
            'message': 'This is a Test',
            'email': 'b4you0870@gmail.com',
            'phone_number': '+919148912120'
        }

        Reminder.objects.create(
            date=datetime.now().date(),
            time=(datetime.now() + timedelta(minutes=10)).time(),
            **expected_results)

        response = self.client.get('/apis/reminders/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_results['id'], response.data['id'])
        self.assertEqual(expected_results['message'], response.data['message'])
        self.assertEqual(expected_results['email'], response.data['email'])
        self.assertEqual(expected_results['phone_number'], response.data['phone_number'])

    def test_get_non_existent_reminder_details(self):
        response = self.client.get('/apis/reminders/1')
        self.assertEqual(response.status_code, 404)

    def test_400_parse_error(self):
        response = self.client.post(
            '/apis/reminders', 'f00bar', content_type='application/json')
        expected = {
            'detail': JSON_ERROR
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(sanitise_json_error(response.data), expected)

    def test_reminder_with_blank_fields(self):
        response = self.client.post(
            '/apis/reminders', {})
        serializer = ReminderSerializer(data=response.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(serializer.is_valid())

    def test_reminder_with_blank_phone_and_email_fields(self):
        response = self.client.post(
            '/apis/reminders',
            {"message": self.message, "date": self.positive_date, "time": self.positive_time})
        serializer = ReminderSerializer(data=response.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(response.data['phone_number'][0], "Phone number was not provided")
        self.assertEqual(response.data['email'][0], "Email was not provided")

    def test_reminder_with_invalid_phone_number(self):
        response = self.client.post(
            '/apis/reminders',
            {"message": self.message, "date": self.positive_date,
             "time": self.positive_time, "phone_number": "9148912120"})
        serializer = ReminderSerializer(data=response.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            response.data['phone_number'][0], "Phone number must be entered in the format: '+919876543210'.")

    def test_reminder_with_invalid_email_field(self):
        response = self.client.post(
            '/apis/reminders',
            {"message": self.message, "date": self.positive_date, "time": self.positive_time, "email": "abc.com"})
        serializer = ReminderSerializer(data=response.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(response.data['email'][0], "Enter a valid email address.")

    def test_reminder_with_date_in_past(self):
        response = self.client.post(
            '/apis/reminders',
            {"message": "Hehere", "date": self.negative_date, "time": self.positive_time, "email": self.email})
        serializer = ReminderSerializer(data=response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['date']['date'], "Can't place reminder in the past")

    def test_reminder_with_time_in_past(self):
        response = self.client.post(
            '/apis/reminders',
            {"message": self.message, "date": self.positive_date, "time": self.negative_time, "email": self.email})
        serializer = ReminderSerializer(data=response.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(response.data['time']['time'], "Can't place reminder in the past", msg="Passed")

    def test_reminder_with_all_fields(self):
        response = self.client.post(
            '/apis/reminders',
            {"message": self.message, "date": self.positive_date, "time": self.positive_time, "email": self.email,
             "phone_number": self.phone_number})
        serializer = ReminderSerializer(data=response.data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(serializer.is_valid())
