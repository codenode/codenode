/*
######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

    TreeBranch - Dynamic tree structure branching, condensing, and grouping

*/


Notebook.TreeBranch = {}; 
Notebook.TreeBranch.MAX_SECTION_LEVEL = 5;
Notebook.TreeBranch.INPUT_LEVEL = 10;
Notebook.TreeBranch.OUTPUT_LEVEL = 11;
Notebook.TreeBranch.TEXT_LEVEL = 15;
////////////////////////////
// Cell nodes
// - spawning
// - initializing
// - changing
// - removing/deleting
////////////////////////////

Notebook.TreeBranch.spawnCellNode = function() {
    //use cellDom to make a cell node
    //give cell node Cell methods, attributes
    //return node for placement by ..
    var u = Util;
    var self = Notebook.TreeBranch;
    var cellnode = Notebook.dom.newCell();
    cellnode = $.extend(cellnode, Notebook.Cell.prototype);
    cellnode.id = u.uniqueId();
    return cellnode;
};

Notebook.TreeBranch.spawnOutCellNode = function() {
    //use cellDom to make a cell node
    //give cell node Cell methods, attributes
    //return node for placement by ..
    var u = Util;
    var self = Notebook.TreeBranch;
    var cellnode = Notebook.dom.newOutCell();
    cellnode = $.extend(cellnode, Notebook.Cell.prototype);
    cellnode.id = u.uniqueId();
    return cellnode;
};

Notebook.TreeBranch.spawnCellNodeLoad = function(cellid, cellstyle, content, props) {
    var self = Notebook.TreeBranch;
    //alert('a big fu from tbranch ie!');
    var cellnode = self.spawnCellNode();
    cellnode.id = cellid;
    cellnode.setStyle(cellstyle);
    cellnode.setType();
    self.enableSpawner(cellnode);
    cellnode.content(content);
    return cellnode;
};



Notebook.TreeBranch.enableSpawner = function(node) {
    if (!node.spawnerNode().enabled) {
        //showElement(node.spawnerNode());//xxxCnange to jquery
        //give the spawnerNode some functionality
        $.extend(node.spawnerNode(), Notebook.Spawner.prototype);
        node.spawnerNode().enabled = true;
        return;
    } else {
        return;
    }
};

Notebook.TreeBranch.disableSpawner = function(node) {
    $(node.spawnerNode()).hide();
    node.spawnerNode().enabled = false;
};

Notebook.TreeBranch.changeCell = function(style, node) {
    //need better check to see if head cell
    var self = Notebook.TreeBranch;
    if (node.isHead()) {
        var nodesbranch = node.getParentBranch();
        var nodesbranchsbranch = node.getParentBranch().getParentBranch();
        self.collapseBranch(nodesbranch);
        node.resetStyle(style);
        self.sieveBranch(nodesbranchsbranch);
    } else {
        var nodesbranch = node.getParentBranch();
        node.resetStyle(style);
        self.sieveBranch(nodesbranch);
    }
    node.adjustTextarea();
    node.setFocus();
    return;
};

Notebook.TreeBranch.changeToTitle = function(node) {
    Notebook.TreeBranch.changeCell('title',node);
};

Notebook.TreeBranch.changeToSubtitle = function(node) {
    Notebook.TreeBranch.changeCell('subtitle',node);
};

Notebook.TreeBranch.changeToSection = function(node) {
    Notebook.TreeBranch.changeCell('section',node);
};

Notebook.TreeBranch.changeToSubsection = function(node) {
    Notebook.TreeBranch.changeCell('subsection', node);
};

Notebook.TreeBranch.changeToInput = function(node) {
    Notebook.TreeBranch.changeCell('input', node);
};

Notebook.TreeBranch.putCellNodeAfter = function(oldersibling, node) {
    var self = Notebook.TreeBranch;
    $(oldersibling).after(node);
    var branchesbranch = $(oldersibling)[0].getParentBranch().getParentBranch();
    self.collapseBranch($(oldersibling)[0].getParentBranch());
    self.sieveBranch(branchesbranch);
    $('img.bracketmaskimg').ifixpng('/static/img/pixel.gif');//xxx iehack
};

Notebook.TreeBranch.putCellNodeAtTop = function(node) {
    $('#main > :first-child').before(node);
};

Notebook.TreeBranch.removeCellNode = function(node) {
    var self = Notebook.TreeBranch;
    var parentbranch = node.getParentBranch();
    $(node).remove();
    self.sieveBranch(parentbranch);
};

