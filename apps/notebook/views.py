from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required

from apps.bookshelf import models as bookshelf_models
from apps.notebook import models as notebook_models

@login_required
def notebook(request, template_name='notebook/notebook.html', extra_context={}, nbid=None):
    """Render the Notebook interface.
    """
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    print "nbid => ", nbid
    nb = notebook_models.Notebook.objects.get(owner=request.user, guid=nbid)
    print nb.owner
    return render_to_response(template_name, {'user':request.user}, context_instance=context)


