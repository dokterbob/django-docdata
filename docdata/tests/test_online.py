from urllib import urlencode

from unittest import skipUnless
from django.conf import settings

from docdata.models import PaymentCluster
from docdata.exceptions import PaymentException

from .base import PaymentTestBase


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
