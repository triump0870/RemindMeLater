from datetime import datetime,time
from Reminder.models import Reminder
import arrow

t = time(23,35)
date = datetime.today().date()
a = Reminder.objects.create(message="ami je tomar",date=date,time=t,email="b4you0870@gmail.com",completed=False)
from Reminder.tasks import send_mail_reminder

# b = send_mail_reminder(a.id)
# print "b:",b

date_time = datetime.combine(a.date,a.time)
reminder_time = arrow.get(date_time).replace(tzinfo=a.time_zone.zone)
c = send_mail_reminder.apply_async((a.id,),eta=reminder_time, serializer='json')
print "c:",c