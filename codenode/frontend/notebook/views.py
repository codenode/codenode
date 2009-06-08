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


@login_required
def save(request, nbid=None):
    """Save cell data
    """
    nb = notebook_models.Notebook.objects.get(owner=request.user, guid=nbid)


