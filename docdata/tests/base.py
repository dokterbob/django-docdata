from django.test import TestCase
from django.core.urlresolvers import reverse

from docdata.interface import PaymentInterface


class PaymentTestBase(TestCase):
    """ Base class for payment tests. """

    def setUp(self):
        """ Common setup. """

        # Setup a payment interface
        self.interface = PaymentInterface()

        # Status change URL
        self.status_change_url = reverse('status_change')

    def _get_unique_id(self):
        """ Create a random id. """

        import random
        # (max value for 2 byte unsigned integer)
        return random.randint(1, 65535)

    def get_transaction_id(self):
        unique_id = self._get_unique_id()
        return 'docdata-test-%d' % unique_id

    default_data = {
        'client_id': '001',
        'price': '10.00',
        'cur_price': 'eur',
        'client_email': 'user@domein.nl',
        'client_firstname': 'Triple',
        'client_lastname': 'Deal',
        'client_address': 'Euclideslaan 2',
        'client_zip': '3584 BN',
        'client_city': 'Utrecht',
        'client_country': 'nl',
        'client_language': 'nl',
        'description': 'test transaction',
        'days_pay_period': '14',
    }

    default_payment_cluster_key = (
        '90B1B94C4DAE9C207E67C48432DC3004126A7F53A0E7F58AF227D27499'
    )
