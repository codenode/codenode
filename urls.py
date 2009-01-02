import os
from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url':'/accounts/login/'}), #uses template/homepage.html 
    (r'^bookshelf/', include('apps.bookshelf.urls')),
    (r'^notebook/', include('apps.notebook.urls')),
    (r'^accounts/', include('apps.registration.urls')),
    (r'^settings/', include('apps.usersettings.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(.*)', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'static')}),
)
