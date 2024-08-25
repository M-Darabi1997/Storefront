from .common import *
import configparser


DEBUG = True

config = configparser.ConfigParser()
config.read(Path('.env'))


DATABASES = {
    'default': {
        'ENGINE': config.get('database', 'DB_ENGINE', fallback='django.db.backends.postgresql'),
        'NAME': config.get('database', 'DB_NAME'),
        'USER': config.get('database', 'DB_USER'),
        'PASSWORD': config.get('database', 'DB_PASSWORD'),
        'HOST': config.get('database', 'DB_HOST',  
 fallback='localhost'),
        'PORT': config.get('database', 'DB_PORT', fallback='5432'),
    }
}

SECRET_KEY = config.get('general', 'SECRET_KEY')

CELERY_BROKER_URL = 'redis://redis:6379/1'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/2',
        'TIMEOUT': 10 * 60,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

EMAIL_HOST = 'smtp4dev'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}
