import re
import arrow
from datetime import datetime
import logging

from rest_framework import serializers

from reminders.models import Reminder

logger = logging.getLogger(__name__)


class ReminderSerializer(serializers.ModelSerializer):

    def validate_date(self, date):
        if date < datetime.now().date():
            raise serializers.ValidationError(
                {"date": "Can't place reminder in the past"})
        return date

    def validate_time(self, time):
        if time < datetime.now().time():
            raise serializers.ValidationError(
                {"time": "Can't place reminder in the past"})
        return time

    def validate(self, data):
        phone_number = data.get('phone_number')
        email = data.get('email')

        if phone_number is not None and phone_number != '':
            regex = re.compile('^\+1?\d{12,15}$')
            phone = regex.match(phone_number)

            if phone is None:
                raise serializers.ValidationError(
                    {"phone_number": "Phone number must be entered in the format: '+919876543210'."})

        if not email and not phone_number:
            raise serializers.ValidationError(
                {"phone_number": "Phone number was not provided", "email": "Email was not provided"})
        return data

    class Meta:
        model = Reminder
        fields = (
            'id',
            'message',
            'phone_number',
            'email',
            'date',
            'time',
            'completed',
        )
        extra_kwargs = {
            "completed": {"read_only": True}
        }
