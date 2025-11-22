"""
Base settings for Assignment_Project_Om_opate22 project.
These are settings shared across all environments.
"""

from pathlib import Path
import os

# --- BASE DIR ---
# IMPORTANT: Since settings moved one level deeper, we need an extra .parent
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# This makes BASE_DIR point to where manage.py lives


# --- SECURITY ---
# SECRET_KEY will be defined in dev/prod settings
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-!fw%$(xv6=#(!j6prmygw_a+9uuh=n8gnk77b8hotyjdh@xik$'
)

# DEBUG will be set per environment
DEBUG = False  # Default to False for safety

# ALLOWED_HOSTS will be set per environment
ALLOWED_HOSTS = []


# --- INSTALLED APPS ---
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your custom apps
    'accounts',
    'colleges',
    'careers',
    'catalog',
    'recommender',
    'rest_framework',
]


# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# --- URL CONFIG ---
ROOT_URLCONF = 'Assignment_Project_Om_opate22.urls'


# --- TEMPLATES ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Global template directory
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


# --- WSGI / ASGI ---
WSGI_APPLICATION = 'Assignment_Project_Om_opate22.wsgi.application'


# --- DATABASE ---
# Move database to data/ folder for better organization
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'data' / 'db.sqlite3',
    }
}


# --- PASSWORD VALIDATION ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_TZ = True


# --- STATIC FILES ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'


# --- MEDIA FILES ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# --- DEFAULT PRIMARY KEY ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- AUTHENTICATION ---
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:dashboard'
LOGOUT_REDIRECT_URL = 'accounts:login'


# --- APPLICATION SETTINGS ---
ITEMS_PER_PAGE = 20
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'