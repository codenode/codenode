/*
######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

  Notebook.Completer.js

*/


//Notebook.Completer = function() {
//};

//Notebook.Completer.prototype = {
Notebook.Completer = {
    init: function() {
        var self = Notebook.Completer;
        self.completing = false;
        self.cellid = null;
        self.tocomplete = '';
    },

    test: function(cellid, tomatch) {
        var self = Notebook.Completer;
        var cell = $('#'+cellid)[0];
        //Completion tests 
        // there are 3 different completion tests. 
        // 1) matching variableNames/funcitonNames/objectNames 
        // 2) attribute to see an objects methods
        // 3) introspection on an object --
        //    _> show the documentation in a popup area temporarily
        //      (as opposed to evaluationg with a ?)
        //      This should work with foo?[TAB] or foo([TAB]
        //
        //

        var REname = /([a-zA-Z_][a-zA-Z_0-9]*)$/;
        var REattribute = /([a-zA-Z_][a-zA-Z_0-9]*[.]+[a-zA-Z_.0-9]*)$/;
        var REintrospect = /([a-zA-Z_][a-zA-Z_0-9]*)\?/;//inplace introspect

        var name_match = tomatch.match(REname);
        var attribute_match = tomatch.match(REattribute);
        var introspect_match = tomatch.match(REintrospect);

        if (attribute_match) {
            cell.completing = true;
            cell.setCompletingLabel('attribute');
            cell.tomatch = attribute_match[1];
            self.completeAttribute(cellid, attribute_match[1]);
            return 'completing';
        }
        if (name_match) {
            cell.completing = true;
            cell.setCompletingLabel('name');
            cell.tomatch = name_match[1];
            self.completeName(cellid, name_match[1]);
            return 'completing';
        }
        if (introspect_match) {
            //('tab: docstring_match ', docstring_match);

            return;
        }
        return false;
    },


/////////////////////////////////////////////////////////
// DOM element nodes for displaying completion results //
/////////////////////////////////////////////////////////

    completionTable: function() {
        return $.DIV({'id':'completions','class':'completions'});
    },

    completionItem: function(item) {
        return $.SPAN({'class':'completionword'},item);
    },

    makeTable: function(wordlist) {
        var max = Math.max.apply(null, $.map(wordlist, function(s){return s.length}));
        //console.log(CT.loc.start, max, data.length);
        var px = parseInt($("textarea").css("font-size"));
        var w = $(window).width();
        var h = $(window).height();

        var td_width = px * max;
        var num_td = Math.floor(w/td_width)+1;
        //console.log(w, td_width, num_td);

        var dlen = wordlist.length;
        var fin = [];
        var temp = [];
        var count = 1;
        var tbody = $.each(wordlist, function(i, val){
            var node = $.TD({'class':'completionword'}, val);
            $(node).mousedown(
                    Notebook.Completer.completionClickHandler);
            temp.push(node);
            if (count == num_td) {
                fin.push($.TR({}, temp));
                temp = [];
                count = 0;
            }
            count += 1;
            if (i == dlen-1) {
                fin.push($.TR({}, temp));
                //var twidth = parseInt($("textarea").width()) - tleft;
                tb = $.TBODY({}, fin);
                //console.log(fin);
                //return tb;
            }
        });
        return fin;

        /*
        var self = Notebook.Completer;
        var wordnodes = $.map(wordlist, self.completionItem);
        var code = $.SPAN(null,wordnodes);
        return code;*/
    },


    completionTable2: function(cellid) {
        var elem = $.TABLE({'id':'completions','class':'completions'}, [$.THEAD({}, ''), $.TBODY({}, '')]);
        var pos = $("#"+cellid).position();
        console.log(pos);
        var topval = pos.top+15;
        var leftval = 4*12 + pos.left;
        return $(elem).css("top", topval+"px").css("left", leftval+"px"); //.css("width", twidth+"px");
    },

    completionTable3: function(cellid) {
        var elem = $.TABLE({'id':'completions','class':'completions'}, [$.THEAD({}, ''), $.TBODY({}, '')]);
        return elem;

    },


////////////////////////////////////////
// Managment of a completions session //
////////////////////////////////////////

    completionInitialize: function(cellid, mode) {
        var self = Notebook.Completer;
        if (self.completing) {
            // already completing. refine completion
            if (mode == self.mode) { //same mode, refine
                //this.refine
                return false;
            } else { //restart in new mode
                self.mode = mode;
                //clear completions table
                return true;

            }
        }
        //HACK
        Notebook.delegator.mode = 'completing';
        $($('#'+cellid)[0].textareaNode()).blur(function(e) {
                e.preventDefault();
                Notebook.Completer.completionExit();});
        self.cellid = cellid;
        self.mode = mode;
        self.completing = true;
        var comtable = self.completionTable3(cellid);
        //$('#notebook').append(comtable);
        $('#foot').append(comtable);
        $('#foot').height('20%');
        $('#notebook').css('bottom', '20%');
        var nheight = $('#notebook').height();
        var nscrolltop = $('#notebook').scrollTop();
        var celloffset = $('#' + cellid).offset()['top'];
        if (celloffset - nheight > -20) {
            $('#notebook').scrollTop(nscrolltop + celloffset - nheight);
        }
        return true;
    },

    completionExit: function() {
        var self = Notebook.Completer;
        if (self.completing) {
            $('#completions').remove();
            $('#foot').height('1px');
            $('#notebook').css('bottom', '0');
            self.completing = false;
            self.mode = 'none';
            //$('#'+self.cellid)[0].completion_refinable = false;
            $('#'+self.cellid)[0].completing = false;
            $('#'+self.cellid)[0].setCompletingLabel('off');
            //HACK
            Notebook.delegator.mode = 'normal';
        }
    },

/////////////////
// Completions //
/////////////////

    completeName: function(cellid, tocomplete) {
        var self = Notebook.Completer;
        var mode = 'name';
        if (self.completionInitialize(cellid, mode)) {
            // request 
            //set callbacks
            //$('#'+self.cellid)[0].completion_refinable = false;
            Notebook.Async.completeName(cellid, 
                    mode, 
                    tocomplete, 
                    self.completeNameCallback, 
                    self.completeNameError);
            return;
        } else { // continue with current completion, refine
            self.refineCompletions(tocomplete);
            return;
        }
    },

    completeAttribute: function(cellid, tocomplete) {
        var self = Notebook.Completer;
        var mode = 'attr';
        var input = tocomplete;
        if (self.completionInitialize(cellid, mode)) {
            // request 
            //set callbacks
            //$('#'+self.cellid)[0].completion_refinable = false;
            Notebook.Async.completeName(cellid, 
                    mode, 
                    tocomplete,
                    self.completeNameCallback,
                    self.completeNameError);
            return;
        } else { // continue with current completion, refine
            self.refineCompletions(tocomplete);
            return;
        }
    },
    /*
    completeIntrospect: function(cellid, tocomplete) {

    },
*/
////////////////////////////////////////////////////
// Completion Server Request Callbacks/Errorbacks //
////////////////////////////////////////////////////

    completeNameCallback: function(response) {
        var self = Notebook.Completer;
        var completions = eval(response.out);
        //Notebook.completer.completions = completions; //record of initial completions
        self.completions = completions;
        //$('#'+self.cellid)[0].completion_refinable = true;
        //Notebook.completer.displayCompletions(completions);
        self.displayCompletions(completions);
    },

    completeNameError: function(result) {
    },

///////////////////////////////////////////////
// Completion Results Managment / Refinement //
///////////////////////////////////////////////

    displayCompletions: function(completions) {
        var self = Notebook.Completer;
        // replace nodes
        if (self.singleMatchQ(completions)) {
            var wordnodes = self.makeTable(completions);
            $('#completions tbody').remove(); 
            $('#completions').append(wordnodes); 
            return;
        }
    },

    //Widdle down possibilities:
    //  - add any completly common prefix-parts to the input-text
    //  - upon typing of new char, eliminate impossible matches
    //  - upon deletion, re-display possible matches (remembered)
    //     if deletion past initial tab-completion, re-start completion
    //     mode
    //  - if only one match, commit completion and end

    refineCompletions: function(tocomplete) {
        var self = Notebook.Completer;
        var chk = function(elm, i) {
            return elm.substr(0, tocomplete.length) == tocomplete;
        }
        self.refined_completions = $.grep(self.completions, function(elm, i) {
            return elm.substr(0, tocomplete.length) == tocomplete;
        });
        self.displayCompletions(self.refined_completions);

    },

    singleMatchQ: function(completions) {
        var self = Notebook.Completer;
        if (completions.length > 1) {
            return true;
        } else if (completions.length == 1) {
            //do completion
            self.completionExit();
            var completion_sufix = completions[0].substr($('#'+self.cellid)[0].tomatch.length);
            $('#'+self.cellid)[0].contentInsert(completion_sufix, $('#'+self.cellid)[0].selectionStart);
            return false;
        } else {
            self.completionExit();
            return false;
        }
    },

    pageCompletions: function(keyCode) {
        console.info('pageCompletions', keyCode);
    },
/////////////////////////////////////////////////////
// Managment of Events for the Completions display //
/////////////////////////////////////////////////////
/*
    completionKeyHandler: function(e) {
        switch(e.key().string) {
            case 'KEY_ESCAPE':
                this.completionExit();
                return;
        }
    },

    completionKeyPressHandler: function(e) {
        var input = e.key().string.match(/([a-zA-Z0-9_])/);
    },
*/

    completionClickHandler: function(e) {
        Notebook.Completer.singleMatchQ([e.currentTarget.textContent]);
    },

    completionBlurHandler: function(e) {
        var self = Notebook.Completer;
        self.completionExit();
    }
};

//Notebook.completer = new Notebook.Completer();
//$(document).ready(Notebook.completer.init);
Notebook.__init__.Completer = function() {
    //Notebook.completer = new Notebook.Completer();
    Notebook.Completer.init();
};

