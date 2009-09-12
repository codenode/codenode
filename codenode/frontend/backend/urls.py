
from django.conf.urls.defaults import *

from codenode.frontend.backend import views 

urlpatterns = patterns('',
        url(r'^connect/(?P<backend_name>\w{1,100})/$', views.connect_to_backend),
        url(r'^(?P<backend_name>\w{1,100})/update_engine_types$', views.update_engine_types),
        )
