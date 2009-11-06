/*
######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

 Notebook.Cell -- A cell objects methods and attributes
 */

Notebook.Cell = function() {
    // this constructor doesn't ever get called
    //Cell.prototype is a set of methods and attributes given to
    //DOM nodes.
    //In this version of the notebook js, MochiKit.Base.update is used
    // to give each cell node (a DOM object) its functionality
    // A new Cell object is never actually created
    this.conrad = 'uno';
};


//or, 
//Notebook.Cell.prototype = {};
//?

/////////////////////////////
// Cell Options/Properties // 
/////////////////////////////

Notebook.Cell.prototype.initCommon = function() {
    this.cell = true;
    this.evaluating = 0;
    this.completing = false;
    this.saved = false;
};

Notebook.Cell.prototype.getProps = function() {
    var props = {
        cellstyle: this.cellstyle,
        cellevel: this.cellevel, //redundant?
        open: this.open
    }
    return props;
};


Notebook.Cell.prototype.setStyle = function(cellstyle) {
    //common default properties
    this.initCommon();
    this.cellstyle = cellstyle;
    this.open = true;
    this.oldcontent = '';
    this.spawnerNode().enabled = false;

    switch(cellstyle) {
        case 'title':
            this.celltype = 'input';
            this.cellevel = 1;
            this.evaluatable = false;
            this.editable = true;
            this.className = 'cell title';
            break;
        case 'subtitle':
            this.celltype = 'input';
            this.cellevel = 2;
            this.evaluatable = false;
            this.editable = true;
            this.className = 'cell subtitle';
            break;
        case 'section':
            this.celltype = 'input';
            this.cellevel = 3;
            this.evaluatable = false;
            this.editable = true;
            this.className = 'cell section';
            break;
        case 'subsection':
            this.celltype = 'input';
            this.cellevel = 4;
            this.evaluatable = false;
            this.editable = true;
            this.className = 'cell subsection';
            break;
        case 'input':
            //logDebug('setinput');
            this.celltype = 'input';
            this.cellevel = 10;
            this.evaluatable = true;
            this.editable = true;
            this.className = 'cell input';
            break;
        case 'outputtext':
            this.celltype = 'output';
            this.cellevel = 11;
            this.evaluatable = false;
            this.editable = false;
            //this.className = 'cell outputtext';
            this.className = 'cell output';
            break;
        case 'outputimage':
            this.celltype = 'output';
            this.cellevel = 11;
            this.evaluatable = false;
            this.editable = false;
            this.className = 'cell output';
            break;
        case 'text':
            this.celltype = 'input';
            this.cellevel = 15;
            this.evaluatable = false;
            this.editable = true;
            this.className = 'cell text';
            break;
        case 'group':
            this.celltype = 'group';
            this.cellevel = -1;
            this.evaluatable = false;
            this.editable = false;
            this.className = 'cell group';
            break;
        case 'text':
        //need some attribute keeping this from being a head
            this.celltype = 'text';
            this.cellevel = 20;
            this.evaluatable = false;
            this.editable = true;
            this.className = 'cell text';
            this.canbehead = false;
            break;
    }
};

Notebook.Cell.prototype.setAsInput = function() {
    this.setStyle('input');
};

Notebook.Cell.prototype.setAsOutput = function() {
    this.setStyle('output');
};

Notebook.Cell.prototype.setAsGroup = function() {
    this.setStyle('group');
    $(this.spawnerNode()).hide();//xxx
};

Notebook.Cell.prototype.setType = function() {
    switch(this.celltype) {
        case 'input':
            $(this.contentNode()).append(Notebook.dom._textarea());
            this.textareaNode().cellid = this.id;
            this.textareaNode().eventtype = 'input';
            break;
        case 'output':
            switch(this.cellstyle) {
                case 'outputtext':
                    $(this.contentNode()).append(Notebook.dom._textoutput());
                    this.textareaNode().readOnly = true;
                    this.textareaNode().cellid = this.id;
                    break;
                case 'outputimage':
                    $(this.contentNode()).append(Notebook.dom._imageoutput());
                    break;   
            }
            break;
    }
};

Notebook.Cell.prototype.resetStyle = function(newstyle) {
    var enabled = this.spawnerNode().enabled;
    this.setStyle(newstyle);
    this.spawnerNode().enabled = enabled;
};

////////////////////////////////////////////////////
////////////////////////////////////////////////////
//  Convinience Methods / Intra-cell-node aliases //
////////////////////////////////////////////////////
////////////////////////////////////////////////////

