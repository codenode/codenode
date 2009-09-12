
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson as json

from codenode.frontend.backend import models
from codenode.frontend.notebook import models as nb_models
from codenode.frontend.backend import rpc


@login_required
def connect_to_backend(request, backend_name):
    """
    This is done by the admin manager thing...
    """
    backend = models.BackendServer.objects.get(name=backend_name)
    engine_types = rpc.listEngineTypes(backend.address)
    for e_type in engine_types:
        engine_type = models.EngineType(name=e_type, backend=backend)
        engine_type.save()

    jsobj = json.dumps(engine_types)
    return HttpResponse(jsobj, mimetype='application/json')

@login_required
def update_engine_types(request, backend_name):
    """Simple way to sync up with the backend on which engine types it has.
    Only add ones that don't match with existing engine types.

    So far, only return json obj of new types...
    """
    backend = models.BackendServer.objects.get(name=backend_name)
    engine_types = rpc.listEngineTypes(backend.address)
    existing_types = models.EngineType.objects.filter(backend=backend).values_list('name', flat=True)
    new_types = []
    for e_type in engine_types:
        if e_type not in existing_types:
            new_types.append(e_type)
            new_engine_type = models.EngineType(name=e_type, backend=backend)
            new_engine_type.save()
    #return render_to_response(template_name, {'new_types':new_types}) 
    jsobj = json.dumps(new_types)
    return HttpResponse(jsobj, mimetype='application/json')







