import itertools
from codenode.frontend.notebook.models import Notebook, Cell

class Revision(object):
    def __init__(self, id, timestamp, changes=None):
        self.id = id
        self.timestamp = timestamp
        self.changes = changes

def get_nb_revisions(nbid):
    """Get only the first nb revesion object if 
    there are in-a-row repeating orderlists.
    """
    nbrevs = Notebook.revisions.filter(guid=nbid)
    nbs = [(nb.orderlist, nb) for nb in nbrevs if nb.orderlist != 'orderlist']
    order_unique = [(c, list(cgen)[0][1]) for c,cgen in itertools.groupby(nbs, lambda x:x[0])]

    revisions = []
    id = len(order_unique)
    for nbtuple in order_unique:
        orderlist,nb = nbtuple
        cell_data = get_cell_revision_diff(orderlist)
        rev = Revision(id, nb._audit_timestamp)
        rev.changes = " ".join(cell_data)
        revisions.append(rev)
        id = id - 1
    return revisions

def get_cell_revision_diff(orderlist):
    orderlist = orderlist.split(",")
    allcontent = []
    for cellid in orderlist:
        cellrevs = Cell.revisions.filter(guid=cellid)[0] #most recent
        allcontent.append(cellrevs.content.replace("\n", ""))
    return allcontent

