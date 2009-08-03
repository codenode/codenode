
from django.conf.urls.defaults import *

from codenode.frontend.backend.views import connect_to_backend
from codenode.frontend.backend.views import runInstance

urlpatterns = patterns('',
        url(r'^connect/(?P<backend_name>\w{3,7})/$', connect_to_backend),
        url(r'^run/(?P<engine_type>\w{3,7})/$', runInstance),
        )
