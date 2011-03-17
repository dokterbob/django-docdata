class PaymentException(Exception):
    def __init__(self, message, error_list):
        self.message = message
        self.error_list = error_list

    def __unicode__(self):
        return '%s, messages: %s' % (self.message, ' '.join(self.error_list))
