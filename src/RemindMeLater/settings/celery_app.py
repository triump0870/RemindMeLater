from __future__ import absolute_import
import os
from django.conf import settings
# from kombu import serialization
import celery
import raven
from raven.contrib.celery import register_signal, register_logger_signal
import environ
env = environ.Env()

RAVEN_CLIENT_SECRET=env(RAVEN_CLIENT_SECRET)
RAVEN_CLIENT_ID=env(RAVEN_CLIENT_SECRET)
SENTRY_LINK = "https://"+RAVEN_CLIENT_ID+":"+RAVEN_CLIENT_SECRET+"@app.getsentry.com/89988"
class Celery(celery.Celery):

    def on_configure(self):
        client = raven.Client(SENTRY_LINK)

        # register a custom filter to filter out duplicate logs
        register_logger_signal(client)

        # hook into the Celery error handler
        register_signal(client)

# set the default Django settings module for the 'celery' program.
# serialization.registry._decoders.pop("application/x-python-serialize")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RemindMeLater.settings.production')
app = Celery('project')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if __name__ == '__main__':
	app.start()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))