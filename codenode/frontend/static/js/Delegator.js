/*
######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

* Delegator - event delegater. Configurable key events by action and group
*             functionality
*/

// Not sure if this needs to be registered with the delegator
$(window).bind('beforeunload', function() {
    if (Notebook.Save.hasUnsavedChanges()) {
        return 'You have unsaved changes that will be lost.';
    }
});

// supress the backspace key for the window
$(window).keydown(function(e) {
    if (e.keyCode === 8)
    {
        return false;
    }
});



Notebook.Delegator = function(nodeid) {
    this.mode = 'normal';
    this.listener = nodeid;
    this.groups = {};
    this.targets = {};
};


Notebook.Delegator.prototype = {
    /* group_selector : string(tag.class) 
     * targets list of targets : string tag.class
     */
    init: function() {
        $(this.listener).bind('keydown', this, this.delegate);
        $(this.listener).bind('keypress', this, this.delegate);
        $(this.listener).bind('keyup', this, this.delegate);
        $(this.listener).bind('click', this, this.delegate);
        $(this.listener).bind('dblclick', this, this.delegate);
        $(this.listener).bind('mousedown', this, this.delegate);
        //$(this.listener).bind('contextmenu', this, this.delegate);
        //Notebook.osystem = $.browser.system();
    },

    registerAllActions: function(allactions) {
        var self = this; //Ahhhh...bind this mofo
        $.each(allactions, function(group_selector, targets) {
            self.registerGroup(group_selector);
            $.each(targets, function(target_selector, target_actions) {
                self.registerTarget(group_selector, target_selector);
                self.registerTargetAction(target_selector, target_actions);
            })
        });
    },

    registerGroup: function(group_selector) {
        //put check for existing group
        this.groups[group_selector] = {};
    },

    registerTarget: function(group_selector, target_selector) {
        //put check for existing target
        this.targets[target_selector] = group_selector;
        this.groups[group_selector][target_selector] = [];
    },

    /* target_selector : string tag.class (initially set in registerGroup
     * action : object
     */
    registerTargetAction: function(target_selector, actions) {
        var self = this;
        if (typeof(action) == 'function') {
            var actions = [actions];
        }
        var target_group = self.targets[target_selector];
        $.each(actions, function(i, action) {
            self.groups[target_group][target_selector].push(action);
        });
    },

    delegate: function(e) {
        var self = e.data;
        var target_selector = e.target.tagName.toLowerCase() + '.' + e.target.className;
        var target_group = self.targets[target_selector];

        if (target_group) {
            var group_element = $(e.target).parents(target_group);
            
            // console.log('delegating ' + target_selector + ' event to ' + 
            //     group_element + ' specified by ' + target_group
            // ) 
            
            e.groupNode = group_element[0];
            e.mode = self.mode;
            var acts = self.groups[target_group][target_selector];
            var returnstop;
            for (var a in acts) {
                if (acts[a].test(e)) {
                    returnstop = acts[a].handler(e);
                    //self.mode = e.mode;
                }
            }
            return;
        } 
        return;
    }
};

Notebook.Action = function(name) {
    //default properties
    this.name = name;
    this.mode = 'normal';
    this.keyCodes = [[0,200]];
    this.button = 0;//?
    this.shift = false;
    this.ctrl = false;
    this.alt = false;
    this.meta = false;
    this.preventDefault = false;
    this.stopPropagation = false;
};

