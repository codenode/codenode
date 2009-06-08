from django.conf.urls.defaults import *

from codenode.frontend.notebook.views import notebook, share

urlpatterns = patterns('',
    url(r'^(?P<nbid>\w{32})/$', notebook, name='notebook'),
    url(r'^share/(?P<nbid>\w{32})$', share, name='share'),
)
