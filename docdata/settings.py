from django.conf import settings

APP_PREFIX = 'DOCDATA'
def get_setting(name, default):
    """ Get a Django setting of the form <APP_PREFIX>_<SETTING>. """
    setting_name = '%s_%s' % (APP_PREFIX, name)
    return getattr(settings, setting_name)

MERCHANT_NAME = get_setting('MERCHANT_NAME')
MERCHANT_PASSWORD = get_setting('MERCHANT_PASSWORD')
