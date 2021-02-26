"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from os import getenv
from pathlib import Path

import django_heroku
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


def getenv_bool(key, default=False):
    """Retrieve an environment variable with a value like "1" or "0" and cast to boolean."""
    val = getenv(key)
    if val is None:
        return default
    return bool(int(val))


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('SECRET_KEY', '823_^#-f(2u@za-3%f0j5!-jy=e4i0yjt_&2v*&o80j0d^17en')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv_bool("DEBUG", False)

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'bootstrap4',
    'django_filters',
    'explorer',
    'core',
    'public',
    'volunteers',
    'recipients',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'

SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

# Email
# https://docs.djangoproject.com/en/3.1/topics/email/

DEFAULT_FROM_EMAIL = "The People's Pantry Toronto <noreply@thepeoplespantryto.com>"
EMAIL_HOST = getenv('MAILGUN_SMTP_SERVER')
EMAIL_PORT = getenv('MAILGUN_SMTP_PORT')
EMAIL_HOST_USER = getenv('MAILGUN_SMTP_LOGIN')
EMAIL_HOST_PASSWORD = getenv('MAILGUN_SMTP_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = 30
if EMAIL_HOST:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

PUBLIC_RELATIONS_EMAIL = 'thepeoplespantrytoronto@gmail.com'
REQUEST_COORDINATORS_EMAIL = 'thepeoplespantryrequests@gmail.com'
DELIVERY_COORDINATORS_EMAIL = 'thepeoplespantrydeliveries@gmail.com'
VOLUNTEER_COORDINATORS_EMAIL = 'thepeoplespantrytovolunteers@gmail.com'

# Authentication
# https://docs.djangoproject.com/en/3.1/topics/auth/default/

LOGOUT_REDIRECT_URL = '/'


# sentry-sdk
# https://docs.sentry.io/platforms/python/guides/django/

SENTRY_DSN = getenv("SENTRY_DSN", None)
if SENTRY_DSN:
    sentry_sdk.init(
        # This key is safe to store in version control
        # Learn more here: https://docs.sentry.io/product/sentry-basics/dsn-explainer/
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )


# django-sql-explorer
# https://django-sql-explorer.readthedocs.io/en/latest/install.html
EXPLORER_CONNECTIONS = {'Default': 'default'}
EXPLORER_DEFAULT_CONNECTION = 'default'
EXPLORER_PERMISSION_VIEW = lambda request: request.user.is_staff
EXPLORER_PERMISSION_CHANGE = lambda request: request.user.is_superuser


# Configure hosted settings automatically using django_heroku
django_heroku.settings(locals())

# Model constants
DEFAULT_LENGTH = 256
NAME_LENGTH = DEFAULT_LENGTH
PHONE_NUMBER_LENGTH = 20
ADDRESS_LENGTH = DEFAULT_LENGTH
CITY_LENGTH = 50
POSTAL_CODE_LENGTH = 7  # Optional space
DAY_LENGTH = 9  # Longest is "Wednesday"
LONG_TEXT_LENGTH = 1024

# Settings for pausing requests
PAUSE_GROCERIES = 40
PAUSE_MEALS = 45

# Settings for figuring out delivery distances
MAX_CHEF_DISTANCE = 15  # Chefs can't be more than this many km away from their recipients

# Maps API keys
MAPQUEST_API_KEY = "xvB2VYxUF6mByw32kqOszrCXfgC7CuUa"  # Eric's dev account - 15k requests/month
GOOGLE_MAPS_PRODUCTION_KEY = getenv("GOOGLE_MAPS_API_KEY")  # Env var refers to PPT Developer API key

# Textline API
# https://textline.docs.apiary.io/

TEXTLINE_ACCESS_TOKEN = getenv("TEXTLINE_ACCESS_TOKEN")


# Group Permissions
# List of permissions that each group has
# Group permissions are reset to this list on every deploy

GROUP_PERMISSIONS = {
    'Chefs': [
        'add_delivery',
        'view_delivery',
        'view_mealrequest',
    ],
    'Deliverers': [
        'add_delivery',
        'view_delivery',
        'view_mealrequest',
    ],
    'Organizers': [
        'add_mealrequest',
        'change_mealrequest',
        'delete_mealrequest',
        'view_mealrequest',
        'add_mealdelivery',
        'change_mealdelivery',
        'delete_mealdelivery',
        'view_mealdelivery',
        'add_mealrequestcomment',
        'view_mealrequestcomment',
        'add_mealdeliverycomment',
        'view_mealdeliverycomment',
        'view_volunteerapplication',
        'view_volunteer',
    ]
}