Notebook.Action.prototype = {
    test: function(e) {
        //match this action?
        if (this.testMode(e.mode)) {
            if (this.testType(e.type)) {
                if (this.testModKeys(e.shiftKey, e.ctrlKey, e.altKey)) {
                    if (this.testKeyCode(e.keyCode)) {
                        //cancel default?
                        if (this.preventDefault) {
                            //e.stopPropagation();
                            //e.preventCapture();
                            e.preventDefault();
                        }
                        if (this.stopPropagation) {
                            e.stopPropagation();
                        }
                        return true;
                    }
                }
            }
        }
        return false;
    },

    testMode: function(mode) {
        if (this.mode == mode || this.mode == 'all') {
            return true;
        }
    },

    testType: function(type) {
        //maybe this could be pre-organized in the target registration
        if (type == this.type) {
            return true;
        }
        return false;
    },

    testKeyCode: function(keyCode) {
        for (var k in this.keyCodes) {
            var curCodeType = typeof(this.keyCodes[k])
            var curCode = this.keyCodes[k]
            switch(curCodeType) {
                case 'number':
                     if (curCode == keyCode) {
                         return true;
                     }
                     break;
                case 'object':
                     if (keyCode >= curCode[0] && keyCode <= curCode[1]) {
                         return true;
                     }
                     break;
                default:
                     break;
            }
        }
        return false;
    },

    testModKeys: function(shift, ctrl, alt) {
        if (this.shift == 'maybe') {
            var shift = 'maybe';
        }
        if (this.ctrl == 'maybe') {
            var ctrl = 'maybe';
        }
        if (this.alt == 'maybe') {
            var alt = 'maybe';
        }
        if (shift == this.shift && ctrl == this.ctrl && alt == this.alt) {
            return true;
        } else {
            return false;
        }
    }
};

Notebook.ClickAction = function(name) {
    //default properties
    this.name = name;
    this.mode = 'normal';
    this.type = 'click';
    this.button = 0;//?
    this.shift = false;
    this.ctrl = false;
    this.alt = false;
    this.meta = false;
    this.preventDefault = false;
    this.stopPropagation = false;
};

Notebook.ClickAction.prototype = {
    test: function(e) {
        //match this action?
        if (this.testMode(e.mode)) {
            if (this.testType(e.type)) {
                if (this.testModKeys(e.shiftKey, e.ctrlKey, e.altKey)) {
                    if (this.testButton(e.button)) {
                        //cancel default?
                        if (this.preventDefault) {
                            //e.stopPropagation();
                            //e.preventCapture();
                            e.preventDefault();
                        }
                        if (this.stopPropagation) {
                            e.stopPropagation();
                        }
                        return true;
                    }
                }
            }
        }
        return false;
    },

    testMode: function(mode) {
        if (this.mode == mode || this.mode == 'all') {
            return true;
        }
    },

    testType: function(type) {
        //maybe this could be pre-organized in the target registration
        if (type == this.type) {
            return true;
        }
        return false;
    },

    testButton: function(button) {
        if (this.button == button) {
            return true;
        }
        return false;
    },

    testModKeys: function(shift, ctrl, alt) {
        if (this.shift == 'maybe') {
            var shift = 'maybe';
        }
        if (this.ctrl == 'maybe') {
            var ctrl = 'maybe';
        }
        if (this.alt == 'maybe') {
            var alt = 'maybe';
        }
        if (shift == this.shift && ctrl == this.ctrl && alt == this.alt) {
            return true;
        } else {
            return false;
        }
    }
};

///////////////////////////////////////
///
// Action Definitions
////////////////////////////////

//////////////////////////
// Mouse Actions
//////////////////////
bracketClick = new Notebook.ClickAction('braclick');
bracketClick.type = 'click';
bracketClick.handler = function(e) {
    console.log('bracketSelector.select ' + e.groupNode);
    Notebook.bracketSelector.select(e.groupNode.id);
};

bracketSelectMore = new Notebook.ClickAction('bmore');
bracketSelectMore.ctrl = true;
bracketSelectMore.handler = function(e) {
    Notebook.bracketSelector.selectMore(e.groupNode.id);
};

bracketDblClick = new Notebook.ClickAction('brackdblclk');
bracketDblClick.type = 'dblclick';
bracketDblClick.handler = function(e) {
    e.groupNode.toggleOpen();
};

bracketRightDown = new Notebook.ClickAction('rightDown');
bracketRightDown.type = 'mousedown';
bracketRightDown.button = 2;
bracketRightDown.ctrl = 'maybe';
bracketRightDown.meta = 'maybe';
bracketRightDown.handler = function(e) {
    var selectedQ = Notebook.bracketSelector.isSelected(e.groupNode.id);
    if (!selectedQ) {
        Notebook.bracketSelector.select(e.groupNode.id);
    }
};

