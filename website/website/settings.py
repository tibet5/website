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
SECRET_KEY = '823_^#-f(2u@za-3%f0j5!-jy=e4i0yjt_&2v*&o80j0d^17en'

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
    'django_extensions',
    'bootstrap4',
    'django_filters',
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
            ],
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'

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

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Authentication
# https://docs.djangoproject.com/en/3.1/topics/auth/default/

LOGOUT_REDIRECT_URL = '/'

# django-tables2
# https://django-tables2.readthedocs.io/en/latest/index.html

DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"

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

# Maps API keys
MAPQUEST_API_KEY = "xvB2VYxUF6mByw32kqOszrCXfgC7CuUa"  # Eric's dev account - 15k requests/month
GOOGLE_MAPS_API_KEY = "AIzaSyCO1r4-P2e5ASqVp1Wgw6jAnFBaOEyGo-s"  # Eric's dev account - hard limit at free tier
GOOGLE_MAPS_EMBED_KEY = "AIzaSyB8X4idnj8vEMpU_H0jF53SGr8pRnT2jaQ"


# Textline API
# https://textline.docs.apiary.io/
TEXTLINE_API_KEY = getenv("TEXTLINE_API_KEY")


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
        'add_delivery',
        'change_delivery',
        'delete_delivery',
        'view_delivery',
        'add_mealrequest',
        'change_mealrequest',
        'delete_mealrequest',
        'view_mealrequest',
        'add_updatenote',
        'change_updatenote',
        'delete_updatenote',
        'view_updatenote',
    ]
}
