import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

from urllib2 import urlopen
from urllib import urlencode

from xml.dom import minidom


class PaymentException(Exception):
    def __init__(self, message, error_list):
        self.message = message
        self.error_list = error_list

    def __unicode__(self):
        return '%s, messages: %s' % (self.message, ' '.join(self.error_list))


class PaymentCluster(object):
    TEST_URL = 'https://test.tripledeal.com/ps/com.tripledeal.paymentservice.servlets.PaymentService'
    PROD_URL = ''

    def __init__(self, test=False):
        if test:
            self.url = self.TEST_URL
        else:
            self.url = self.PROD_URL

    def new_payment_cluster(self, **kwargs):
        """
        Wrapper around the new_payment_cluster command.

        Returns:
            Dictionary with `payment_cluster_id` and `payment_cluster_key`.
        """

        # Set the command
        kwargs['command'] = 'new_payment_cluster'

        # Make sure required arguments are available
        assert 'merchant_name' in kwargs
        assert 'merchant_password' in kwargs
        assert 'merchant_transaction_id' in kwargs
        assert 'profile' in kwargs
        assert 'client_id' in kwargs
        assert 'price' in kwargs
        assert 'cur_price' in kwargs
        assert 'client_email' in kwargs
        assert 'client_firstname' in kwargs
        assert 'client_lastname' in kwargs
        assert 'client_address' in kwargs
        assert 'client_zip' in kwargs
        assert 'client_city' in kwargs
        assert 'client_country' in kwargs
        assert 'client_language' in kwargs
        assert 'days_pay_period' in kwargs

        # Raises URLError on errors.
        result = urlopen(self.url, urlencode(kwargs))

        # Parse the result XML
        resultdom = minidom.parse(result)

        errors = resultdom.getElementsByTagName('errorlist').item(0)
        if errors:
            error_list = []
            for error in errors.getElementsByTagName('error'):
                error_list.append(error.getAttribute('msg'))

            raise PaymentException('Something went wrong!', error_list)

        # Get cluster key and id
        id = resultdom.getElementsByTagName('id')[0].getAttribute('value')
        key = resultdom.getElementsByTagName('key')[0].getAttribute('value')

        return {'payment_cluster_id': id, 'payment_cluster_key': key}

    def show_payment_cluster_url(self, **kwargs):
        """ Return the URL for show_payment_cluster. """

        # Set the command
        kwargs['command'] = 'show_payment_cluster'

        # Make sure required arguments are there
        assert 'merchant_name' in kwargs
        assert 'payment_cluster_key' in kwargs

        return self.url+'?'+urlencode(kwargs)
