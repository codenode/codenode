from django.conf.urls.defaults import *

from codenode.frontend.notebook.views import notebook
from codenode.frontend.notebook.views import nbobject
from codenode.frontend.notebook.views import save
from codenode.frontend.notebook.views import delete_cell
from codenode.frontend.notebook.views import title
from codenode.frontend.notebook.views import share

urlpatterns = patterns('',
    url(r'^(?P<nbid>\w{32})/$', notebook, name='notebook'),
    url(r'^(?P<nbid>\w{32})/nbobject$', nbobject, name='nbobject'),
    url(r'^(?P<nbid>\w{32})/save$', save, name='save'),
    url(r'^(?P<nbid>\w{32})/deletecell$', delete_cell, name='delete_cell'),
    url(r'^(?P<nbid>\w{32})/title$', title, name='title'),
    url(r'^share/(?P<nbid>\w{32})$', share, name='share'),
)
