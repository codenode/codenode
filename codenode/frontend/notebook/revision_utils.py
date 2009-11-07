######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

from django.utils import simplejson as json
from codenode.frontend.notebook.models import Notebook, Cell

def get_nb_revisions(nbid, n=25):
    """Get notebook revisions.

    TODO: Only show 'n' revisions per page.
    """
    #Get all Notebook revisions, orderlist='orderlist' means there are no meaningful revisions:
    nbrevs = Notebook.revisions.filter(guid=nbid).exclude(orderlist='orderlist')
    revisions = []
    for nb in nbrevs:
        orderlist = nb.orderlist
        current_audit_id, current_audit_ts = nb._audit_id, nb._audit_timestamp #id and timestamp of nb revision snapshot.
        recent_cells = get_recent_cells(orderlist, current_audit_ts)
        revisions.append((current_audit_id, current_audit_ts, recent_cells))
    unique_revisions = get_unique_revisions(revisions)
    return unique_revisions

def get_unique_revisions(revisions):
    """Find in-order unique revisions.
    In other words, drop all in-a-row duplicate revisions.
    """
    uniques = []
    current_audit_id, current_audit_ts, current = revisions.pop(0)
    for (current_audit_id, current_audit_ts, previous) in revisions:
        if current != previous:
            codediff = diff_from_previous(current, previous)
            uniques.append((current_audit_id, current_audit_ts, codediff, current))
        current = previous
    return uniques

def get_recent_cells(orderlist, current_audit_ts):
    """The latest (cellid, content) for all cells in give 'orderlist'.
    The 'current_nb_ts' is the timestamp of the notebook snapshot.
    """
    orderlist = json.loads(orderlist)
    allcontent = []
    for cellid in orderlist:
        cellrevs = Cell.revisions.filter(guid=cellid, _audit_timestamp__lte=current_audit_ts).order_by("-_audit_timestamp")[0] #most recent
        allcontent.append((cellid, cellrevs.content))
    return allcontent

def diff_from_previous(current, previous):
    """Difference of current to previous diff.
    Only take content that is input, and hence the cell id
    does not end in "o", which signifies output.
    """
    diff = set(current).symmetric_difference(set(previous))
    revdiff = reversed(list(diff))
    codediff = " | ".join([s[1].replace("\n", "") for s in revdiff if s[0][-1] != "o"])
    return codediff


def revert_to_revision(id):
    """Revert to revision with given id.
    Copy all neeed data into new models and save,
    which will create fresh timestamps and audit_id 
    for the new Notebook and Cell data.

    Returns original Notebook id.
    """
    #XXX The below code could _definitely_ be optimized:
    nbrev = Notebook.revisions.get(_audit_id=id)
    ts = nbrev._audit_timestamp
    nb = Notebook.objects.get(guid=nbrev.guid)
    nb.orderlist = nbrev.orderlist
    nb.save()
    orderlist = json.loads(nbrev.orderlist)
    for cellid in orderlist:
        cellrev = Cell.revisions.filter(guid=cellid, _audit_timestamp__lte=ts).order_by("-_audit_timestamp")[0] #most recent
        cell = Cell.objects.get(guid=cellrev.guid)
        cell.content, cell.style, cell.type, cell.props = cellrev.content, cellrev.style, cellrev.type, cellrev.props
        cell.save()
    return nb.guid
