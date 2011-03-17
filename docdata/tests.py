"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from docdata.models import PaymentCluster

class PaymentTest(TestCase):
    def test_init(self):
        pc = PaymentCluster()
        pc.save()
        