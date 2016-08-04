CELERY_RESULT_BACKEND = 'rpc://'
BROKER_POOL_LIMIT = 3

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_ENABLE_UTC = True
CELERY_SEND_TASK_ERROR_EMAILS = True
SERVER_EMAIL = 'abc@example.com'
ADMINS = [
        ('abc', 'abc@example.com')
]
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
DEFAULT_FROM_EMAIL = 'abc@example.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 465
EMAIL_TIMEOUT = 10
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_HOST_USER = 'abcjdjdlasskjjdklsaj'
EMAIL_HOST_PASSWORD = 'djkashdklahsjdhasljkdhjksahdjkashdjakhdak'