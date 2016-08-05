CELERY_RESULT_BACKEND = 'amqp'
CELERY_IGNORE_RESULT = False
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_ENABLE_UTC = True
CELERY_SEND_TASK_ERROR_EMAILS = True
SERVER_EMAIL = 'rohan@rohanroy.com'
ADMINS = [
        ('Rohan', 'rohan@rohanroy.com')
]
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
DEFAULT_FROM_EMAIL = 'rohan@rohanroy.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 465
EMAIL_TIMEOUT = 10
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
