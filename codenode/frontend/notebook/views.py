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
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from codenode.frontend.bookshelf import models as bookshelf_models
from codenode.frontend.notebook import models as notebook_models

from codenode.frontend.notebook import forms 

from codenode.frontend.notebook.revision_utils import get_nb_revisions, revert_to_revision

@login_required
def notebook(request, nbid=None, owner=None, title=None, template_name='notebook/notebook.html'):
    """Render the Notebook interface.
    """
    # if the id is supplied, we can get the notebook directly
    if nbid: 
        nb = notebook_models.Notebook.objects.get(owner=request.user, guid=nbid)
        lastmod = nb.created_time #XXX
        return render_to_response(template_name, {'title':nb.title, 'lastmod':lastmod, 'nbid':nbid, 'user':request.user})
    
    # otherwise, we need to look it up and redirect
    assert owner and title
    matching_notebooks = notebook_models.Notebook.objects.\
                                    filter(owner__username__iexact=owner).\
                                    filter(title__iexact=title)
    notebook = iter(matching_notebooks).next()
    return HttpResponseRedirect(reverse('notebook', args=[notebook.guid]))
    
@login_required
def revisions(request, nbid=None, template_name='notebook/revisions.html'):
    """Notebook revisions.
    """
    revisions = get_nb_revisions(nbid)
    return render_to_response(template_name, {'nbid':nbid, 'user':request.user, 'revisions':revisions})

@login_required
def nbobject(request, nbid):
    nb = notebook_models.Notebook.objects.get(owner=request.user, guid=nbid)

    cells = notebook_models.Cell.objects.filter(notebook=nb)

    nbdata, cellsdata = {}, {}
    for cell in cells:
        cellsdata[cell.guid] = {'content':cell.content, 'cellstyle':cell.style, 'props':cell.props}
    nbdata['cells'] = cellsdata
    nbdata['settings'] = {'cell_input_border':'None', 'cell_output_border':'None'}
    nbdata['nbid'] = nb.guid
    nbdata['orderlist'] = nb.orderlist
    nbdata['title'] = nb.title
    jsobj = json.dumps(nbdata)
    return HttpResponse(jsobj, mimetype="application/json")

@login_required
def title(request, nbid):
    if request.method == "POST":
        newtitle = request.POST.get('newtitle')
        nb = notebook_models.Notebook.objects.get(owner=request.user, guid=nbid)
        nb.title = unicode(newtitle)
        nb.save()
        data = {'response':'ok', 'title':newtitle}
        jsobj = json.dumps(data)
        return HttpResponse(jsobj, mimetype="application/json")

@login_required
def save(request, nbid):
    """Save cell data
    TODO think about moving saving logic into model/model manager 
    """
    nb = notebook_models.Notebook.objects.get(owner=request.user, guid=nbid)
    orderlist = request.POST.get('orderlist')
    cellsdata = json.loads(request.POST.get('cellsdata'))

    for cellid, data in cellsdata.items():
        cells = notebook_models.Cell.objects.filter(guid=cellid, notebook=nb)
        content = data["content"]
        style = data["cellstyle"]
        props = data["props"]
        if len(cells) > 0:
            cell = cells[0]
            cell.content = content
            cell.type = u"text"
            cell.style = style
            cell.props = props
            cell.save()
        else:
            cell = notebook_models.Cell(guid=cellid, 
                            notebook=nb, 
                            owner=nb.owner,
                            content=content, 
                            type=u"text", 
                            style=style, 
                            props=props)
            nb.cell_set.add(cell)
    nb.orderlist = orderlist
    nb.save()
    resp = {'resp':'ok'}
    jsobj = json.dumps(resp)
    return HttpResponse(jsobj, mimetype="application/json")

@login_required
def delete_cell(request):
    """
    XXX Not fully implemented!
    """
    if request.method == "POST":
        cellids = json.loads(request.POST.get('cellids', [None])[0])
        if isinstance(cellids, unicode):
            cellids = [cellids]
        notebook_models.Cell.objects.in_bulk(cellids).delete()
        resp = "{'resp':'ok'}"
        jsobj = json.dumps(resp)
        return HttpResponse(jsobj, mimetype="application/json")

@login_required
def revert(request, id=None):
    """Revert to Notebook with revision id.
    """
    nbid = revert_to_revision(id)
    return HttpResponseRedirect("/notebook/%s" % nbid)

@login_required
def share(request, nbid=None, template_name='notebook/share.html'):
    """Share Notebook interface.
    """
    if request.method == "POST":
        form = forms.ShareNotebook(request.POST)
        if form.is_valid():
            nb = notebook_models.Notebook.objects.get(owner=request.user, guid=nbid)
            sharedusers = form.cleaned_data['shared_user_list'].split(",")
            allcollabs = nb.collaborators.all()
            #add below logic to apps.models.Notebook XXX
            for su in sharedusers:
                username = su.strip()
                try:
                    user = User.objects.get(username=username)
                    if user not in allcollabs and user != request.user:
                        print "Adding user=> ", user
                        nb.collaborators.add(user)
                except User.DoesNotExist:
                    print "User.DoesNotExist"
            nb.save()
        return HttpResponseRedirect(reverse('notebook', args=[nbid]))
    else:
        allusers = User.objects.all() #XXX take away request.user
        nb = notebook_models.Notebook.objects.get(owner=request.user, guid=nbid)
        sharedusers = nb.collaborators.all()
        form = forms.ShareNotebook()
    return render_to_response(template_name, {'form':form, 'nbid':nbid, 'sharedusers':sharedusers, 
                                              'allusers':allusers, 'user':request.user, 'title': nb.title})












