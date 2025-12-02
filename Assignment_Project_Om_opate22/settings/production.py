from .base import *

DEBUG = False

ALLOWED_HOSTS = ['opate22.pythonanywhere.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'opate22$info390gc-mysql-database-Traject-opate22',
        'USER': 'opate22',
        'PASSWORD': 'Crispyunicorn6248$',
        'HOST': 'opate22.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
}
