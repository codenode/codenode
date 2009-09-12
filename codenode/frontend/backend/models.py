
from django.db import models
from django.contrib.auth.models import User

from codenode.frontend.notebook.models import Notebook


class BackendServer(models.Model):
    """This currently assumes the server is accessed via http (xmlrpc) by
    the way the address is stored.
    """
    name = models.CharField(max_length=100)
    # put validation check in to make sure address is good
    address = models.CharField("Server address (e.g. http://localhost:9000)", max_length=100)

    def __unicode__(self):
        return u"Backend Server %s @ %s" % (self.name, self.address)

class EngineType(models.Model):
    """Establish (un)official set of attributes.
    These attributes are defined in the backend plugin.
    """
    name = models.CharField(max_length=100)
    backend = models.ForeignKey(BackendServer)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"%s Engine Type " % (self.name,)

class NotebookBackendRecord(models.Model):
    """
    Each notebook gets an engine access id from the backend server.
    The access id is a token for making computation requests to the
    backend. The backend associates the access id with an engine type.
    """
    notebook = models.ForeignKey(Notebook, unique=True, related_name='backend')
    engine_type = models.ForeignKey(EngineType)
    access_id = models.CharField(max_length=32)

    def __unicode__(self):
        return u"Notebook Engine Type: %s" % (self.engine_type,)


