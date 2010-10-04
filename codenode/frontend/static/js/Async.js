/*
######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

 Notebook.Async - The AJAX functions -- this is where all async 
            communications are defined.

 */
DATA_URL = '/notebook/'+document.location.pathname.split('/')[2]+'/';
CONTROL_URL = '/backend/'+document.location.pathname.split('/')[2]+'/';
INTERPRETER_URL = '/asyncnotebook/'+document.location.pathname.split('/')[2];
Notebook.Async = function() {
};


// Should Async be a class or not?

Notebook.Async.initialize = function() {
    // eval json written to html body by server
    var url = DATA_URL+'nbobject';
    var success = function (res) {
         if (res.orderlist == "orderlist"){ //no cells exists
            Util.helperCell();
        }
        Notebook.Load.takeCellsData(res);
        }
    $.getJSON(url, success);
    Notebook.Async.startEngine();
    Notebook.Indicator.endMsg();
};

Notebook.Async.startEngine = function() {
    var path = INTERPRETER_URL;
    var data = JSON.stringify({method:'start'});
    $.ajax({
        url:path,
        type:'POST',
        data:data,
        dataType:'json',
        success: function(result) {
            //engine started
            //console.info(result)
        },
        error: function(result) {
            //engine failed to start
            //console.info(result)
        }});
};

Notebook.Async.signalKernel = function(action) {
    var self = Notebook.Async;
    var path = INTERPRETER_URL;
    var data = JSON.stringify({'method':action});
    $.ajax({
            url:path,
            type:'POST',
            data:data,
            dataType:'json',
            success:self.signalSuccess,
            error:self.signalError});
};

Notebook.Async.signalSuccess = function(result) {
};

Notebook.Async.signalError = function(result) {
};

Notebook.Async.evalCell = function(cellid, input) {
    var self = Notebook.Async;
    var path = INTERPRETER_URL;
    if (input == '?') {
        var input = 'introspect?';
    }
    var data = JSON.stringify({method:'evaluate', 'cellid':cellid, 'input':input});
    /*
    $.post(path, data, self.evalSuccess, 'json')
    */
    $.ajax({
            url:path,
            type:'POST',
            data:data,
            dataType:'json',
            success:self.evalSuccess});
    return;
}; 

Notebook.Async.evalSuccess = function(response) {
    var self = Notebook.Async;
    var t = Notebook.TreeBranch;
    var cellid = response.cellid;
    var incount = 'In[' + response.input_count + ']:';
    var outcount = 'Out[' + response.input_count + ']:';
    //$('#'+cellid)[0].saved = true; //not evaluating
    //This is where numbering of cells could go.
    $('#'+cellid)[0].numberLabel(incount);
    var cellstyle = response.cellstyle;
    var content = response.out + response.err;
    t.spawnOutputCellNode(cellid, cellstyle, content, outcount);
    $('#'+cellid)[0].evalResult();
    
    // since these handlers are empty, use the default save which updates cells save state
    // Notebook.Save._save(self.evalSaveSuccess, self.evalSaveError);
    Notebook.Save.save()
};

Notebook.Async.evalError = function(response) {
};

Notebook.Async.evalSaveSuccess = function(response) {
};

Notebook.Async.evalSaveError = function(response) {
};


Notebook.Async.saveToDatabase = function(orderlist, cellsdata, success, error) {
    var path = DATA_URL+'save';
    var cells = JSON.stringify(cellsdata);
    var orderlist = JSON.stringify(orderlist);
    var data = {'orderlist':orderlist, 'cellsdata':cells};
    $.ajax({
            url:path,
            type:'POST',
            data:data,
            dataType:'json',
            success:success,
            error:error});
};

Notebook.Async.deleteCells = function(mainid, ids) {
    var path = BASE_URL+'deletecell';
    var cellids = JSON.stringify(ids);
    var data = {'cellids':cellids};
    /*xxx: need to finish
    var d = a.doXHR(path, {
                    method:'post',
                    headers:{'Content-Type':'application/x-www-form-urlencoded'},
                    sendContent:data});
    var delback = b.partial($(mainid).deleteCallback, mainid)
    d.addCallbacks(delback, $(mainid).deleteErr);
    return d;
    */
};

Notebook.Async.changeNotebookTitle = function(title, success, error) {
    var path = DATA_URL+'title';
    var data = {'newtitle':title};
    $.ajax({
            url:path,
            type:'POST',
            data:data,
            dataType:'json',
            success:success,
            error:error});
};



/** completeName - for completing the name of a variable or function */
Notebook.Async.completeName = function(cellid, mode, input, success, error) {
    //request match from server
    // this ultimatly returns a list of 0 or more match possibilities
    var path = INTERPRETER_URL;
    var data = JSON.stringify({method:'complete', 'mode':mode, 'cellid':cellid, 'input':input});
    $.ajax({
            url:path,
            type:'POST',
            data:data,
            dataType:'json',
            success:success,
            error:error});
};

//$(document).ready(Notebook.Async.initialize);
Notebook.__init__.Async = function() {
    Notebook.Async.initialize();
};
