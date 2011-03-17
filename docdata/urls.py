from djagno.conf.urls.defaults import *


urlpatterns = patterns('docdata.views',
    # Status change notifications
    url(r'^status_change/$', 'status_change', name='status_change'),

    # User status feedback
    url(r'^success/$', 'user_feedback', {'status': 'success'}, name='success'),
    url(r'^failure/$', 'user_feedback', {'status': 'failure'}, name='failure'),
    url(r'^canceled/$', 'user_feedback', {'status': 'canceled'}, name='canceled'),
    url(r'^pending/$', 'user_feedback', {'status': 'pending'}, name='pending'),
    url(r'^error/$', 'user_feedback', {'status': 'error'}, name='error')
)