Notebook.TreeBranch.deleteCellNode = function(node) {
    var self = Notebook.TreeBranch;
    var branchesbranch = $(node)[0].getParentBranch().getParentBranch();
    self.collapseBranch($(node)[0].getParentBranch());
    $(node).remove();
    self.sieveBranch(branchesbranch);

};

Notebook.TreeBranch.setOutputCell = function(outputnode, inputid) {
    var self = Notebook.TreeBranch;
    var node = $('#'+inputid)[0];
    if (node.isHead()) {
        //very hack, assumes one output cell after input...and stuff
        self.removeCellNode(node.nextCell());
    }
    self.putCellNodeAfter(node, outputnode);
    var oid = outputnode.id;
    $('img.outputimage').one('load', oid, function(e) {
            $('#'+e.data)[0].adjustTextarea();
            });
    outputnode.adjustTextarea();
    //outputnode.saved = true;
    if ($('#auxdisplay').html() == 'spawner') {
        outputnode.spawnerNode().setFocus();
    }
    self.sieveBranch(node.getParentBranch());
};

Notebook.TreeBranch.setNullOutputCell = function(inputid) {
    var self = Notebook.TreeBranch;
    var node = $('#'+inputid)[0];
    if (node.isHead()) {
        //very hack, assumes one output cell after input...and stuff
        self.removeCellNode(node.nextCell());
    }
    self.sieveBranch(node.getParentBranch());
};

Notebook.TreeBranch.spawnOutputCellNode = function(id, cellstyle, content, count) {
    var self = Notebook.TreeBranch;
    if (content.length > 0) {
        var node = self.spawnOutCellNode();
        //here we check for what kind of content the server returned
        node.setStyle(cellstyle);
        node.id = id + 'o';
        node.setType();
        self.enableSpawner(node);
        node.content(content);
        node.numberLabel(count);
        self.setOutputCell(node, id);
        return;
    } else {
        self.setNullOutputCell(id);
    }
    //$(id).spawnerNode().setFocus();
};

Notebook.TreeBranch.spawnInputCellNode = function() {
    var self = Notebook.TreeBranch;
    var node = self.spawnCellNode();
    node.setStyle('input');
    node.setType();
    self.enableSpawner(node);
    return node;
};

Notebook.TreeBranch.spawnTitleCellNode = function() {
    var self = Notebook.TreeBranch;
    var node = self.spawnCellNode();
    node.setStyle('title');
};

/////////////////////////////////////
// Cellnode organization in the DOM
//
/////////////////////////////////////

Notebook.TreeBranch.loadSieve = function(orderlist) {
    var self = Notebook.TreeBranch;
    for (cell in orderlist) {
        var cellid = orderlist[cell];
        var cellnode = $('#'+cellid)[0];
        cellnode.adjustTextarea();
        var nodes = self.getNextCellsToAbsorb(cellnode);
        if (nodes.length > 0) {
            var branchnode = self.branchAtNode(cellnode);
        }
    }
    $('img.bracketmaskimg').ifixpng();//xxx iehack

};

Notebook.TreeBranch.sieveBranch = function(branchnode) {
    var self = Notebook.TreeBranch;
    var branchlevel = branchnode.getCellLevel();
    //generalize getting headnode?
    var headnode = branchnode.contentNode().firstChild;
    var curnode = headnode;
    var curlevel = headnode.getCellLevel();
    while (curnode.nextCell()) {
        var nextnode = curnode.nextCell();
        var nextlevel = nextnode.getCellLevel();
        if (nextlevel <= branchlevel) {
            var nodes = self.collapseBranchAtNode(nextnode);
            $(branchnode).after(nodes);
            var parentbranch = branchnode.getParentBranch();
            return self.sieveBranch(parentbranch);
        } else if (nextlevel < curlevel) {
            //need better check to see if already branched
            if (!nextnode.isGroup()) { 
                var newbranch = self.branchAtNode(nextnode);
                if (newbranch.isGroup()) {
                    //new branch was created by branchAtNode
                    nextnode = newbranch;
                    nextlevel = nextnode.getCellLevel();
                    self.sieveBranch(newbranch);
                }
            }
        } else if (nextlevel > curlevel) {
            curnode = self.absorbNode(curnode, nextnode);
        }
        //if we get here, then check next cellnode
        curnode = nextnode;
        curlevel = nextlevel;
    }
};

//future
Notebook.TreeBranch.sieveOnChange = function(changednode) {
    var self = Notebook.TreeBranch;
    if (changednode.isHead()) {
        self.collapseBranch(changednode.getParentBranch());
    }
};

