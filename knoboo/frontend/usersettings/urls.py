from django.conf.urls.defaults import *

from knoboo.frontend.usersettings.views import usersettings

urlpatterns = patterns('',
    url(r'^$', usersettings, name='usersettings'),
)
