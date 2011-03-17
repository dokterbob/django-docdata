"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from docdata.models import PaymentCluster
from docdata.exceptions import PaymentException


class PaymentTest(TestCase):
    default_data = {
            "client_id" : "001",
            "price" : "10.00",
            "cur_price" : "eur",
            "client_email" : "user@domein.nl",
            "client_firstname" : "Triple",
            "client_lastname" : "Deal",
            "client_address" : "Euclideslaan 2",
            "client_zip" : "3584 BN",
            "client_city" : "Utrecht",
            "client_country" : "nl",
            "client_language" : "nl",
            "description" : "test transaction",
            "days_pay_period" : "14",
    }

    def _get_unique_id(self):
        """ Create a unique key from the POSIX timestamp. """
        import random
        # (max value for 2 byte unsigned integer)
        return random.randint(1, 65535)

    def test_createcluster(self):
        pc = PaymentCluster(pk=self._get_unique_id())

        pc.create_cluster(**self.default_data)

        pc.save()

        self.assertTrue(pc.cluster_key)
        self.assertTrue(pc.cluster_id)

    def test_clusterfail(self):
        pc = PaymentCluster(pk=self._get_unique_id())

        data = self.default_data.copy()

        del data['client_email']

        # Missing fields should be caught early
        self.assertRaises(
            AssertionError,
            pc.create_cluster,
            **data
        )

        data = self.default_data.copy()
        data['merchant_name'] = 'nobody'

        # Overriding the merchang name should yield an error
        self.assertRaises(
            PaymentException,
            pc.create_cluster,
            **data
        )

        data = self.default_data.copy()
        data['price'] = '0.00'

        # Zero amount should yield an error
        self.assertRaises(
            PaymentException,
            pc.create_cluster,
            **data
        )

    def test_report(self):
        """ Test payment cluster status reports. """

        # Create a cluster
        pc = PaymentCluster(pk=self._get_unique_id())
        pc.create_cluster(**self.default_data)

        pc.update_status()

        self.assertFalse(pc.paid)
        self.assertFalse(pc.closed)

    def test_reportfail(self):
        """ Test whether errors in report code are caught. """

        # Create a cluster
        pc = PaymentCluster(pk=self._get_unique_id())
        pc.cluster_key = 'banana'
        self.assertRaises(PaymentException, pc.update_status)

    def test_showurl(self):
        """ See whether we can generate a show url. """

        # Create a cluster
        pc = PaymentCluster(pk=self._get_unique_id())
        pc.create_cluster(**self.default_data)
        self.assertTrue(pc.payment_url())

    # def test_paysuccess(self):
    #     """ Test whether succesful payments are processed. """
    #
    #     # Create a cluster
    #     pc = PaymentCluster(pk=self._get_unique_id())
    #     pc.create_cluster(**self.default_data)
    #
    #     url = pc.show_payment_url()
    #     print 'Please go to %s and perform a successful payment. Press <ENTER> to proceed.' % url
    #
    #     raw_input()
    #
    #     pc.update_status()
    #
    #     self.assertTrue(pc.paid)
    #     self.assertTrue(pc.closed)
    #
    # def test_payfailure(self):
    #     """ Test whether succesful payments are processed. """
    #
    #     # Create a cluster
    #     pc = PaymentCluster(pk=self._get_unique_id())
    #     pc.create_cluster(**self.default_data)
    #
    #     url = pc.show_payment_url()
    #     print 'Please go to %s and cancel the payment. Press <ENTER> to proceed.' % url
    #
    #     raw_input()
    #
    #     pc.update_status()
    #
    #     self.assertFalse(pc.paid)
    #     self.assertTrue(pc.closed)
