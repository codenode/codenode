import os
from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

#urlpatterns = patterns('django.views.generic.simple',
urlpatterns = patterns("",
    (r'^$', 'django.views.generic.simple.redirect_to', {'url':'bookshelf'}), #uses template/homepage.html 
    (r'^bookshelf/', include('knoboo.frontend.bookshelf.urls')),
    (r'^notebook/', include('knoboo.frontend.notebook.urls')),
    (r'^accounts/', include('knoboo.frontend.registration.urls')),
    (r'^settings/', include('knoboo.frontend.usersettings.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(.*)', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'static')}),
)
