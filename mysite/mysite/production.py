from settings import *

DEBUG = False

ALLOWED_HOSTS = ['gaoyumedia.net', 'www.gaoyumedia.net']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'production.sqlite3'),
    }
}