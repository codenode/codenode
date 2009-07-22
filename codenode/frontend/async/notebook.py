
from codenode.frontend.notebook import models as nb_models
from codenode.frontend.backend import models as bkend_models

from codenode.backend import engine


class RequestRouter:
    """
    When the request gets here, it has already been associated to a User
    via a session ID (stored in the db).

    Filter Notebook table by permitted writer/evaluator (owner and
    collaborator, currently)
    Then, query notebook by id. The result will be either:
     - nb exists (therefore configured with a backend engine type)
      -- get current engine instance id, or create a new instance (implicit
      start up; this is a design decision, maybe it should be configurable)
      Use Backend admin to create new instance. 
      Use Engine client to execute request.
    - nb does not exist; return error.
    """

    def getBackendEngine(self, user_id, notebook_id):
        nb = nb_models.Notebook.objects.filter(owner=user_id).get(guid=notebook_id)
        engine_instance = bkend_models.EngineInstanceobjects.get(notebook=nb)
        return engine_instance.backend.hostname, engine_instance.id


