"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from urllib import urlencode

from django.test import TestCase
from django.conf import settings
from django.utils.unittest.case import skipUnless
from django.core.urlresolvers import reverse

from docdata.models import PaymentCluster
from docdata.exceptions import PaymentException


class PaymentTestBase(TestCase):
    """ Base class for payment tests. """

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

    status_change_url = reverse('status_change')

    def _get_unique_id(self):
        """ Create a random id. """

        import random
        # (max value for 2 byte unsigned integer)
        return random.randint(1, 65535)

    def get_transaction_id(self):
        unique_id = self._get_unique_id()
        return 'docdata-test-%d' % unique_id


@skipUnless(settings.DOCDATA_ONLINE_TESTS, 'Skipping online tests.')
class OnlinePaymentTests(PaymentTestBase):
    """ Tests requiring payment credentials to be set. """

    def test_createcluster(self):
        pc = PaymentCluster(pk=self.get_transaction_id())

        pc.create_cluster(**self.default_data)

        pc.save()

        self.assertTrue(pc.cluster_key)
        self.assertTrue(pc.cluster_id)

    def test_createclusterunicode(self):
        """
        Test creating a cluster with some unicode data
        Regression test.
        """
        pc = PaymentCluster(pk=self.get_transaction_id())

        self.default_data.update({'client_firstname': u'Margr\xe8t'})

        pc.create_cluster(**self.default_data)

        pc.save()

        self.assertTrue(pc.cluster_key)
        self.assertTrue(pc.cluster_id)

    def test_clusterfail(self):
        pc = PaymentCluster(pk=self.get_transaction_id())

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
        pc = PaymentCluster(pk=self.get_transaction_id())
        pc.create_cluster(**self.default_data)

        pc.update_status()

        self.assertFalse(pc.paid)
        self.assertFalse(pc.closed)

    def test_reportfail(self):
        """ Test whether errors in report code are caught. """

        # Create a cluster
        pc = PaymentCluster(pk=self.get_transaction_id())
        pc.cluster_key = 'banana'
        self.assertRaises(PaymentException, pc.update_status)

    def test_showurl(self):
        """ See whether we can generate a show url. """

        # Create a cluster
        pc = PaymentCluster(pk=self.get_transaction_id())
        pc.create_cluster(**self.default_data)
        self.assertTrue(pc.payment_url())

    def test_status_success(self):
        # Create a cluster
        pc = PaymentCluster(pk=self.get_transaction_id())
        pc.create_cluster(**self.default_data)
        transaction_id = pc.transaction_id

        url = self.status_change_url
        url += '?' + urlencode({'merchant_transaction_id': transaction_id})

        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)


class OfflinePaymentTests(PaymentTestBase):
    """ Tests not requiring payment credentials to be set. """

    def test_status_fail(self):
        """ Test whether status_change requests are handled well."""

        url = self.status_change_url

        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 404)

        response = self.client.get(url+'?merchant_transaction_id=kaas')
        self.failUnlessEqual(response.status_code, 404)

    def test_transaction_id(self):
        """ Test transaction_id -> pk resolution. """

        pc = PaymentCluster(pk=self.get_transaction_id())
        pc.save()

        transaction_id = pc.transaction_id
        pc2 = PaymentCluster.get_by_transaction_id(transaction_id)

        self.assertEqual(pc.pk, pc2.pk)
