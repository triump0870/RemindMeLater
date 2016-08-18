from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics
from rest_framework.permissions import AllowAny

from reminders.models import Reminder
from .serializers import ReminderSerializer

# Create your views here.


class ReminderList(generics.ListCreateAPIView):
    """
    The API endpoint /apis/reminder has GET and POST access.
    """
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = (AllowAny,)


class ReminderDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    The API endpoint /apis/reminders/id has GET, PUT, PATCH 
    and DELETE access. 
    """
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = (AllowAny,)
