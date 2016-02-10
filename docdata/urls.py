from django.conf.urls import url

from .views import status_change


urlpatterns = [
    # Status change notifications
    url(r'^status_change/$', status_change, name='status_change'),
]