Notebook.TreeBranch.absorbNode = function(absorbernode, nodetoabsorb) {
    var self = Notebook.TreeBranch;
    if (absorbernode.isHead()) {
        //don't do anything
        return absorbernode;
    }
    if (!absorbernode.isGroup()) {
        var absorbernode = self.branchAtNode(absorbernode);
    } else {
        self.growBranch(absorbernode);
    }
    return absorbernode;
};

Notebook.TreeBranch.growBranch = function(branchnode) {
    var self = Notebook.TreeBranch;
    var nodes = self.getNextSiblingsToAbsorb(branchnode);
    nodes = $(nodes).remove(); 
    $(branchnode.contentNode()).append(nodes);
    return;
};
        
Notebook.TreeBranch.branchAtNode = function(node) {
    var self = Notebook.TreeBranch;
    var nodes = self.getNextSiblingsToAbsorb(node);
    nodes = $(nodes).remove();
    if (nodes.length > 0) {
        var groupnode = self.makeGroupNode();
        $(node).replaceWith(groupnode);
        //$(groupnode.contentNode()).append(nodes);
        //$(groupnode.contentNode()).prepend(node);
        groupnode.appendChildCells(nodes);
        groupnode.prependChildCells(node);
        $('img.bracketmaskimg').ifixpng();//xxx iehack
        return groupnode;
    } else {
        return node;
    }
};

//Only function that depends on DOM / spawnNode
Notebook.TreeBranch.makeGroupNode = function() {
    var u = Util;
    var self = Notebook.TreeBranch;
    var node = Notebook.dom.groupCell();
    node = $.extend(node, Notebook.Cell.prototype);
    node.id = u.uniqueId();
    node.setAsGroup();
    //node.appendChildCells(nodes);
    return node;
};

Notebook.TreeBranch.collapseBranch = function(node) {
    //should node be the branch's group node, or the head node?
    //need to make sure node is a group...
    var self = Notebook.TreeBranch;
    if (node.id == 'main') {
        return; //xxxHack to prevent deleting main
    };
    var headnode = node.contentNode().firstChild;
    var nodes = self.collapseBranchAtNode(headnode);
    $(node).after(nodes);
    //remove group node;
    $(node).remove();
    return;
};

Notebook.TreeBranch.collapseBranchAtNode = function(node) {
    //var self = Notebook.TreeBranch;
    //var nodes = self.getAllNextSiblingNodes(node);
    var nodes = $(node).add($(node).nextAll()).remove();
    return nodes;
};

Notebook.TreeBranch.getAllNextSiblingNodes = function(node) {
    var curnode = node;
    var nodes = [];
    while (curnode.nextCell()) {
        nodes.push(curnode.nextCell());
        curnode = curnode.nextCell();
    }
    return nodes;
};

Notebook.TreeBranch.getNextSiblingsToAbsorb = function(node) {
    var self = Notebook.TreeBranch;
    var curnode = node;
    var matchlevel = node.getCellLevel();
    var nodes = [];

    if (matchlevel < self.MAX_SECTION_LEVEL) { 
        while (curnode.nextCell()) {
            if (curnode.nextCell().getCellLevel() > matchlevel) {
                nodes.push(curnode.nextCell());
                curnode = curnode.nextCell();
            } else {
                break;
            }
        }
    } else if (matchlevel == self.INPUT_LEVEL) {
        while (curnode.nextCell()) {
            if (curnode.nextCell().getCellLevel() == self.OUTPUT_LEVEL) {
                nodes.push(curnode.nextCell());
                curnode = curnode.nextCell();
            } else {
                break;
            }
        }
    }
    return nodes;
};

Notebook.TreeBranch.getNextCellsToAbsorb = function(node) {
    var self = Notebook.TreeBranch;
    var nodes = [];
    if (!node.isHead()) {
        var curnode = node;
        var matchlevel = node.getCellLevel();
        if (matchlevel < self.MAX_SECTION_LEVEL) { 
            while (curnode.nextCell()) {
                if (curnode.nextCell().getCellLevel() > matchlevel) {
                    nodes.push(curnode.nextCell());
                    curnode = curnode.nextCell();
                } else {
                    break;
                }
            }
        } else if (matchlevel == self.INPUT_LEVEL) {
            while (curnode.nextCell()) {
                if (curnode.nextCell().getCellLevel() == self.OUTPUT_LEVEL) {
                    nodes.push(curnode.nextCell());
                    curnode = curnode.nextCell();
                } else {
                    break;
                }
            }
        }
    }
    return nodes;
};


