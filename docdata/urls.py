from django.conf.urls.defaults import *


urlpatterns = patterns('docdata.views',
    # Status change notifications
    url(r'^status_change/$', 'status_change', name='status_change'),
)