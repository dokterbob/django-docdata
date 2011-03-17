import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse, HttpResponseNotFound

from docdata.models import PaymentCluster


def status_change(request):
    """ Update URL should have ?merchant_transaction_id=<id> set. """
    transaction_id = request.GET.get('merchant_transaction_id')

    if not transaction_id:
        logger.warning('No transaction id in status change message')
        return HttpResponseNotFound('')

    logger.debug('Received status change message for transaction_id %s',
                 transaction_id)

    try:
        payment_cluster = \
            PaymentCluster.get_by_transaction_id(transaction_id)
    except (PaymentCluster.DoesNotExist, ValueError):
        logger.warning('Status change for payment cluster with merchant \
                        transaction_id %s not matched', transaction_id)
        return HttpResponseNotFound('')

    payment_cluster.update_status()

    logger.debug('Status for payment with transaction_id %s updated',
                 transaction_id)

    # Allways return a 200
    return HttpResponse('')
