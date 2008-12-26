from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required

from apps.bookshelf import models as bookshelf_models
from apps.notebook import models as notebook_models

@login_required
def notebook(request, nbid=None, template_name='notebook/notebook.html'):
    """Render the Notebook interface.
    """
    nb = notebook_models.Notebook.objects.get(owner=request.user, guid=nbid)
    lastmod = nb.created_time #XXX
    return render_to_response(template_name, {'lastmod':lastmod, 'user':request.user})


