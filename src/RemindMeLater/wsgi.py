"""
WSGI config for RemindMeLater project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""
import os

from django.conf import settings

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "RemindMeLater.settings.production")
# Wrap werkzeug debugger if DEBUG is on

if settings.DEBUG:
    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()

    try:
        import django.views.debug
        import six
        from werkzeug.debug import DebuggedApplication

        def null_technical_500_response(request, exc_type, exc_value, tb):
            six.reraise(exc_type, exc_value, tb)

        django.views.debug.technical_500_response = null_technical_500_response
        application = DebuggedApplication(application, evalex=True)

    except ImportError:
        pass

else:
    from django.core.wsgi import get_wsgi_application
    from dj_static import Cling

    application = Cling(get_wsgi_application())
