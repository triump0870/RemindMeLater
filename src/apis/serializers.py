import re
import arrow
from datetime import datetime
import logging

from rest_framework import serializers

from reminders.models import Reminder

logger = logging.getLogger(__name__)


class ReminderSerializer(serializers.ModelSerializer):
    """
    The representation of the serializer will be,

    "id": 7,
    "message": "The test message",
    "phone_number": null,
    "email": "b4you0870@gmail.com",
    "date": "2016-08-15",
    "time": "18:05:00",
    "completed": false

    The editable fields are `message`, `phone_number`, `email`, `date` and `time`.
    Non editable fields are `id` and `completed`.

    """
    def validate_date(self, date):
        """
        Checks the date field if it's in past.
        """
        if date < datetime.now().date():
            raise serializers.ValidationError(
                {"date": "Can't place reminder in the past"})
        return date

    def validate(self, data):
        """
        Checks the time field if it's in past.

        Checks whether any of phone_number or email is provided or not.

        Checks whether the phone_number is in correct format or not.
        """
        phone_number = data.get('phone_number')
        email = data.get('email')
        date = data.get('date')
        time = data.get('time')
            
        _datetime = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M")
        if _datetime < datetime.now():
            raise serializers.ValidationError(
                {"time": "Can't place reminder in the past"})
            
        if phone_number is not None and phone_number != '':
            # Regular expression for checking ITU standards for phone number
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
            # `completed` field will not be available for editting
            "completed": {"read_only": True}
        }
