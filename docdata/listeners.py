import logging
logger = logging.getLogger(__name__)


def payment_update_logger(sender, **kwargs):
    """ Write out a log message for each update signal sent. """

    logger.debug(
        'Payment status update for transaction %s: paid=%s, closed=%s',
        sender.transaction_id, sender.paid, sender.closed
    )