///////////////////////////////////////////
// -- General Cell Methods --            //
// -- Cell DOM relation/navigation       // 
///////////////////////////////////////////


/** parentCell - either a cell or the notebook */
//! Use parentBranch !!
Notebook.Cell.prototype.parentCell = function() {
    if (this.parentNode.id == 'main') {
        return this.parentNode;
    }
    // the first parentNode gets us into the contentNode of the
    // parentBranch, hence the second parentNode call
    return this.parentNode.parentNode;
};

/** getParentBranch - the group this cell resides is */
// !! maybe use parentCell, which name is better? cell..
Notebook.Cell.prototype.getParentBranch = function() {
    if (this.parentNode.id == 'main') {
        return this.parentNode;
    }
    // the first parentNode gets us into the contentNode of the
    return this.parentNode.parentNode;
};

Notebook.Cell.prototype.childCells = function(ids) {
    var getCellIds = function(node) {
        try {
            var nodeType = node.type();
        }
        catch (ex) {
            var nodeType = false;
        }
        if (nodeType != 'creator') {
            ids.push(node.id);
        }
        if (nodeType == 'group') {
            ids = node.childCells(ids);
        }
        if (node.nextSibling) {
            getCellIds(node.nextSibling);
        }
    };
    nodeWalk(this.contentNode().firstChild, getCellIds);
    return ids;
};

Notebook.Cell.prototype.getCellLevel = function() {
    //group cells level generally determined by its head cell
    if (this.celltype == 'group') {
        return this.contentNode().firstChild.getCellLevel();
    } else {
        return this.cellevel;
    }
};

// previous and next Cell should be like previous and next Sibling:
// that is, they should be wrt the node they exist in

/** previousCell -- a cell's version of previousSibbling */
Notebook.Cell.prototype.previousCell = function() {
    var prev = this.previousSibling;
    if (prev) {
        if (prev.cell) {
            return prev;
        } else {
            return null;
        }
    }
    return prev;
};

Notebook.Cell.prototype.prevVisibleCell = function() {
    var prev = $(this).prev(':visible')[0];//xxx
    if (prev) {
        if (prev.cell) {
            return prev;
        } else {
            return null;
        }
    }
    prev = null;
    return prev;
};

/** nextCell -- a cell's version of nextSibling */
Notebook.Cell.prototype.nextCell = function() {
    var next = this.nextSibling;
    if (next) {
        if (next.cell) {
            return next;
        } else {
            return null;
        }
    }
    next = null;
    return next; //should be null
};

Notebook.Cell.prototype.nextVisibleCell = function() {
    var next = $(this).next(':visible')[0];//xxx
    if (next) {
        if (next.cell) {
            return next;
        } else {
            return null;
        }
    }
    return next; //should be null
};

Notebook.Cell.prototype.appendChildCells = function(node) {
    $(this.contentNode()).append(node);
};

Notebook.Cell.prototype.prependChildCells = function(node) {
    $(this.contentNode()).prepend(node);
};

Notebook.Cell.prototype.isHead = function() {
    //Hackiness...special cases for notebook branch
    //don't want cell at top of notebook to be heads of the notebook
    //the notebook doesn't have a head?
    //or the notebook could be force to have a head...is that general?
    var branchheadid = this.getParentBranch().contentNode().firstChild.id;
    var notebookbranchQ = this.getParentBranch().id;
    if (branchheadid == this.id && notebookbranchQ != 'main') {
        //this is head of a branch
        return true;
    }
    return false;
};

//changed from isBranchGroup
Notebook.Cell.prototype.isGroup = function() {
    if (this.celltype == 'group') {
        return true;
    }
    return false;
};



/** setFocus, depending on celltype (including creators) */
// !! REDO !!
Notebook.Cell.prototype.setFocus = function() {
    switch(this.celltype) {
        case 'input':
            this.textareaNode().focus();
            break;
        case 'group':
            this.contentNode().firstChild.setFocus();
            break;
        case 'output':
            this.textareaNode().focus();
            break;
        default:
            return;
    }
    $('#auxdisplay').html(this.id);
};

/** focusLastInGroup - used when entering a group from below */
Notebook.Cell.prototype.focusLastInGroup = function() {
    this.contentNode().lastChild.focusFromBelow();
    $(this.contentNode()).children(':visible:last')[0].focusFromBelow();
};

/** beBlured - for cell creators (not anymore) */
// need to re-think for cells
Notebook.Cell.prototype.beBlured = function() {
    this.textareaNode().blur();
    return;
};

