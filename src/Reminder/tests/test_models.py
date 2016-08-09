import arrow
import logging
from datetime import datetime,time,timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError 

from Reminder.models import Reminder

logger = loggin.getLogger(__name__)

class ReminderTest(TestCase):

	message = "This is a test"
	now = datetime.now()
	date = now.date()
	time = now.time()
	delta = timedelta(minutes=10)
	positive_time = (now+delta).time()
	negative_time = (now-delta).time()
	email = "b4you0870@gmail.com"
	phone_number = "+919148912120"

	def create_reminder(self, message,date,time,email=None,phone_number=None):
		return Reminder.objects.create(message=message,date=date,time=time,email=email,phone_number=phone_number)

	def test_reminder_fail_creation(self):
		with self.assertRaises(ValidationError):
			obj = self.create_reminder(self.message,self.date,self.negative_time,self.email)
		logger.info("Fail test passed")

	def test_reminder_success_creation(self):
		obj = self.create_reminder(self.message,self.date,self.positive_time,self.email,'')
		self.assertTrue(isinstance(obj,Reminder))
		self.assertEqual(obj.__unicode__(),'Reminder #{0}'.format(obj.pk))
		self.assertTrue(obj.phone_number is None)
		self.assertTrue(obj.email is not None)
		logger.info("Positive test passed")

	def test_reminder_email_phone_number_both_present(self):
		obj = self.create_reminder(self.message,self.date,self.positive_time,self.email,self.phone_number)
		self.assertTrue(obj.email is not None)
		self.assertTrue(obj.phone_number is not None)
		logger.info("Email and phone number both present test passed")

	def test_reminder_email_phone_number_both_not_present(self):
		with self.assertRaises(ValidationError):
			obj = self.create_reminder(self.message,self.date,self.positive_time)
		logger.info("Email and phone number both not present test passed")

	def test_reminder_phone_number_present(self):
		obj = self.create_reminder(self.message,self.date,self.positive_time,'',self.phone_number)
		self.assertTrue(obj.phone_number is not None)
		self.assertTrue(obj.email is None)
		logger.info("Test passed")		


