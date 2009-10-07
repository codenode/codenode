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


@login_required
def save(request, nbid=None):
    """Save cell data
    """
    nb = notebook_models.Notebook.objects.get(owner=request.user, guid=nbid)


