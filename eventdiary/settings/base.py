"""
Django settings for eventdiary project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.core.exceptions import ImproperlyConfigured
import cloudinary

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/
 
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

# # SECURITY WARNING: keep the secret key used in production secret!
import envvars
envvars.load()
SECRET_KEY = envvars.get('SECRET_KEY')

ALLOWED_HOSTS = ["*"]
DEBUG_TOOLBAR_PATCH_SETTINGS = False

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allaccess',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'anymail',
    'bootstrap3',
    'cloudinary',
    'envvars',
    'fancybox',
    'multiselectfield',
    'phonenumber_field',
    'session_security',
    'smart_selects',
    'widget_tweaks',
    'web.accounts',
    'web.deals',
    'web.authentication',
    'web.centers',
    'web.merchant',
)

ROOT_URLCONF = 'eventdiary.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    'allaccess.backends.AuthorizedServiceBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
)

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

WSGI_APPLICATION = 'eventdiary.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

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

import dj_database_url

DATABASES["default"] = dj_database_url.config()

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = envvars.get('EMAIL_HOST')
EMAIL_HOST_USER = envvars.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = envvars.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 465
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = "staticfiles"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

LOGIN_REDIRECT_URL = '/center'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')

cloudinary.config(
  cloud_name = envvars.get("CLOUDINARY_NAME"),
  api_key = envvars.get("CLOUDINARY_KEY"),
  api_secret = envvars.get("CLOUDINARY_SECRET")
)

# centers listings and search:
Centers = {
    'default_search_city': 25,
    'num_page_items': 15,
    'min_orphan_items': 2,
}

