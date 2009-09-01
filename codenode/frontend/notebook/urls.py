######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

from django.conf.urls.defaults import *

from codenode.frontend.notebook.views import notebook, share, revisions, revert

urlpatterns = patterns('',
    url(r'^(?P<nbid>\w{32})/$', notebook, name='notebook'),
    url(r'^(?P<owner>\w+)/(?P<title>.+)/$', notebook, name='notebook-by-title'),
    url(r'^share/(?P<nbid>\w{32})$', share, name='share'),
    url(r'^revisions/(?P<nbid>\w{32})$', revisions, name='revisions'),
    url(r'^revert/(?P<id>\d+)$', revert, name='revert'),
)
