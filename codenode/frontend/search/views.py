from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json

from codenode.frontend.search import search

@login_required
def search_view(request):
    q = request.GET.get("q")
    result0 = search.search(q)
    result1 = search.search(q, default_field="title")
    result0.upgrade_and_extend(result1)
    results = [res["nbid"] for res in result0] # if res["owner"] == request.user]
    jsobj = json.dumps({"query":q, "results":results})
    return HttpResponse(jsobj, mimetype='application/json')
