/*
######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

    SaveLoad.js - saving and loading cell data.

*/


Notebook.Save = {};

Notebook.Save.getUnsavedCellList = function(orderlist) {
    function dosave(cellid, i) {
        return !$('#'+cellid)[0].saved;
    }
    var tosave = $.grep(orderlist, dosave); 
    return tosave;
};

/** generateOrderList - a list of cell Id's (str) in canonical order */
Notebook.Save.generateOrderList = function() {
    var cellnodes = $('div.cell:not(.group)');
    if(cellnodes.length > 0) {
        var orderlist = $.map(cellnodes, function(n, i) {
                return $(n).attr('id');
                });
    } else {
        var orderlist = ['none'];
    }
    return orderlist;
};

Notebook.Save.generateCellData = function(cellids) {
    var cellsdata = {};
    for (c in cellids) {
        var cellid = cellids[c];
        var cellnode = $('#'+cellid)[0];
        var cellstyle = cellnode.cellstyle;
        var content = cellnode.content();
        var props = JSON.stringify(cellnode.getProps());
        cellsdata[cellid] = {'cellstyle':cellstyle,
                            'content':content,
                            'props':props};
    }
    return cellsdata;
};

Notebook.Save._save = function(success, error) {
    var self = Notebook.Save;
    var orderlist = self.generateOrderList();
    if (orderlist[0] != 'none') {
        var tosave = self.getUnsavedCellList(orderlist);
        var cellsdata = self.generateCellData(tosave);
        Notebook.Save.tosave = tosave;
        Notebook.Async.saveToDatabase(orderlist, cellsdata, success, error);
    } else {
        success(true);//slightly hacky
    }
};

Notebook.Save.save = function() {
    Notebook.Indicator.save();
    var self = Notebook.Save;
    self._save(self.saveSuccess, self.saveError);
};

Notebook.Save.saveAndClose = function() {
    Notebook.Indicator.save();
    var self = Notebook.Save;
    self._save(self.saveCloseSuccess, self.saveError);
};

Notebook.Save.saveSuccess = function(res) {
    var self = Notebook.Save;
    Notebook.Indicator.saved();
    for (id in self.tosave) {
        $('#'+self.tosave[id])[0].saved = true;
    }
};

Notebook.Save.saveCloseSuccess = function(res) {
    /* Close window or go back depending on User settings*/
    if (NOTEBOOK_OPENS_IN_NEW_WINDOW){ 
        window.close();
    } else {
        window.location="/bookshelf/"; /*XXX How to not hardcode this?*/
    }
};

Notebook.Save.saveError = function(res) {
    Notebook.Indicator.saveError();
};


Notebook.Load = {};

Notebook.Load.takeCellsData = function(nbobject) {
    var orderlist = nbobject.orderlist.split(',');
    var orderlist = eval(nbobject.orderlist);
    //check if this nb is new/empty
    if (orderlist[0] == 'orderlist') {
        return;
    }
    var cellsdata = nbobject.cells;
    var nodes = [];
    for (c in orderlist) {
        try {
            var cellid = orderlist[c];
            var cellstyle = cellsdata[cellid]['cellstyle'];
            var content = cellsdata[cellid]['content'];
            var props = cellsdata[cellid]['props'];
            var node = Notebook.TreeBranch.spawnCellNodeLoad(cellid, cellstyle, content, props);
            node.saved = true;
            nodes.push(node);
        } catch (err) {
            continue;
        }
    }
    Notebook.TreeBranch.putCellNodeAtTop(nodes);
    Notebook.TreeBranch.loadSieve(orderlist);
    $('img.outputimage').one('load', function(e) {
            $(e.currentTarget).parents('div.cell.output')[0].adjustTextarea();
            });
};




