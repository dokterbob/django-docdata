import logging
logger = logging.getLogger(__name__)

from urllib2 import urlopen
from urllib import urlencode

from xml.dom import minidom

from docdata.exceptions import PaymentException, PaymentStatusException


def yntobool(char):
    """ Interpret a char as Boolean. """

    if char == 'Y':
        return True
    elif char == 'N':
        return False
    else:
        raise Exception('Cannot interpret %s as boolean' % char)


class PaymentInterface(object):
    """
    Wrapper around Docdata API calls.

    This object is stateless and does not use any settings, hence it can be
    used easily in non-Django applications.
    """

    TEST_URL = 'https://test.tripledeal.com/ps/com.tripledeal.paymentservice.servlets.PaymentService'
    PROD_URL = ''

    def _check_errors(resultdom):
        """ Check for errors in the DOM, raise PaymentException if found. """

        errors = resultdom.getElementsByTagName('errorlist').item(0)
        if errors:
            error_list = []
            for error in errors.getElementsByTagName('error'):
                error_list.append(error.getAttribute('msg'))

            raise PaymentException('Something went wrong!', error_list)

    def __init__(self, debug=False):
        """
        Initialize the interface. If `test` is `True`, the test URL is used.
        """
        if debug:
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

        # Check for errors
        self._check_errors(resultdom)

        # Get cluster key and id
        id = resultdom.getElementsByTagName('id')[0].getAttribute('value')
        key = resultdom.getElementsByTagName('key')[0].getAttribute('value')

        return {'payment_cluster_id': id, 'payment_cluster_key': key}

    def status_payment_cluster(self, **kwargs):
        """ Get the status for a payment cluster. """

        # Set the command
        kwargs['command'] = 'status_payment_cluster'

        # Make sure required arguments are there
        assert 'merchant_name' in kwargs
        assert 'merchand_password' in kwargs
        assert 'payment_cluster_key' in kwargs
        assert 'report_type' in kwargs

        # Save some typing
        report_type = kwargs['report_type']
        assert report_type in ('txt_simple',
                               'txt_simple2',
                               'xml_std',
                               'xml_ext',
                               'xml_all')

        result = urlopen(self.url, urlencode(kwargs))

        if report_type == 'txt_simple':
            # Interpret the result as a boolean
            data = result.read()

            try:
                return yntobool(data)
            except:
                raise PaymentStatusException('Unknown status received',
                                             report_type=report_type,
                                             data=data)
        elif report_type == 'txt_simple2':
            # Interpret the result as a tuple of booleans
            data = result.read()

            try:
                return (yntobool(data[0]), yntobool(data[1]))
            except:
                raise PaymentStatusException('Unknown status received',
                                             report_type=report_type,
                                             data=data)
        else:
            # We're dealing with XML, interpret as a dictionary

            # Parse the result XML
            resultdom = minidom.parse(result)

            # Check for errors
            self._check_errors(resultdom)

            data = {}
            for e in resultdom.getElementsByTagName('status')[0].childNodes:
                # Make sure we've got only one child
                assert len(e.childNodes) == 1

                value = e.firstChild

                # Make sure it's text
                assert value.nodeType == value.TEXT_NODE

                data[e.tagName] = value.wholeText

            # Make sure we're actually returning something
            assert data

            return data



    def show_payment_cluster_url(self, **kwargs):
        """ Return the URL for show_payment_cluster. """

        # Set the command
        kwargs['command'] = 'show_payment_cluster'

        # Make sure required arguments are there
        assert 'merchant_name' in kwargs
        assert 'payment_cluster_key' in kwargs

        return self.url+'?'+urlencode(kwargs)
