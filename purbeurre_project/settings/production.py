from .defaults import *
import logging
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.DEBUG
)

sentry_sdk.init(
    dsn="https://fed70ebb04884fd1813c123bcc88f136@o522203.ingest.sentry.io/5633331",
    integrations=[DjangoIntegration(), sentry_logging],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'root': {
        'handlers': ['console', ],
        'level': 'INFO',
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'myprojectcustom': {
            'level': 'INFO',
            'handlers': ['console', ],
        },
        'django.request': {
            'level' : 'INFO',
            'handlers': ['console', ],
            'propagate': False
        }
     }
}