mainNullClick = new Notebook.ClickAction('nullclick');
mainNullClick.type = 'mousedown';
mainNullClick.handler = function(e) {
    Notebook.bracketSelector.deselectAll();
    e.groupNode.setFocus();
};

cellContextMenu = new Notebook.ClickAction('context');
cellContextMenu.type = "contextmenu";
cellContextMenu.button = 2;
cellContextMenu.stopPropagation = true;
cellContextMenu.handler = function(e) {
};

bottompadClick = new Notebook.ClickAction('botpad');
bottompadClick.type = 'click';
bottompadClick.handler = function(e) {
    e.groupNode.focusFromBelow();
};


/////////////////////////
// Key Actions
///////////////////////


spawnKeydownAction = new Notebook.Action('spawnkeydown');
spawnKeydownAction.keyCodes = [13, 32, [48, 57], [185, 193], [219, 222], [65, 90]];
spawnKeydownAction.type = 'keydown';
spawnKeydownAction.shift = 'maybe';
spawnKeydownAction.ctrl = 'maybe';
spawnKeydownAction.handler = function(e) {
    var node = Notebook.TreeBranch.spawnInputCellNode();
    if (e.groupNode.id == 'topspawner') {
        Notebook.TreeBranch.putCellNodeAtTop(node);
    } else {
        Notebook.TreeBranch.putCellNodeAfter(e.groupNode.parentNode, node);
    }
    node.setFocus();
};

evalAction = new Notebook.Action('eval');
evalAction.keyCodes = [13];
evalAction.shift = true;
evalAction.type = 'keydown';
evalAction.preventDefault = true;
evalAction.handler = function(e) {
   e.groupNode.evaluate();
   e.groupNode.focusDown();
}; 

stopevalAction = new Notebook.Action('eval');
stopevalAction.keyCodes = [13];
stopevalAction.shift = true;
stopevalAction.type = 'keypress';
stopevalAction.preventDefault = true;
stopevalAction.handler = function(e) {
}; 

cellTabAction = new Notebook.Action('celltab');
cellTabAction.keyCodes = [9];
cellTabAction.type = 'keydown';
//cellTabAction.type = 'keyup';
cellTabAction.preventDefault = true;
cellTabAction.handler = function(e) {
    var gid = e.groupNode.id;
    //if (!$.browser.mac() && !$.browser.opera()) {
    if (browser.OS == 'Mac' && !$.browser.opera) {
        e.mode = e.groupNode.tab();
    } else if ($.browser.mozilla || $.browser.msie) {
        e.mode = e.groupNode.tab();
    } else if ($.browser.mozilla) {
        e.mode = e.groupNode.tab();
    };
};

tabcompleteExitAction = new Notebook.Action('tabexit');
tabcompleteExitAction.keyCodes = [27, 32, 8] 
tabcompleteExitAction.type = 'keydown';
tabcompleteExitAction.mode = 'completing';
tabcompleteExitAction.preventDefault = false;
tabcompleteExitAction.handler = function(e) {
    e.groupNode.completionExit();
    e.mode = 'normal';
};

cellTabFilter = new Notebook.Action('tabfilter');
cellTabFilter.keyCodes = [9];
cellTabFilter.type = 'keypress';
cellTabFilter.mode = 'all';
cellTabFilter.preventDefault = true;
cellTabFilter.handler = function(e) {
    //e.groupNode.parentNode.setFocus();
};

hackcellTabFilter = new Notebook.Action('tabfilter');
hackcellTabFilter.keyCodes = [9];
hackcellTabFilter.type = 'keyup';
hackcellTabFilter.mode = 'all';
hackcellTabFilter.preventDefault = true;
hackcellTabFilter.handler = function(e) {
    //if ($.browser.mac() || $.browser.opera()) {
    if (browser.OS == 'Mac' || $.browser.opera) {
        e.groupNode.parentNode.setFocus();
        e.groupNode.parentNode.tab();
    };
};

