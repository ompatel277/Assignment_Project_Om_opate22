"""
Production settings - used on PythonAnywhere server.
Uses DEBUG=False and strict security settings.
"""

from .base import *
import os

# Override settings for production
DEBUG = False

# IMPORTANT: Add your PythonAnywhere URL here
# Replace 'yourusername' with your actual PythonAnywhere username
ALLOWED_HOSTS = [
    'yourusername.pythonanywhere.com',  # CHANGE THIS!
    '127.0.0.1',
    'localhost',
]

# Production security settings
SECURE_SSL_REDIRECT = False  # PythonAnywhere handles SSL
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Use environment variable for SECRET_KEY in production
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-!fw%$(xv6=#(!j6prmygw_a+9uuh=n8gnk77b8hotyjdh@xik$'
)

# Optional: Use PostgreSQL or MySQL on PythonAnywhere
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'yourusername$dbname',
#         'USER': 'yourusername',
#         'PASSWORD': 'yourpassword',
#         'HOST': 'yourusername.mysql.pythonanywhere-services.com',
#     }
# }