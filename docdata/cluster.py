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

    def create(self, **kwargs):
        kwargs['command'] = 'new_payment_cluster'

        assert 'merchant_name' in kwargs
                 # merchant_password,
                 # merchant_transaction_id,
                 # profile='standard',
                 # client_id,
                 # price,
                 # cur_price,
                 # client_email,
                 # client_firstname,
                 # client_lastname,
                 # client_address,
                 # client_zip,
                 # client_city,
                 # client_country
                 # client_language,
                 # days_pay_period
        
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
    
    def show_url(self, **kwargs):
        kwargs['command'] = 'show_payment_cluster'
        
        assert 'merchant_name' in kwargs
        assert 'payment_cluster_key' in kwargs
        