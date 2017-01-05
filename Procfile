release: python src/manage.py migrate
web: gunicorn --chdir src/ RemindMeLater.wsgi --preload
worker: celery --workdir=src -A RemindMeLater worker --app=RemindMeLater.settings.celery_app:app --loglevel=info --pool=solo