/** focusPreviousCell - a cell's focus previousSibling */
Notebook.Cell.prototype.focusPreviousCell = function() {
    //var prev = this.previousCell();
    var prev = this.prevVisibleCell();
    if (prev) {
        prev.focusFromBelow();
    } else {
        this.parentCell().focusUp();
    }
};

Notebook.Cell.prototype.focusUp = function() {
    if (this.inputUpTest()) {
        this.focusPreviousCell();
    }
};

Notebook.Cell.prototype.focusFromBelow = function() {
    if (this.isGroup()) {
        this.focusLastInGroup();
    } else if (this.spawnerNode().enabled) {
        this.focusSpawner();
        return;
    } else {
        //this.focusContent();
        this.setFocus();
        return;
    }
};


/** focusNextCell - a cell's focus nextSibling */
Notebook.Cell.prototype.focusNextCell = function() {
    //var next = this.nextCell();
    var next = this.nextVisibleCell();
    if (next) {
        this.beBlured();
        next.focusFromAbove();
    } else if (this.parentCell().cell) {
        this.parentCell().focusNextCell();
    } else {
        this.focusFromBelow();
    }
};

Notebook.Cell.prototype.focusDown = function() {
    if (this.inputDownTest()) {
        if (this.spawnerNode().enabled) {
            this.beBlured();
            this.spawnerNode().setFocus();
            return;
        } else {
            this.focusNextCell();
        }
    }
};

Notebook.Cell.prototype.focusFromAbove = function() {
    //this.focusContent();
    this.setFocus();
};



/** inputUpTest - see if the cursor of input is fully home */
Notebook.Cell.prototype.inputUpTest = function() {
    if (this.celltype == 'input') {
        var s = this.getSelection();
        var before = this.content().substr(0,s.start);
        var i = before.indexOf('\n');
        if (i == -1 || before == '') {
            //this.focusPreviousSibling();
            return true; // move to previous cell
        } else {
            return false; // don't move cells
        }
    } else {
        return true; //move
    }
};

Notebook.Cell.prototype.inputDownTest = function() {
    if (this.celltype == 'input') {
        var s = this.getSelection();
        var after = this.content().substr(s.end);
        var i = after.indexOf('\n');
        if (i == -1 || after == '') {
            //this.focusNextSibling();
            return true; // move to next cell
        } else {
            return false; // don't move cells
        }
    } else {
        return true; //move
    }
};


Notebook.Cell.prototype.contentChanged = function() {
    this.clearNumberLabel();
    this.saved = false;
};

////////////////////////////////
// -- Group Cell functions -- //
////////////////////////////////

Notebook.Cell.prototype.closeGroup = function() {
    if (this.celltype == 'group' && this.open) {
        $(this.contentNode().firstChild).nextAll().hide()
        this.open = false;
    }
};

Notebook.Cell.prototype.openGroup = function() {
    if (this.celltype == 'group' && !this.open) {
        $(this.contentNode().firstChild).nextAll().show()
        this.open = true;
    }
};

Notebook.Cell.prototype.toggleOpen = function() {
    if (this.celltype == 'group') {
        this.open ? this.closeGroup():this.openGroup();
    }
};

////////////////////////////////////
// -- Main Cell Parts --      
/////////////////////////////////

Notebook.Cell.prototype.labelNode = function() {
    return $(this).children('.label')[0];
};

Notebook.Cell.prototype.contentNode = function() {
    return $(this).children('.contents')[0];
};

Notebook.Cell.prototype.stemNode = function() {
    //xxx
    return this.childNodes[2];
};

Notebook.Cell.prototype.spawnerNode = function() {
    return $(this).children('.spawner')[0];
};

//////////////////////////////////
// -- Cell Label Node (left) -- //
//////////////////////////////////

Notebook.Cell.prototype.tabLabel = function() {
    return this.labelNode().childNodes[1];
};

Notebook.Cell.prototype.numberLabel = function(count) {
    this.labelNode().childNodes[0].innerHTML = count;
};

Notebook.Cell.prototype.clearNumberLabel = function() {
    this.numberLabel('');
};

//////////////////////////////////////
// -- Cell Content Node (center) -- //
//////////////////////////////////////

