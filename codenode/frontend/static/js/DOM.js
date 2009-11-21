/*
######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

 Notebook.DOM - templates 
 
 */


Notebook.DOM = {};



Notebook.DOM.topspawner = function() {
    var node = $.DIV({'class':'spawner', 
                'id':'topspawner'
                }, 
                $.TEXTAREA({'class':'spawninput'}));
    node.lastChild.readOnly = true;
    return node;
};

Notebook.DOM.mainDIV = function() {
    var node = $.DIV({'id':'main', 'class':'main'});
    return node;
};

Notebook.DOM.botPad = function() {
    var node = $.DIV({'id':'botpad',
                'class':'botpad'
                });
    return node;
};

///////////////////////////
// Cell templates
//////////////////////////

Notebook.DOM.newCell = function() {
    var self = Notebook.DOM;
    var node = $.DIV({
        'class':'cell'
        }, 
        self._label(),
        self._content(),
        //this._treebranch(),
        self._bracket(),
        self._spawner());
    return node;
};

Notebook.DOM.newOutCell = function() {
    var self = Notebook.DOM;
    var node = $.DIV({
        'class':'cell'
        }, 
        self._label(),
        self._content(),
        //this._treebranch(),
        self._bracket_output(),
        self._spawner());
    return node;
};

Notebook.DOM.groupCell = function() {
    var self = Notebook.DOM;
    var node = $.DIV({
        'class':'cell'
        }, 
        self._content(),
        self._bracket_group(),
        self._spawner());
    return node;
};

Notebook.DOM._label = function() {
    var node = $.SPAN({
        'class':'label'},
            $.DIV({'class':'number'}),
            $.DIV({'class':'tablight'}));
    return node;
};

Notebook.DOM._content = function() {
    var node = $.SPAN({
        'class':'contents'
        });
    return node;
};

Notebook.DOM._textarea = function() {
    var node = $.TEXTAREA({
            'class':'input',
            'cols':'1',
            'rows':'1'
            });
    return node;
};

Notebook.DOM._textoutput = function() {
    var node = $.TEXTAREA({
            'class':'outputtext',
            'cols':'1',
            'rows':'1'
            });
    /*
    var node = $.SPAN({
            'class':'outputtext'
            });*/
    return node;
};

Notebook.DOM._imageoutput = function() {
    return $.A({'class':'outputimage','href':'#'}, $.IMG({'class':'outputimage'}));
};


Notebook.DOM._treebranch = function() {
        var node = $.DIV({
            'class':'ctreebranch'
            });
        return node;
};

Notebook.DOM._bracket = function() {
    var node = $.SPAN({'class':'bracketng'},
                    $.IMG({'class':'bracketmaskimg', 'src':'/static/img/bracketslant.png'}));
    /*var node = $.DIV({'class':'bracketng'},
                    $.IMG({'class':'bracketmaskimg', 'src':'/static/img/bracketslant.png'}),
                    $.DIV({'class':'fillup'}));*/
    return node;
};

Notebook.DOM._bracket_output = function() {
     var node = $.SPAN({'class':'bracketng'},
                    $.IMG({'class':'bracketmaskimg', 'src':'/static/img/bracketoutput.png'}));
     return node;
};

Notebook.DOM._bracket_group = function() {
     var node = $.SPAN({'class':'bracketng'});
     return node;
};

Notebook.DOM._spawner = function() {
    var node = $.DIV({ 'class':'spawner'},
        $.TEXTAREA({
            'class':'spawninput', 
            'title':'Click, then start typing to create a new Cell.'     
        }));
    node.lastChild.readOnly = true;
    return node;
};

/*
Notebook.DOM.spawnPrompt = function() {
    var node = DIV({
        'id':'spawnprompt',
        'class':'spawnprompt'
        },
        DIV({'class':'promptsymbol'},'Type to start a new cell'),
        TEXTAREA({'cols':'10','rows':'1'}),
        DIV({'class':'spawnmenu'}));
    return node;
};
*/
Notebook.DOM.contextMenu = function() {
    return $.DIV({'class':'contextMenu', 'id':'bracketMenu'},
            $.UL(null,
                $.LI({'id':'totitle'}, 'Title'),
                $.LI({'id':'tosubtitle'}, 'Subtitle'),
                $.LI({'id':'tosection'}, 'Section'),
                $.LI({'id':'tosubsection'}, 'Subsection'),
                $.LI({'id':'totext'}, 'Text'),
                $.LI({'id':'toinput'}, 'Input'),
                $.LI({'id':'tooutput'}, 'Output')
              ));
};

Notebook.dom = Notebook.DOM;

