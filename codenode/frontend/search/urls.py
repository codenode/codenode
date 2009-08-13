from django.conf.urls.defaults import *

from codenode.frontend.search.views import search_view

urlpatterns = patterns('',
    url(r'', search_view, name='search'),
)
