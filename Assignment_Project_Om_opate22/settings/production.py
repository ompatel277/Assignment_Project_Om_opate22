from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'opate22.pythonanywhere.com'
]

CSRF_TRUSTED_ORIGINS = [
    'https://opate22.pythonanywhere.com'
]

# -------------------
# DATABASE (SQLite)
# -------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'data' / 'db.sqlite3',
    }
}

# -------------------
# STATIC FILES
# -------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# -------------------
# MEDIA FILES
# -------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
