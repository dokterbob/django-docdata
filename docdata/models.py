import logging
logger = logging.getLogger(__name__)

from django.db import models

from docdata.signals import payment_status_changed
from docdata.interface import PaymentInterface
from docdata.settings import (
    MERCHANT_NAME, MERCHANT_PASSWORD, DEBUG, PROFILE
)

# Connect listener to signal
from listeners import payment_update_logger
payment_status_changed.connect(payment_update_logger)


class PaymentCluster(models.Model):
    """ Payment cluster model. """

    @classmethod
    def get_by_transaction_id(cls, transaction_id):
        """
        Get the payment cluster belonging to a specific transaction_id.
        """
        assert transaction_id

        logger.debug('Looking up transaction with transaction id %s',
                     transaction_id)
        return cls.objects.get(pk=transaction_id)

    def __init__(self, *args, **kwargs):
        """ Make sure we have an interface available. """
        super(PaymentCluster, self).__init__(*args, **kwargs)

        self.interface = PaymentInterface(debug=DEBUG)

    def __unicode__(self):
        """ Our natural representation is the transaction id. """
        return self.transaction_id

    def create_cluster(self, **kwargs):
        """
        Create a new payment cluster over at Docdata and save key and id.
        """

        data = {
            'merchant_name': MERCHANT_NAME,
            'merchant_password': MERCHANT_PASSWORD,
            'merchant_transaction_id': self.transaction_id,
            'profile': PROFILE,
        }

        data.update(kwargs)

        result = self.interface.new_payment_cluster(**data)

        self.transaction_id = data['merchant_transaction_id']
        self.cluster_key = result['payment_cluster_key']
        self.cluster_id = result['payment_cluster_id']

        self.save()

    def update_status(self):
        """ Go out and update the payment status, and save to database. """

        assert self.cluster_key
        data = {
            'merchant_name': MERCHANT_NAME,
            'merchant_password': MERCHANT_PASSWORD,
            'payment_cluster_key': self.cluster_key,
            'report_type': 'txt_simple2'
        }

        result = self.interface.status_payment_cluster(**data)

        old_paid = self.paid
        old_closed = self.closed

        self.paid = result['paid']
        self.closed = result['closed']

        self.save()

        # Status changed? Send signal!
        if old_paid != self.paid or old_closed != self.closed:
            results = payment_status_changed.send_robust(
                sender=self, old_paid=old_paid, old_cloder=old_closed
            )

            # Re-raise exceptions in listeners
            for (receiver, response) in results:
                if isinstance(response, Exception):
                    raise response
        else:
            # Status update request without change? Weird! Log!
            logger.warning(
                'Status update requested but no change detected '
                'for transaction_id \'%s\'', self.transaction_id
            )

    def payment_url(self, **kwargs):
        """ Return the URL to redirect to for actual payment. """

        assert self.cluster_key

        data = {
            'merchant_name': MERCHANT_NAME,
            'payment_cluster_key': self.cluster_key
        }

        data.update(**kwargs)

        return self.interface.show_payment_cluster_url(**data)

    @classmethod
    def clear(self, days=1):
        """ Remove closed payment clusters modified at least `days` ago. """
        from datetime import datetime, timedelta

        # Too bad these little statistics *might* hurt performance
        old_count = self.objects.all().count()

        oldest = datetime.now() - timedelta(days=days)
        self.objects.filter(closed=True, modified__lt=oldest).delete()

        logging.info(
            'Deleted %d old PaymentClusters',
            old_count - self.objects.all().count()
        )

    transaction_id = models.CharField(max_length=35, primary_key=True)

    cluster_key = models.CharField(max_length=255)
    cluster_id = models.CharField(max_length=255)

    paid = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
