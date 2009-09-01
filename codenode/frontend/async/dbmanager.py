######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

from codenode.frontend.notebook import models

class NotebookSession(object):

    def __init__(self, id):
        self.id = id

    def save_notebook_metadata(self, orderlist, cellsdata):
        #print 'save_notebook_metadata'
        #print orderlist, cellsdata
        nb = models.Notebook.objects.get(guid=self.id)
        for cellid, data in cellsdata.items():
            cells = models.Cell.objects.filter(guid=cellid)
            content = data["content"]
            style = data["cellstyle"]
            props = data["props"]
            if len(cells) > 0:
                cell = cells[0]
                #print 'lenCELLS > 0', cell
                cell.content = content
                cell.type = u"text"
                cell.style = style
                cell.props = props
                cell.save()
            else:
                #print 'NO CELLS'
                cell = models.Cell(guid=cellid, 
                                notebook=nb, 
                                owner=nb.owner,
                                content=content, 
                                type=u"text", 
                                style=style, 
                                props=props)
                nb.cell_set.add(cell)
        #print 'save orderlist'
        nb.orderlist = orderlist
        nb.save()
        return

    def get_notebook(self):
        nb = models.Notebook.objects.get(guid=self.id)
        return nb

    def getSystem(self):
        nb = self.get_notebook()
        system = nb.system
        return system

    def get_notebook_data(self):
        """return a dictionary object representation of a notebooks data for
        use by:
         - js in web browser
         - printers
         """
        nb = self.get_notebook()
        cells = models.Cell.objects.filter(notebook=nb)

        nbdata, cellsdata = {}, {}
        for cell in cells:
            cellsdata[cell.guid] = {'content':cell.content, 'cellstyle':cell.style, 'props':cell.props}
        nbdata['cells'] = cellsdata
        nbdata['settings'] = {'cell_input_border':'None', 'cell_output_border':'None'}
        nbdata['nbid'] = nb.guid
        nbdata['orderlist'] = nb.orderlist
        nbdata['title'] = nb.title
        return nbdata

    def change_notebook_metadata(self, title):
        #XXX need to generalize
        nb = self.get_notebook()
        nb.title = unicode(title)
        nb.save()

    def save_cell(self, id, content, type, style, props):
        id, content, type, style, props = [unicode(w) for w in [id, content, type, style, props]]
        nb = self.get_notebook()
        #cell, created = models.Cell.objects.get_or_create(guid=id, owner=nb.owner)
        cells = models.Cell.objects.filter(guid=id)
        if len(cells) == 0:
            cell = models.Cell(guid=id, owner=nb.owner)
        else:
            cell = cells[0]
        cell.content = content
        cell.type = type
        cell.style = style
        cell.props = props
        if len(cells) == 0:
            nb.cell_set.add(cell)
            nb.save()
        else:
            cell.save()

    def delete_cells(self, cellids):
        """Delete 1 or more cells from a Notebook.

        'cellids' is either 1 cellid or a list of cellids

        (Note: There may be a cleaner way to del cells?)
        """
        nb = self.get_notebook()
        if isinstance(cellids, unicode):
            cellids = [cellids]
        models.Cell.objects.in_bulk(cellids).delete()



