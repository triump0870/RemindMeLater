# In production set the environment variable like this:
#    DJANGO_SETTINGS_MODULE=RemindMeLater.settings.production
from .base import *             # NOQA
import logging.config
import dj_database_url

# Sentry/ Raven settings
import raven

# For security and performance reasons, DEBUG is turned off
DEBUG = False
TEMPLATE_DEBUG = DEBUG
BROKER_URL = "amqp://bdbwbjza:yYpzWPRU7azVAXCsH6PVwkxmxeFWfCzz@reindeer.rmq.cloudamqp.com/bdbwbjza"
# Must mention ALLOWED_HOSTS in production!
ALLOWED_HOSTS = ["*"]

# Cache the templates in memory for speed-up
loaders = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]   

TEMPLATES[0]['OPTIONS'].update({"loaders": loaders})
TEMPLATES[0].update({"APP_DIRS": False})

# Define STATIC_ROOT for the collectstatic command
STATIC_ROOT = join(BASE_DIR,'..','site','static')

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Log everything to the logs directory at the top
LOGFILE_ROOT = join(dirname(BASE_DIR), 'logs')

# Hereku postgres database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
    }
}


RAVEN_CONFIG = {
    'dsn': 'https://67f46cd6b820412e8f0d4d94cc832486:36fba09345934d469d45b0b298e7e87b@app.getsentry.com/89988',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
}   

# production database settings
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

MIDDLEWARE_CLASSES = (
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
) + MIDDLEWARE_CLASSES

# Reset logging
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'proj_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(LOGFILE_ROOT, 'project.log'),
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },

    'loggers': {
        'project': {
            'handlers': ['proj_log_file'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['proj_log_file','sentry'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console','sentry'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console','sentry'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console','sentry'],
            'propagate': False,
        },
        '': {
            'handlers': ['proj_log_file','console'],
            'level': 'WARNING',
            'propagate': True,
        },
    }
}
logging.config.dictConfig(LOGGING)
