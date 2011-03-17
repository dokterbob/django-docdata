from django.db import models

from docdata.interface import PaymentInterface
from docdata.settings import MERCHANT_NAME, MERCHANT_PASSWORD, DEBUG, \
                             PROFILE, TRANSACTION_ID_PREFIX


class PaymentCluster(models.Model):
    """ Payment cluster model. """

    def _get_transaction_id(self):
        """ Generate a transaction id from this cluster's public key. """

        assert self.pk, 'No public key available for unique reference'

        return '%s-%d' % (TRANSACTION_ID_PREFIX, self.pk)

    @classmethod
    def get_by_transaction_id(cls, transaction_id):
        """ Get the payment cluster belonging to a specific transaction_id. """
        assert transaction_id

        pk = transaction_id[len(TRANSACTION_ID_PREFIX)+1:]
        return cls.objects.get(pk=pk)

    def __init__(self, *args, **kwargs):
        """ Make sure we have an interface available. """
        super(PaymentCluster, self).__init__(*args, **kwargs)

        self.interface = PaymentInterface(debug=DEBUG)


    def create_cluster(self, **kwargs):
        """ Create a new payment cluster over at Docdata and save key and id. """

        data = {'merchant_name': MERCHANT_NAME,
                'merchant_password': MERCHANT_PASSWORD,
                'merchant_transaction_id': self._get_transaction_id(),
                'profile': PROFILE,}

        data.update(kwargs)

        result = self.interface.new_payment_cluster(**data)

        self.cluster_key = result['payment_cluster_key']
        self.cluster_id = result['payment_cluster_id']

    def update_status(self):
        """ Go out and update the payment status, and save to database. """

        assert self.cluster_key
        data = {'merchant_name': MERCHANT_NAME,
                'merchant_password': MERCHANT_PASSWORD,
                'payment_cluster_key': self.cluster_key,
                'report_type': 'txt_simple2'}

        result = self.interface.status_payment_cluster(**data)

        self.paid = result['paid']
        self.closed = result['closed']

        self.save()

    def payment_url(self):
        """ Return the URL to redirect to for actual payment. """

        assert self.cluster_key

        data = {'merchant_name': MERCHANT_NAME,
                'payment_cluster_key': self.cluster_key
        }

        return self.interface.show_payment_cluster_url(**data)

    cluster_key = models.CharField(max_length=255)
    cluster_id = models.CharField(max_length=255)

    paid = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)