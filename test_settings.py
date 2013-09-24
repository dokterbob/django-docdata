DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

# HACK: this fixes our threaded runserver remote tests
# DATABASE_NAME='test_docdata.sqlite',
# TEST_DATABASE_NAME='test_docdata.sqlite',

INSTALLED_APPS = (
    'docdata',
)

ROOT_URLCONF = 'docdata.urls'

try:
    # If available, South is required by setuptest
    import south
    INSTALLED_APPS += ('south', )
except ImportError:
    # South not installed and hence is not required
    pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '- %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
    }
}

# Make absolutely sure we're running in debug mode
DOCDATA_DEBUG = True

try:
    from test_secrets import DOCDATA_MERCHANT_NAME, DOCDATA_MERCHANT_PASSWORD

    # Run online tests
    DOCDATA_ONLINE_TESTS = True

except ImportError, e:
    print 'Warning:', e
    print (
        'DOCDATA_MERCHANT_NAME and DOCDATA_MERCHANT_PASSWORD '
        'are not set in test_settings.py. Online tests will be skipped.'
    )

    # Do not run online tests
    DOCDATA_MERCHANT_NAME = 'bogus_merchant'
    DOCDATA_MERCHANT_PASSWORD = 'bogus_pw'
    DOCDATA_ONLINE_TESTS = False
