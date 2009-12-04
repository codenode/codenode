/*
######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################
 Notebook.js - Notebook.x is the main notebook namespace. 
               This initialize functions sets up some menus and 
               the top spawner onload.
*/



Notebook = {};
Notebook.__init__ = {};

Notebook.initialize = function() {
    browser = new BrowserDetect();
    browser.init();
    $.ifixpng('/static/img/pixel.gif');
    $.extend($('#notebook')[0], {
        setFocus: function() {
            this.firstChild.setFocus();
        },
        focusFromBelow: function() {
            this.lastChild.focusFromBelow();
        }
    });
    var topnode = Notebook.dom.topspawner();
    //b.update(topnode, {
    $.extend(topnode, {
        focusUp: function() {
            //;
        },
        setFocus: function() {
        this.firstChild.focus();
        },
        beBlured: function() {
            //setStyle(this, {'background-color':'white'});
        },
        focusDown: function() {
            if ($('#main > :first-child')[0]) {
                $('#main > :first-child')[0].focusFromAbove();
            }
        }
    });
    var mainnode = Notebook.dom.mainDIV();
    $.extend(mainnode, {
        getCellLevel: function() {
            return 0;
        },
        getParentBranch: function() {
            return $('#main')[0];
        },
        contentNode: function() {
            return $('#main')[0];
        },
        focusPreviousSibling: function() {
            this.previousSibling.setFocus();
        },
        focusUp: function() {
            this.focusPreviousSibling();
        },
        focusFromBelow: function() {
            this.lastChild.focusFromBelow();
        }
    });
    mainnode.cell = false;
    var botpad = Notebook.dom.botPad();
    $.extend(botpad, {
        focusFromAbove: function() {
            if (this.previousSibling) {
                this.previousSibling.focusFromBelow();
            } else {
                this.parentNode.focusUp();
            }
        },
        focusFromBelow: function() {
            if (this.previousSibling) {
                this.previousSibling.focusFromBelow();
            } else {
                this.parentNode.focusUp();
            }
        }
    });
    $(mainnode).append(botpad);
    $('#notebook').append(topnode, mainnode);
    //hack
    Notebook.cellid = 0;
    //topnode.setFocus();
    Util.nbTitle(document.title);
    $('#titlecontainer').bind('click', Util.startChangeTitle);//xxx eventHack
    var contextmenu = Notebook.DOM.contextMenu();
    $('#foot').after(contextmenu);
};

Notebook.SelectionManager = function() {
    this.selections = [];
};

Notebook.SelectionManager.prototype = {
    deselectAll: function() {
        for (var s in this.selections) {
            $('#'+this.selections[s])[0].setBracketUnSelected();//xxx HACK
        }
        this.selections = [];
    },
    select: function(id) {
        this.deselectAll();
        $('#'+id)[0].setBracketSelected();
        this.selections.push(id);
        $('#auxinput').focus();
    },
    selectMore: function(id) {
        $('#'+id)[0].setBracketSelected();
        this.selections.push(id);
    },
    modifySelectionStyle: function(newstyle) {
        if (this.selections.length == 1) {
            Notebook.TreeBranch.changeCell(newstyle, $('#'+this.selections[0])[0]);
            this.deselectAll();
        }
    },
    deleteSelections: function() {
        for (var s in this.selections) {
            var selection = this.selections[s]; 
            Notebook.TreeBranch.deleteCellNode($('#'+selection)[0]);
        }
        this.selections = [];
    },
    isSelected: function(id) {
        var index = $.inArray(id, this.selections);
        if (index == -1) {
            return false;
        }
        return true;
    }
        
};

//$(document).ready(Notebook.initialize);
Notebook.__init__.Notebook = function() {
    Notebook.initialize();
};

__notebook_component_inits__ = function() {
    Notebook.Indicator.loading(); //Bleh
    Notebook.__init__.Notebook();
    Notebook.__init__.Delegator();
    Notebook.__init__.Completer();
    Notebook.__init__.Async();
    Util.init();
};

$(document).ready(__notebook_component_inits__);
