from django.db import models

from docdata.interface import PaymentInterface
from docdata.settings import MERCHANT_NAME, MERCHANT_PASSWORD, DEBUG


class PaymentCluster(models.Model):
    """ Payment cluster model. """

    # def get_merchant_transaction_id(self):
    #     """ Generate a transaction id from this cluster's public key. """
    #     
    #     return 'django_docdata-%d' % self.pk
    # 
    # def __init__(self):
    #     print 'yoepie'
    
    payment_cluster_key = models.CharField(primary_key=True, max_length=255)
    payment_cluster_id = models.CharField(max_length=255)