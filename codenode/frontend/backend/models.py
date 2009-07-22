
from django.db import models
from django.contrib.auth.models import User

from codenode.frontend.notebook.models import Notebook

class BackendServer(models.Model):
    name = models.CharField(max_length=100)
    hostname = models.CharField(max_length=100)
    portnumber = models.PositiveIntegerField()
    #up = models.BooleanField()

    def __unicode__(self):
        return u"Backend Server %s @ %s:%d" % (self.name, self.hostname,
                self.portnumber)

class EngineType(models.Model):
    """Establish (un)official set of attributes.
    These attributes are defined in the backend plugin.
    """
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    backend = models.ForeignKey(BackendServer)
    description = models.TextField()

    def __unicode__(self):
        return u"%s Engine Type for the %s language" % (self.name, self.language)

class EngineInstance(models.Model):
    type = models.ForeignKey(EngineType)
    id = models.CharField(max_length=32)
    backend = models.ForeignKey(BackendServer)
    owner = models.ForeignKey(User) #This or just Notebook guid?
    notebook = models.ForeignKey(Notebook)
    created_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s Engine Instance %s @ %s" % (self.type, self.id,
                self.backend)
