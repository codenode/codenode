import os
from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'homepage.html'}),
    (r'^bookshelf/', include('apps.bookshelf.urls')),
    (r'^notebook/', include('apps.notebook.urls')),
    (r'^accounts/', include('apps.registration.urls')),
    (r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
    print os.path.join(settings.PROJECT_PATH, 'static')
    urlpatterns += patterns('',
        (r'^static/(.*)', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'static')}),
)
