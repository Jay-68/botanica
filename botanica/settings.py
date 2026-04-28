"""
Botanica Project Settings
"""
import os
from pathlib import Path
from urllib.parse import urlparse, parse_qsl

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# load environment variables from .env in local development
load_dotenv()

DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in {'1', 'true', 'yes'}

SECRET_KEY_ENV = os.getenv('DJANGO_SECRET_KEY')
if SECRET_KEY_ENV:
    SECRET_KEY = SECRET_KEY_ENV
elif DEBUG:
    SECRET_KEY = 'django-insecure-local-dev-key'
else:
    raise ImproperlyConfigured('DJANGO_SECRET_KEY environment variable is required in production.')

ALLOWED_HOSTS = [host.strip() for host in os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',') if host.strip()]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'grimoire',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'botanica.urls'

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

WSGI_APPLICATION = 'botanica.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "neondb",
        "USER": "neondb_owner",
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": "ep-snowy-silence-ab7eaame.eu-west-2.aws.neon.tech",
        "PORT": "5432",
        "OPTIONS": {"sslmode": "require"},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE="whitenoise.storage.CompressedManifestStaticFilesStorage"

DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/admin/login/'

if not DEBUG:
    CSRF_TRUSTED_ORIGINS = [‘https://web-production-6a521.up.railway.app/’]