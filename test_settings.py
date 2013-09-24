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

try:
    from test_secrets import DOCDATA_MERCHANT_NAME, DOCDATA_MERCHANT_PASSWORD
except ImportError:
    sys.exit(
        'Must define DOCDATA_MERCHANT_NAME and DOCDATA_MERCHANT_PASSWORD '
        'in test_secrets.py first!'
    )
