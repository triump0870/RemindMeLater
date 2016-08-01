web: python src/manage.py collectstatic --noinput
web: gunicorn --chdir src/ RemindMeLater.wsgi --preload