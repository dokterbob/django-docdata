from django.http import HttpResponse


def status_change(request):
    """ Update URL should have ?merchant_transaction_id=<id> set. """
    merchant_transaction_id = request.GET.get('merchant_transaction_id')

    # Allways return a 200
    return HttpResponse('')

def user_feedback(request, status):
    raise NotImplementedError
