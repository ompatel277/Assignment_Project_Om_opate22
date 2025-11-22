"""
Development settings - used when running locally on your laptop.
Uses DEBUG=True and loose security for easier development.
"""

from .base import *

# Override settings for development
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']

# Development-specific settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# You can add development-specific apps here if needed
# INSTALLED_APPS += ['debug_toolbar']