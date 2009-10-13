######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

import os
from whoosh import index
from whoosh import analysis
from whoosh.qparser import QueryParser
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.filedb.filestore import FileStorage

from django.db.models import signals
from django.conf import settings

from codenode.frontend.notebook import models

SEARCH_INDEX = settings.SEARCH_INDEX
SEARCH_SCHEMA = Schema(
    nbid=KEYWORD(stored=True), 
    owner=KEYWORD(stored=True), 
    title=TEXT(field_boost=3), 
    content=TEXT(analyzer=analysis.FancyAnalyzer())
)

def create_index(**kwargs):
    if not os.path.exists(SEARCH_INDEX):
        os.mkdir(SEARCH_INDEX)
        storage = FileStorage(SEARCH_INDEX)
        storage.create_index(SEARCH_SCHEMA)
#Django signal registration
signals.post_syncdb.connect(create_index)

def update_index(**kwargs):
    instance = kwargs['instance']
    ix = index.open_dir(SEARCH_INDEX)
    writer = ix.writer()
    instvars = [instance.notebook.guid, instance.notebook.owner, instance.notebook.title, instance.content]
    nbid, owner, title, content = [unicode(e) for e in instvars] #XXX is this unicode usage correct?
    writer.add_document(nbid=nbid, owner=owner, title=title, content=content)
    writer.commit()
#Django signal registration
signals.post_save.connect(update_index, sender=models.Cell)

def search(q, default_field="content"):
    ix = index.open_dir(SEARCH_INDEX)
    searcher = ix.searcher()
    parser = QueryParser(default_field, schema=ix.schema)
    query = parser.parse(q)
    results = searcher.search(query)
    return results

def delete(**kwargs):
    """Remove deleted Notebook's Cells from the Index.
    """
    instance = kwargs['instance']
    ix = index.open_dir(SEARCH_INDEX)
    searcher = ix.searcher()
    parser = QueryParser("nbid", schema=ix.schema)
    query = parser.parse(instance.guid)
    number_deleted = ix.delete_by_query(query)
    ix.commit()
#Django signal registration
signals.post_delete.connect(delete, sender=models.Notebook)
