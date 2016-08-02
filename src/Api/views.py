from django.shortcuts import render
from rest_framework import generics
from Reminder.models import Reminder
from .serializer import ReminderSerializer, ReminderDetailSerializer

# Create your views here.

class CreateReminderView(generics.ListCreateAPIView):
	queryset = Reminder.objects.all()
	serializer_class = ReminderSerializer

class ReminderDetailView(generics.RetrieveUpdateAPIView):
	serializer_class = ReminderSerializer

	def get_queryset(self):
		return Reminder.objects.all()


