"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from docdata.models import PaymentCluster
from docdata.exceptions import PaymentException


class PaymentTest(TestCase):
    def _get_unique_id(self):
        """ Create a unique key from the POSIX timestamp. """

        import time
        return int(time.time())

    def test_createcluster(self):
        pc = PaymentCluster(pk=self._get_unique_id())

        pc.create_cluster(**{
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
        })

        pc.save()

        self.assertTrue(pc.cluster_key)
        self.assertTrue(pc.cluster_id)

    def test_clusterfail(self):
        pc = PaymentCluster(pk=self._get_unique_id())

        # Missing fields should be caught early
        self.assertRaises(
            AssertionError,
            pc.create_cluster,
            **{
                "client_id" : "001",
                "price" : "10.00",
                "cur_price" : "eur",
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
        )

        # Overriding the merchang name should yield an error
        self.assertRaises(
            PaymentException,
            pc.create_cluster,
            **{
                "merchant_name": "nobody",
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
        )

        # Zero amount should yield an error
        self.assertRaises(
            PaymentException,
            pc.create_cluster,
            **{
                "merchant_name": "nobody",
                "client_id" : "001",
                "price" : "00.00",
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
        )