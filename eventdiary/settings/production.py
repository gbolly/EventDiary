from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Parse database configuration from $DATABASE_URL
import dj_database_url

ALLOWED_HOSTS = ['*']

DATABASES = {'default': dj_database_url.config()}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# STATIC_ROOT = 'staticfiles'

STATIC_ROOT= os.path.join(BASE_DIR,'staticfiles')

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