refineTabcompletion = new Notebook.Action('refinetab');
refineTabcompletion.keyCodes = [8, [10, 26], [28, 31], [35, 200]]; //anykey?
refineTabcompletion.type = 'keyup';
refineTabcompletion.mode = 'completing';
refineTabcompletion.preventDefault = true;
refineTabcompletion.handler = function(e) {
    e.mode = e.groupNode.tabCompletion();
};

pageTabcompletions = new Notebook.Action('pagetabs');
pageTabcompletions.keyCodes = [33, 34];
pageTabcompletions.type = 'keydown';
pageTabcompletions.mode = 'completing';
pageTabcompletions.preventDefault = true;
pageTabcompletions.handler = function(e) {
    Notebook.Completer.pageCompletions(e.keyCode);
};

adjustCellAction = new Notebook.Action('adjustcell');
adjustCellAction.keyCodes = [8, [10,200]];
adjustCellAction.shift = 'maybe';
adjustCellAction.ctrl = 'maybe';
adjustCellAction.type = 'keyup';
adjustCellAction.handler = function(e) {
    e.groupNode.adjustTextarea();
};

cellContentChange = new Notebook.Action('change');
cellContentChange.keyCodes = [8, 13, 32, [48, 57], [185, 193], [65, 90], [97, 122]];
cellContentChange.shift = 'maybe';
cellContentChange.ctrl = 'maybe';
cellContentChange.type = 'keydown';
cellContentChange.handler = function(e) {
    e.groupNode.saved = false;
};


cellUpArrowAction = new Notebook.Action('cellUpArrow');
cellUpArrowAction.keyCodes = [38, 63232];
cellUpArrowAction.type = 'keypress';
if ($.browser.msie) {
    cellUpArrowAction.type = 'keydown';
};
cellUpArrowAction.preventDefault = false;
cellUpArrowAction.handler = function(e) {
    e.groupNode.focusUp();
};

cellDownArrowAction = new Notebook.Action('cellDownArrow');
cellDownArrowAction.keyCodes = [40, 63233];
cellDownArrowAction.type = 'keypress';
if ($.browser.msie) {
    cellDownArrowAction.type = 'keydown';
}
cellDownArrowAction.preventDefault = false;
cellDownArrowAction.handler = function(e) {
    e.groupNode.focusDown();
};

spawnerUpArrowAction = new Notebook.Action('spawnerUpArrow');
spawnerUpArrowAction.keyCodes = [38, 63232];
spawnerUpArrowAction.type = 'keypress';
if ($.browser.msie) {
    spawnerUpArrowAction.type = 'keydown';
};
spawnerUpArrowAction.preventDefault = true;
spawnerUpArrowAction.handler = function(e) {
    e.groupNode.focusUp();
};

spawnerDownArrowAction = new Notebook.Action('spawnerDownArrow');
spawnerDownArrowAction.keyCodes = [40, 63233];
spawnerDownArrowAction.type = 'keypress';
if ($.browser.msie) {
    spawnerDownArrowAction.type = 'keydown';
};
spawnerDownArrowAction.preventDefault = true;
spawnerDownArrowAction.handler = function(e) {
    e.groupNode.focusDown();
};

bracketKeyDelete = new Notebook.Action('backkeydel');
bracketKeyDelete.keyCodes = [46,8];
bracketKeyDelete.type = 'keydown';
bracketKeyDelete.handler = function(e) {
    Notebook.bracketSelector.deleteSelections();
};

emptycellDelete = new Notebook.Action('emptycellDelete');
emptycellDelete.keyCodes = [46, 8];
emptycellDelete.type = 'keydown';
emptycellDelete.preventDefault = false;
emptycellDelete.stopPropagation = true;
emptycellDelete.handler = function(e) {
    if (e.target.value=="")  {
        e.groupNode.focusUp()
        Notebook.TreeBranch.deleteCellNode(e.groupNode);
        e.preventDefault(); // needed to prevent browser going back    
    }
};


