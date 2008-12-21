from django.conf.urls.defaults import *

from apps.notebook.views import notebook

urlpatterns = patterns('',
    url(r'(?P<nbid>\w{32})', notebook, name='notebook'),
)
