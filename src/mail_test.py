from datetime import datetime, time
from Reminder.models import Reminder
import arrow

t = time(13, 21, 05)
date = datetime.today().date()
a = Reminder.objects.create(message="Hello world",
                            date=date, time=t, phone_number="+919148912120")
# from Reminder.tasks import send_sms_reminder

# # b = send_mail_reminder(a.id)
# # print "b:",b

# date_time = datetime.combine(a.date,a.time)
# reminder_time = arrow.get(date_time).replace(tzinfo=a.time_zone.zone)
# c = send_sms_reminder.apply_async((a.id,), eta=reminder_time)
# print "c:",c
