web: gunicorn --chdir src/ RemindMeLater.wsgi --preload
worker: celery -A RemindMeLater.settings worker -l info