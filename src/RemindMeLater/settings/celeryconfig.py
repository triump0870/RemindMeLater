BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = 'rpc://'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['Application/json']
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_ENABLE_UTC = True