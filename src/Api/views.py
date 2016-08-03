from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions

from Reminder.models import Reminder
from .serializer import ReminderSerializer
# Create your views here.

@api_view(['GET','POST'])
@permission_classes((permissions.AllowAny,))
def reminder_list(request, format=None):
	"""
	List all reminder or create new reminder.
	"""
	if request.method == 'GET':
		reminders = Reminder.objects.all()
		serializer = ReminderSerializer(reminders, many=True)

		return Response(serializer.data)

	if request.method == 'POST':
		serializer = ReminderSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
@permission_classes((permissions.AllowAny,))
def reminder_detail(request, pk, format=None):
	"""
	Get, update or delete the reminder.
	"""
	try:
		reminder = Reminder.objects.get(pk=pk)
	except Reminder.DoesNotExist:
		Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = ReminderSerializer(reminder)
		return Response(serializer.data)

	elif request.method == 'PUT':
		serializer = ReminderSerializer(reminder, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		reminder.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)



