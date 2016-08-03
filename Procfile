web: gunicorn --chdir src/ RemindMeLater.wsgi --preload
worker: celery --workdir=src -A RemindMeLater worker --app=RemindMeLater.settings.celery_app:app --loglevel=info 