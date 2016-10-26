from jsignature.settings import *

import os

INSTALLED_APPS = INSTALLED_APPS + ('tests',)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'test')
DISABLE_MIGRATIONS = os.environ.get('DISABLE_MIGRATIONS', 'false').lower() == 'true'
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'test.sqlite3',
    'TEST_NAME': ':memory:' if DISABLE_MIGRATIONS else 'test.sqlite3',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': ''
}
