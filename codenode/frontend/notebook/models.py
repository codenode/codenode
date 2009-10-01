######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from codenode.frontend.notebook import revision

class Notebook(models.Model):
    guid = models.CharField(max_length=32, unique=True, editable=False) #needs to be globally unique
    owner = models.ForeignKey(User)
    collaborators = models.ManyToManyField(User, blank=True, related_name='notebook_collaborator')
    viewers = models.ManyToManyField(User, blank=True, related_name='notebook_viewer')
    title = models.CharField(max_length=100, default='untitled')
    # The location should be handled by a bookshelf model
    location = models.CharField(max_length=100, default='root')
    created_time = models.DateTimeField(auto_now_add=True)
    orderlist = models.TextField(editable=False, default='orderlist')

    revisions = revision.AuditTrail()

    def save(self):
        if not self.guid:
            self.guid = str(uuid.uuid4()).replace("-", "")
        super(Notebook, self).save()

    def last_modified_time(self):
        """Last time corresponding Notebook was modified.

        This is equivalent to finding the most recently modified Cell in this Notebook.
        """
        try:
            return self.cell_set.latest(field_name="last_modified").last_modified
        except Cell.DoesNotExist:
            return self.created_time
    
    def last_modified_by(self):
        """User who modified corresponding Notebook last; 

        Find who recently modified the last modified cell in this Notebook
        """
        try:
            # this really needs cell to have a last_modified_by attribute
            return self.cell_set.latest(field_name="last_modified").owner
        except Cell.DoesNotExist: 
            return self.owner

    class Meta:
        verbose_name = _('Notebook')
        verbose_name_plural = _('Notebooks')
    
    def __unicode__(self):
        return u"Notebook '%s' owned by '%s'" % (self.title, self.owner)
 

class Cell(models.Model):
    guid = models.CharField(primary_key=True, max_length=50, unique=True, editable=False) #created by javascript - needs to be globally unique
    owner = models.ForeignKey(User)
    notebook = models.ForeignKey(Notebook)
    content = models.TextField()
    style = models.TextField() #json object that holds style settings.
    type = models.CharField(max_length=100) 
    props = models.TextField() 
    last_modified = models.DateTimeField(auto_now=True)

    revisions = revision.AuditTrail()

    def save_evaluate(self, json_obj):
        """
        save a cell during an evalutate. (Temp name)
        format:
        {content:input,
         
        """

    def save_result(self, json_obj):
        """
        save data resulting from an evaluation. (Temp name)
        """
    #def save(self):
        #update Notebook last modified time.

    class Meta:
        verbose_name = _('Cell')
        verbose_name_plural = _('Cells')
    
    def __unicode__(self):
        return u"Cell in Notebook '%s'" % (self.notebook.title, )
 


