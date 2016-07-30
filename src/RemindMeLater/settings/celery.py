from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings


# Set the default django settings module for the 'Celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE','RemindMeLater.settings')
app = Celery('RemindMeLater')

# Using a string here means the worker will not have to
# pickle the object when using windows
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.Task(bind=True)
def debug_task(self):
	print 'Request: {0!r}'.format(self.request)

