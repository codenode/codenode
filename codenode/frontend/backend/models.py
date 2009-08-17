
from django.db import models
from django.contrib.auth.models import User

from codenode.frontend.notebook.models import Notebook

class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

class BackendServer(models.Model):
    """This currently assumes the server is accessed via http (xmlrpc) by
    the way the address is stored.
    """
    name = models.CharField(max_length=100)
    # put validation check in to make sure address is good
    address = models.CharField("Server address (e.g. http://localhost:9000)", max_length=100)
    #last_contact = models.DateTimeField(auto_now=True)
    #up = models.BooleanField()

    def __unicode__(self):
        return u"Backend Server %s @ %s" % (self.name, self.address)

class EngineType(models.Model):
    """Establish (un)official set of attributes.
    These attributes are defined in the backend plugin.
    """
    name = models.CharField(max_length=100)
    #language = models.ForeignKey(ProgrammingLanguage, null=True, blank=True)
    # It might be better to allow multiple backends to support the same
    # engine type. Also, should defining attributes of a type include
    # specific environment details (data, packages, etc.)?
    backend = models.ForeignKey(BackendServer)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"%s Engine Type " % (self.name,)

class EngineTypesToBackends(models.Model):
    """Many to Many relation. Many backends can support the same engine
    type.
    """
    type = models.ForeignKey(EngineType)
    backend = models.ForeignKey(BackendServer)

class EngineInstance(models.Model):
    type = models.ForeignKey(EngineType)
    instance_id = models.CharField(max_length=32, blank=True)
    backend = models.ForeignKey(BackendServer)
    owner = models.ForeignKey(User) #This or just Notebook guid?
    notebook = models.ForeignKey(Notebook, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    termination_time = models.DateTimeField(auto_now=False, blank=True, null=True)

    def __unicode__(self):
        return u"%s Engine Instance %s @ %s" % (self.type, self.instance_id,
                self.backend)


class EngineTypeToNotebook(models.Model):
    """Relate a notebook document to an engine type.
    This table is for remembering a notebook's default engine type.
    """
    type = models.ForeignKey(EngineType)
    notebook = models.ForeignKey(Notebook, unique=True, related_name='engine_types')



