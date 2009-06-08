from django.conf.urls.defaults import *

from codenode.frontend.usersettings.views import usersettings

urlpatterns = patterns('',
    url(r'^$', usersettings, name='usersettings'),
)
