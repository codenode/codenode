from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from codenode.frontend.bookshelf import models as bookshelf_models
from codenode.frontend.notebook import models as notebook_models

from codenode.frontend.notebook import forms 

@login_required
def notebook(request, nbid=None, template_name='notebook/notebook.html'):
    """Render the Notebook interface.
    """
    nb = notebook_models.Notebook.objects.get(owner=request.user, guid=nbid)
    lastmod = nb.created_time #XXX
    return render_to_response(template_name, {'title':nb.title, 'lastmod':lastmod, 'nbid':nbid, 'user':request.user})

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
        newtitle = request.POST.get('newtitle', [None])[0]
        nb = notebook_models.Notebook.objects.get(owner=request.user, guid=nbid)
        nb.title = unicode(title)
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
    orderlist = ",".join(request.POST.get('orderlist', []))
    cellsdata = request.POST.get('cellsdata', [None])[0]
    cellsdata = json.loads(cellsdata)

    for cellid, data in cellsdata.items():
        cells = notebook_models.Cell.objects.filter(guid=cellid, notebok=nb)
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

    resp = "{'resp':'ok'}"
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
        return HttpResponseRedirect("/notebook/%s" % nbid) #XXX generalize
    else:
        allusers = User.objects.all() #XXX take away request.user
        nb = notebook_models.Notebook.objects.get(owner=request.user, guid=nbid)
        sharedusers = nb.collaborators.all()
        form = forms.ShareNotebook()
    return render_to_response(template_name, {'form':form, 'nbid':nbid, 'sharedusers':sharedusers, 'allusers':allusers, 'user':request.user})












