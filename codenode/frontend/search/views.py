######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json

from codenode.frontend.notebook.models import Notebook
from codenode.frontend.search import search

@login_required
def search_view(request):
    q = request.GET.get("q")
    result0 = search.search(q)
    result1 = search.search(q, default_field="title")
    result0.upgrade_and_extend(result1)
    owner = request.user.username
    nbids = [res["nbid"] for res in result0 if res["owner"] == owner]
    nbs = Notebook.objects.filter(guid__in=nbids, owner=request.user).order_by("created_time")
    results = [[e.guid, e.title, e.backend.all()[0].engine_type.name, e.last_modified_time().strftime("%Y-%m-%d %H:%M:%S"), e.location] for e in nbs]
    jsobj = json.dumps({"query":q, "results":results})
    return HttpResponse(jsobj, mimetype='application/json')
