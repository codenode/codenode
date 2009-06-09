from django.conf.urls.defaults import *

from codenode.frontend.util.views import newadmin

urlpatterns = patterns('',
    url(r'^newadmin$', newadmin, name='newadmin'),
)
