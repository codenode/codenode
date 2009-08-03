import os
from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    (r'^$', 'django.views.generic.simple.redirect_to', {'url':'bookshelf'}), #uses template/homepage.html 
    (r'^bookshelf/', include('codenode.frontend.bookshelf.urls')),
    (r'^notebook/', include('codenode.frontend.notebook.urls')),
    (r'^backend/', include('codenode.frontend.backend.urls')),
    (r'^accounts/', include('codenode.frontend.registration.urls')),
    (r'^settings/', include('codenode.frontend.usersettings.urls')),
    (r'^util/', include('codenode.frontend.util.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(.*)', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'static')}),
)
