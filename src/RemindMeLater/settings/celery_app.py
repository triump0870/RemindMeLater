from __future__ import absolute_import
import os
from django.conf import settings
# from kombu import serialization
import celery
import raven
from raven.contrib.celery import register_signal, register_logger_signal
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RemindMeLater.settings.production')
SENTRY_LINK = "https://"+settings.RAVEN_CLIENT_ID+":"+settings.RAVEN_CLIENT_SECRET+"@app.getsentry.com/89988"
class Celery(celery.Celery):

    def on_configure(self):
        client = raven.Client(SENTRY_LINK)

        # register a custom filter to filter out duplicate logs
        register_logger_signal(client)

        # hook into the Celery error handler
        register_signal(client)

# set the default Django settings module for the 'celery' program.
# serialization.registry._decoders.pop("application/x-python-serialize")
app = Celery('RemindMeLater')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if __name__ == '__main__':
	app.start()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))