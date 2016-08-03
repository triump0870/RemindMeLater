from __future__ import unicode_literals
from mock import patch, Mock
from django.core.exceptions import MiddlewareNotUsed
import unittest
import os

from twilio_notifications.middleware import TwilioNotificationsMiddleware
from twilio_notifications.middleware import MessageClient, load_twilio_config
from twilio_notifications.middleware import MESSAGE


class TestNotificationMiddleware(unittest.TestCase):

    @patch('twilio_notifications.middleware.load_twilio_config')
    @patch('twilio_notifications.middleware.load_admins_file')
    def test_notify_on_exception(self, mock_load_admins_file,
                                 mock_load_twilio_config):

        # Given
        admin_number = '+919148912120'
        sending_number = '+919148912120'

        mock_load_admins_file.return_value = [
            {'name': 'Some name', 'phone_number': admin_number}
        ]

        mock_message_client = Mock(spec=MessageClient)
        mock_load_twilio_config.return_value = (sending_number,'ACec857ee47c600c9595cca4b05754b8da', 'cd2143dcb91ca678ddbbeb2fe81d987c')

        middleware = TwilioNotificationsMiddleware()
        middleware.client = mock_message_client

        exception_message = 'Some exception message'

        # When
        middleware.process_exception(None, 'Some exception message')

        # Then
        mock_message_client.send_message.assert_called_once_with(
            MESSAGE % exception_message, admin_number
        )

    def test_correct_load_twilio_config(self):
        os.environ['TWILIO_ACCOUNT_SID'] = 'ACec857ee47c600c9595cca4b05754b8da'
        os.environ['TWILIO_AUTH_TOKEN'] = 'cd2143dcb91ca678ddbbeb2fe81d987c'
        os.environ['TWILIO_NUMBER'] = '919148912120'

        try:
            load_twilio_config()
        except MiddlewareNotUsed:
            self.fail('MiddlewareNotUsed when correctly configured')

    def test_fail_load_twilio_config(self):
        os.environ['TWILIO_ACCOUNT_SID'] = 'ACec857ee47c600c9595cca4b05754b8dw'
        os.environ['TWILIO_AUTH_TOKEN'] = 'cd2143dcb91ca678ddbbeb2fe81d987r'
        os.environ.pop('TWILIO_NUMBER')

        with self.assertRaises(MiddlewareNotUsed):
            load_twilio_config()