/** content - Sets new content OR returns content, if it exists */
// the text should always be inside the firstChild of a non-groupcell
// content node.
Notebook.Cell.prototype.content = function(newcontent) {
    if (!newcontent) {
        if (this.celltype == 'input') {
            return this.contentNode().childNodes[0].value;
        } 
        if (this.celltype == 'output') {
            switch (this.cellstyle) {
                case 'outputtext':
                    return this.contentNode().childNodes[0].value;
                case 'outputimage':
                    return $(this.contentNode()).find('img.outputimage')[0].name;
            }
        }
        if (this.celltype == 'group') {
            return this.contentNode().childNodes;
        }
    } else {
        if (this.celltype == 'input') {
            this.contentNode().childNodes[0].value = newcontent;
            this.oldcontent = newcontent;
        } 
        if (this.celltype == 'output') {
            switch (this.cellstyle) {
                case 'outputtext':
                    var contentsplit = newcontent.split('\n');
                    var spancontent = $.map(contentsplit, function(n, i) {
                            return $.SPAN(null, n);
                            });
                    this.contentNode().childNodes[0].value = newcontent;
                    //$(this.contentNode().childNodes[0]).append(spancontent);
                    break;
                case 'outputimage':
                    //this.imagesrc = newcontent; //does this need to be remembered?
                                        //it should be on the server
                    //image wrapped with an anchor element
                    //look for img node by using getFirstElByTagAndClass
                    //this.contentNode().childNodes[0].src = newcontent;
                    //$(this.contentNode().firstChild).ready(console.info(this.contentNode().firstChild.firstChild.height));
                    // parameterize image path
                    $(this.contentNode()).find('img.outputimage')[0].src = '/data/'+newcontent;
                    $(this.contentNode()).find('img.outputimage')[0].name = newcontent;
                    break;
            }
        }
        if (this.celltype == 'iogroup') {
            $(this.contentNode()).children().replaceWith(newcontent);
        }
        if (this.celltype == 'group') {
            $(this.contentNode()).children().replaceWith(newcontent);
        }
    }
};

Notebook.Cell.prototype.focusContent = function() {
    //decide what to focus depending on what style cell
    this.contentNode().firstChild.focus();
};

/** textareaNode */
// If there is a textarea, this returns the node
Notebook.Cell.prototype.textareaNode = function() {
    // put in condition on type (has to be input)
    return this.contentNode().childNodes[0];
};

/** adjustTextarea */
// if there is a textarea, set the number of rows
// triggered by keyup for editable cells
// also used for outputtext
Notebook.Cell.prototype.adjustTextarea = function() {
    if (this.celltype == 'input') { 
        var rows = this.content().split('\n').length;
        this.textareaNode().rows = rows;
        var h = $(this.textareaNode()).height();
        //h += getElementDimensions(this.spawnerNode()).h;
        //$(this).height(h);
        return true;
    } else if (this.cellstyle == 'outputtext') {
        var rows = this.content().split('\n').length;
        this.textareaNode().rows = rows;
        var tawidth = $(this.textareaNode()).width();
        var breaks = this.content().split('\n');
        var spaces = this.content().split(' ');
        var longestbreak = breaks.sort(function(a,b) {
                return a.length - b.length;
                }).pop().length;
        var fontsize = 13; //generalize
        /*
        var wid = $(this.textareaNode()).width();
        var cols = wid/7;
        var len = this.content().length;
        var nspaces = this.content().split(' ').length;
        var nnewlines = this.content().split('\n').length;
        if (len > cols) {
            if (len/nspaces > cols) {
                //make more spaces
            } else if (len/nnewlines > cols) {
                //fix
            }
        }
        var ans = Math.ceil(len/cols);
        this.textareaNode().rows = ans;
        var h = $(this.textareaNode()).height();
        $(this).height(h);
        */
        return;
    } else if (this.cellstyle == 'outputimage') {
        var h = $(this.contentNode()).height();
        //h += getElementDimensions(this.spawnerNode()).h;
        $(this).height(h);
        return;
    }
};

Notebook.Cell.prototype.checkForChange = function() {
    var oc = this.oldcontent;
    var cc = this.content();
    if (oc != cc) {
        this.contentChanged();
        this.oldcontent = cc;
        this.saved = false;
    }

};

Notebook.Cell.prototype.pageTextContent = function() {
    //make text fit into cell
    //grab text, split on page tokens
    //get cur width in cols?
    //break up string
};

// for input text, get cursor selection Star/End
Notebook.Cell.prototype.getSelection = function() {
    //Get cursor position using Selection 
    //var selection = new Selection(this.textareaNode());
    //var s = selection.create();
    var s = $(this.textareaNode()).getSelection();
    return s;
};

