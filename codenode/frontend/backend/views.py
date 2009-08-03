

from django.contrib.auth.decorators import login_required

from codenode.frontend.backend import models
from codenode.frontend.notebook import models as nb_models
from codenode.frontend.backend import rpc


@login_required
def connect_to_backend(request, backend_name):
    backend = models.BackendServer.objects.get(name=backend_name)
    engine_types = rpc.listEngineTypes(backend.address)
    for e_type in engine_types:
        engine_type = models.EngineType(name=e_type, backend=backend)
        engine_type.save()

@login_required
def runInstance(request):
    nbid = request.POST.get('nbid')
    nb = nb_models.Notebook.objects.get(guid=nbid)
    backend - nb.engine_type.backend
    engine_id = rpc.runEngineInstance(backend.address, nb.engine_type.name)
    engine_instance = models.EngineInstance(type=nb.engine_type,
                                        id=engine_id,
                                        backend=backend,
                                        owner=request.user,
                                        notebook=nb)
    engine_instance.save()
