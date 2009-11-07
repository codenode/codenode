######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required

from codenode.frontend.bookshelf import models as bookshelf_models
from codenode.frontend.notebook import models as notebook_models
from codenode.frontend.backend import models as backend_models
from codenode.frontend.backend import rpc

@login_required
def bookshelf(request, template_name='bookshelf/bookshelf.html'):
    """Render the Bookshelf interface.
    """
    #engine_types = backend_models.EngineType.objects.values_list("name", flat=True)
    engine_types = backend_models.EngineType.objects.all()
    return render_to_response(template_name, 
        {'engine_types':engine_types, 'path':request.path}, context_instance=RequestContext(request))

@login_required
def load_bookshelf_data(request):
    """Retrieve a user's Notebooks for the Bookshelf.

    Handles the current location (all, trash, archive, folder id) as well
    and the order (asc or desc) and field that it is to be sorted on.
    """ 
    location, order, sort = [request.GET.get(v, '') for v in ['location', 'order', 'sort']]
    if order == "lastmodified":
        order = "created_time" #XXX
    if sort == "desc":
        order = "-"+order
    q = notebook_models.Notebook.objects.filter(owner=request.user, location=location).order_by(order)
    data = [[e.guid, 
            e.title, 
            e.backend.all()[0].engine_type.name, 
            e.last_modified_time().strftime("%Y-%m-%d %H:%M:%S"), 
            e.location] for e in q]
    jsobj = json.dumps(data)
    return HttpResponse(jsobj, mimetype='application/json')


@login_required
def folders(request):
    """Handle creating, retrieving, updating, deleting of folders.
    """
    if request.method == "GET":
        q = bookshelf_models.Folder.objects.filter(owner=request.user)
        data = [[e.guid, e.title] for e in q]
    if request.method == "POST":
        if "create" in request.POST:
            newfolder = bookshelf_models.Folder(owner=request.user, title="New Folder")
            newfolder.save()
            data = [[newfolder.guid, "New Folder"]]
        if "update" in request.POST:
            guid = request.POST.get("id", "")
            folder = bookshelf_models.Folder.objects.get(guid=guid)
            folder.title = request.POST.get("newname", "")
            folder.save()
            data = [[folder.guid, folder.title]]
        if "delete" in request.POST:
            folderid = request.POST.get("folderid", "")
            nbids =  request.POST.getlist("nbids")
            folder = bookshelf_models.Folder.objects.get(owner=request.user, guid=folderid)
            folder.delete()
            for nbid in nbids:
                nb = notebook_models.Notebook.objects.get(owner=request.user, guid=nbid)
                nb.delete()
            data = {"response":"ok"}
    jsobj = json.dumps(data)
    return HttpResponse(jsobj, mimetype='application/json')


@login_required
def change_notebook_location(request):
    """Move one or more notebooks to a different location in the Bookshelf.
    """
    dest = request.POST.get("dest" '')
    ids = request.POST.getlist("nbid")
    for nbid in ids:
        nb = notebook_models.Notebook.objects.get(owner=request.user, guid=nbid)
        nb.location = dest
        nb.save()
    jsobj = json.dumps({"response":"ok"})
    return HttpResponse(jsobj, mimetype='application/json')


@login_required
def new_notebook(request):
    """Create a new Notebook.
    Set notebook default type, and start instance.
    """
    engine_type_id = request.GET.get("engine_type", "")
    nb = notebook_models.Notebook(owner=request.user)
    nb.save()
    engine_type = backend_models.EngineType.objects.get(id=engine_type_id)
    access_id = rpc.allocateEngine(engine_type.backend.address, engine_type.name)
    default_engine = backend_models.NotebookBackendRecord(notebook=nb,
                                                engine_type=engine_type, 
                                                access_id=access_id)
    default_engine.save()
    redirect = "/notebook/%s" % nb.guid
    return HttpResponseRedirect(redirect)


@login_required
def empty_trash(request):
    """Permanently delete all Notebooks in the Trash section of the Bookshelf.
    """ 
    nbids = request.POST.getlist("nbids")
    for nbid in nbids:
        nb = notebook_models.Notebook.objects.get(owner=request.user, guid=nbid)
        nb.delete()
    jsobj = json.dumps({"response":"ok"})
    return HttpResponse(jsobj, mimetype='application/json')

