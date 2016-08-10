import arrow
import logging
from datetime import datetime,time,timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError 

from Reminder.models import Reminder

logger = logging.getLogger(__name__)

class ReminderTest(TestCase):

	MESSAGE = "This is a test"
	NOW = datetime.now()
	DATE = NOW.date()
	TIME = NOW.time()
	DELTA = timedelta(minutes=10)
	POSITIVE_TIME = (NOW+DELTA).time()
	NEGATIVE_TIME = (NOW-DELTA).time()
	EMAIL = "b4you0870@gmail.com"
	PHONE_NUMBER = "+919148912120"

	def create_reminder(self, message,date,time,email=None,phone_number=None):
		return Reminder.objects.create(message=message,date=date,time=time,email=email,phone_number=phone_number)

	def test_reminder_fail_creation(self):
		with self.assertRaises(ValidationError):
			obj = self.create_reminder(self.MESSAGE,self.DATE,self.NEGATIVE_TIME,self.EMAIL)
		logger.info("Fail test passed")

	def test_reminder_success_creation(self):
		obj = self.create_reminder(self.MESSAGE,self.DATE,self.POSITIVE_TIME,self.EMAIL,'')
		self.assertTrue(isinstance(obj,Reminder))
		self.assertEqual(obj.__unicode__(),'Reminder #{0}'.format(obj.pk))
		self.assertTrue(obj.phone_number is None)
		self.assertTrue(obj.email is not None)
		self.assertTrue(obj.task_id is not None)
		logger.info("Positive test passed")

	def test_reminder_email_phone_number_both_present(self):
		obj = self.create_reminder(self.MESSAGE,self.DATE,self.POSITIVE_TIME,self.EMAIL,self.PHONE_NUMBER)
		self.assertTrue(obj.email is not None)
		self.assertTrue(obj.phone_number is not None)
		logger.info("Email and phone number both present test passed")

	def test_reminder_email_phone_number_both_not_present(self):
		with self.assertRaises(ValidationError):
			obj = self.create_reminder(self.MESSAGE,self.DATE,self.POSITIVE_TIME)
		logger.info("Email and phone number both not present test passed")

	def test_reminder_phone_number_present(self):
		obj = self.create_reminder(self.MESSAGE,self.DATE,self.POSITIVE_TIME,'',self.PHONE_NUMBER)
		self.assertTrue(obj.phone_number is not None)
		self.assertTrue(obj.email is None)
		logger.info("Test passed")		


