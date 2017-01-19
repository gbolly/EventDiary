from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SITE_ID = 3

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'theeventdiary',
        'USER': 'theeventdiary',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_ROOT = 'staticfiles'
