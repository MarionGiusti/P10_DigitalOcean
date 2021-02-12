from .defaults import *

DEBUG = False

ALLOWED_HOSTS = ['134.122.106.30']
SECRET_KEY = os.getenv("SECRET_KEY")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'purbeurre',
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PWD'),
        'HOST': '',
        'PORT': '5432',
    }
}
