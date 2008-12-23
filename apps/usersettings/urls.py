from django.conf.urls.defaults import *

from apps.usersettings.views import usersettings

urlpatterns = patterns('',
    url(r'^$', usersettings, name='usersettings'),
)
