import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Notebook(models.Model):
    guid = models.CharField(max_length=32, unique=True, editable=False) #needs to be globally unique
    owner = models.ForeignKey(User)
    collaborators = models.ManyToManyField(User, blank=True, related_name='notebook_collaborator')
    viewers = models.ManyToManyField(User, blank=True, related_name='notebook_viewer')
    title = models.CharField(max_length=100)
    system = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    style = models.CharField(max_length=2048) #json object that holds style settings.
    created_time = models.DateTimeField(auto_now=True)

    def save(self):
        if not self.guid:
            self.guid = str(uuid.uuid4()).replace("-", "")
        super(Notebook, self).save()

    def last_modified_time(self, owner):
        """Last time corresponding Notebook was modified.

        This is equivalent to finding the most recently modified Cell in this Notebook.
        """
        try:
            q = Cell.objects.filter(owner=owner).latest(field_name="last_modified")
            return unicode(q.last_modified).split(".")[0]
        except Cell.DoesNotExist:
            return unicode(self.created_time).split(".")[0]
        
    
    def last_modified_by(self, owner):
        """User who modified corresponding Notebook last; 

        Find who recently modified the last modified cell in this Notebook
        """
        #XXX implement correctly
        return Cell.objects.filter(owner=owner).latest(field_name="last_modified").last_modified_by

    class Meta:
        verbose_name = _('Notebook')
        verbose_name_plural = _('Notebooks')
    
    def __unicode__(self):
        return u"Notebook '%s' ownded by '%s'" % (self.title, self.owner)
 

class Cell(models.Model):
    guid = models.CharField(max_length=50, unique=True) #created by javascript - needs to be globally unique
    owner = models.ForeignKey(User)
    notebook = models.ForeignKey(Notebook)
    content = models.CharField(max_length=65535) #the code
    style = models.CharField(max_length=1024) #json object that holds style settings.
    type = models.CharField(max_length=100) 
    props = models.CharField(max_length=100) 
    last_modified = models.DateTimeField(auto_now=True)

    #def save(self):
        #update Notebook last modified time.

    class Meta:
        verbose_name = _('Cell')
        verbose_name_plural = _('Cells')
    
    def __unicode__(self):
        return u"Cell in Notebook '%s'" % (self.notebook.title, )
 