Notebook.Cell.prototype.contentInsert = function(newcontent, cursor) {
    // Insert stuff where the cursor is
    //$(this.textareaNode()).replaceSelection(newcontent);
    var newcursor = newcontent.length + cursor;
    var curcontent = this.content();
    var finalcontent = curcontent.substr(0,cursor) + newcontent + curcontent.substr(cursor);
    this.content(finalcontent);
    if(this.contentNode().firstChild.setSelectionRange) {
        this.contentNode().firstChild.setSelectionRange(newcursor,newcursor);
    } else if (this.contentNode().firstChild.createTextRange) {
        var range = this.contentNode().firstChild.createTextRange();
        range.moveEnd('character', newcursor - finalcontent.length);
        range.collapse(false);
        range.select();
    }
};

/////////////////////////////////////
// -- Cell Bracket Node (right) -- //
//   rename bracket to stemNode ... maybe?
/////////////////////////////////////

// this node has two wrappers...
Notebook.Cell.prototype.bracketNode = function() {
    return $(this).children('.bracketng')[0];
};

Notebook.Cell.prototype.focusBracket = function() {
    this.bracketNode().focus();
};

Notebook.Cell.prototype.highlightBracket = function() {
    $(this.bracketNode()).css('background-color', 'yellow');
};

Notebook.Cell.prototype.unhighlightBracket = function() {
    $(this.bracketNode()).css('background-color', 'white');
};

Notebook.Cell.prototype.setBracketSelected = function() {
    $(this.bracketNode()).css('outline', '1px solid black');
    this.bracketNode().focus();
};

Notebook.Cell.prototype.setBracketUnSelected = function() {
    $(this.bracketNode()).css('outline', '1px solid white');
};

////////////////////////////////////////
// -- Cell Spawner Node (Bottom) -- ///
//////////////////////////////////////


Notebook.Cell.prototype.focusSpawner = function() {
    this.spawnerNode().setFocus();
};

Notebook.Cell.prototype.blurSpawner = function() {
    this.spawnerNode().beBlured();
};



////////////////////////////////////////////////////////
////////////////////////////////////////////////////////
// Action Methods -- Server calls / Dynamic style ... //
////////////////////////////////////////////////////////
////////////////////////////////////////////////////////

///////////////////////////
// -- Cell Evaluation -- //
///////////////////////////

Notebook.Cell.prototype.evaluate = function() {
    if (this.evaluatable) {
        this.evaluating = 2;
        this.highlightBracket()
        //!! reference to ASYNC
        Notebook.Async.evalCell(this.id,this.content());
    }
};

//!!!! REDO !!!
Notebook.Cell.prototype.evalResult = function() {
    this.evaluating = 0; //not evaluating
    this.unhighlightBracket();
};

///////////////////////////
// --  Cell Deletion  -- //
///////////////////////////

//!! Take this functionality OUT -- MOVE to TreeBranch
Notebook.Cell.prototype.deleteCells = function() {
    //put in check for child cells
    var ids = [this.id];
    ids = this.childCells(ids);
    var d = notebook.deleteCells(this.id, ids);
    return d;

};

Notebook.Cell.prototype.deleteCallback = function(meid, result) {
    notebook.deleteCellNode($('#'+meid));
    notebook.save();
};

Notebook.Cell.prototype.deleteErr = function(result) {
};

//////////////////////////////
// -- Tab Key Completion -- //
//////////////////////////////

/** tab - */
Notebook.Cell.prototype.tab = function() {
    var mode = this.tabCompletion();
    if (mode) {
        return mode;
    }
    //('tab: four spaces');
    this.contentInsert('    ',this.selectionStart);
    this.completing = false;
    //Notebook.Completer.completionExit();
    this.setCompletingLabel('off');
    return 'normal';
};

Notebook.Cell.prototype.tabCompletion = function() {
    //Get cursor position using Selection 
    //var selection = new Selection(this.contentNode().childNodes[0]);
    //var s = selection.create();
    var s = this.getSelection();
    this.selectionStart = s.start;
    
    var tomatch = this.content().substr(0,this.selectionStart);

    var mode = Notebook.Completer.test(this.id, tomatch);
    return mode;
};


Notebook.Cell.prototype.completionExit = function() {
    if (this.completing) {
        this.completing = false;
        Notebook.Completer.completionExit();
    }
};

Notebook.Cell.prototype.setCompletingLabel = function(mode) {
    switch(mode) {
        case 'tab':
            $(this.tabLabel()).css('background-color','blue');
            break;
        case 'name':
            $(this.tabLabel()).css('background-color','yellow');
            break;
        case 'attribute':
            $(this.tabLabel()).css('background-color','orange');
            break;
        case 'off':
            $(this.tabLabel()).css('background-color','white');
            break;
    }
};