//$(document).ready(function() {
Notebook.__init__.Delegator = function() {
    $('#notebook')[0].className = 'notebook';//xxx hacky
    Notebook.delegator = new Notebook.Delegator('#notebook');
    Notebook.delegator.init();
    Notebook.delegator.registerAllActions({
        'div.spawner': {
            'textarea.spawninput': [spawnKeydownAction,
                                    hackcellTabFilter,
                                    spawnerDownArrowAction,
                                    spawnerUpArrowAction]
        },
        'div.cell.input': {
            'textarea.input': [adjustCellAction,
                                cellUpArrowAction,
                                cellDownArrowAction,
                                evalAction,
                                stopevalAction,
                                cellTabFilter,
                                cellTabAction,
                                pageTabcompletions,
                                tabcompleteExitAction,
                                refineTabcompletion,
                                mainNullClick,
                                cellContentChange,
                                bracketRightDown,
                                emptycellDelete],
        },
        'div.cell.group': {
            'span.bracketng': [bracketClick,
                            bracketSelectMore,
                            //cellContextMenu,
                            bracketRightDown,
                            bracketDblClick,
                            bracketKeyDelete],
        },
        'div.cell.output': {
            'textarea.outputtext': [cellUpArrowAction,
                                    cellDownArrowAction,
                                    mainNullClick],
            'a.outputimage': [cellUpArrowAction,
                                cellDownArrowAction],
            'img.outputimage': [mainNullClick]
        },
        'div.main': {
            'div.botpad': [bottompadClick]
        },
        'div.notebook': {
            'div.main': [mainNullClick]
        }
    });
    Notebook.auxdelegator = new Notebook.Delegator('#foot');
    Notebook.auxdelegator.init();
    Notebook.auxdelegator.registerAllActions({
        'div.foot': {
            'input.auxinput': [bracketKeyDelete]
        }
    });
    Notebook.bracketSelector = new Notebook.SelectionManager();
    $('div.contextMenu').hide();
    $('div.notebook').contextMenu('bracketMenu', {
        bindings: {
            'totitle': function(t) {
                Notebook.bracketSelector.modifySelectionStyle('title');
            },
            'tosubtitle': function(t) {
                Notebook.bracketSelector.modifySelectionStyle('subtitle');
            },
            'tosection': function(t) {
                Notebook.bracketSelector.modifySelectionStyle('section');
            },
            'tosubsection': function(t) {
                Notebook.bracketSelector.modifySelectionStyle('subsection');
            },
            'totext': function(t) {
                Notebook.bracketSelector.modifySelectionStyle('text');
            },
            'toinput': function(t) {
                Notebook.bracketSelector.modifySelectionStyle('input');
            },
            'delete': function(t) {
                Notebook.bracketSelector.deleteSelections();
            }
        },
        onContextMenu: function(e) {
            var t = e.target.tagName.toLowerCase() + '.' + e.target.className;
            if (t == 'span.bracketng' || t == 'textarea.input') {
                var groupNode = $(e.target).parents('div.cell');
                e.groupNode = groupNode;
                return true;
            }
            return false;  
        },
        onShowMenu: function(e, menu) {
            return menu;
        },
        itemStyle: {
            'fontFamily': 'arial, sans-serif',
            'fontSize': '12px',
            'padding': '3px 20px',
            'border': 'none'
        },
        itemHoverStyle: {
            'border': 'none'
        },
        menuStyle: {
            'width': '150px',
            'backgroundColor': '#f3f3f3'
        }
            
    });
    $('#titlecontainer').click(Util.startChangeTitle);
    $('#savebutton').click(function(e){Notebook.Save.save()});
    $('#saveclosebutton').click(function(e){Notebook.Save.saveAndClose()});
    $('#interruptbutton').click(function(e){Notebook.Async.signalKernel('interrupt')});
    $('#killkernelbutton').click(function(e){Notebook.Async.signalKernel('kill')});
};

