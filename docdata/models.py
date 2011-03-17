from django.db import models

from docdata.interface import PaymentInterface
from docdata.settings import MERCHANT_NAME, MERCHANT_PASSWORD, DEBUG, PROFILE


class PaymentCluster(models.Model):
    """ Payment cluster model. """

    def get_transaction_id(self):
        """ Generate a transaction id from this cluster's public key. """

        assert self.pk, 'No public key available for unique reference'
        return 'django_docdata-%d' % self.pk

    def __init__(self, *args, **kwargs):
        """ Make sure we have an interface available. """
        super(PaymentCluster, self).__init__(*args, **kwargs)

        self.interface = PaymentInterface(debug=DEBUG)


    def create_cluster(self, **kwargs):
        data = {'merchant_name': MERCHANT_NAME,
                'merchant_password': MERCHANT_PASSWORD,
                'merchant_transaction_id': self.get_transaction_id(),
                'profile': PROFILE,}

        data.update(kwargs)

        result = self.interface.new_payment_cluster(**data)

        self.cluster_key = result['payment_cluster_key']
        self.cluster_id = result['payment_cluster_id']

    cluster_key = models.CharField(max_length=255)
    cluster_id = models.CharField(max_length=255)