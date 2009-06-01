/*
Util - for common misc funtions
*/

Util = {};

Util.nbTitle = function(title) {
    $('#statictitle').innerHTML = title;
    $('#statictitle').enabled = false;
    return;
};

Util.changeTitlePrompt = function(title) {
    var node = $.FORM({'id':'changetitleform'}, 
               $.INPUT({'id':'changetitle', 'type':'text', 'value':title}));
    return node;
};

Util.startChangeTitle = function(e) {
    var self = Util;
    if (!$('#titlecontainer')[0].enabled) {
        $('#titlecontainer')[0].enabled = true;
        $('#statictitle').hide();
        var title = $('#statictitle').text();//document.title;
        var node = Util.changeTitlePrompt(title);
        $(node.firstChild).blur(self.blurChangeTitle);
        $(node).submit(self.exitChangeTitle);
        $('#titlecontainer').append(node);
        node.firstChild.focus();
        return;
    } else {
        //e.stop();
    }
};

Util.blurChangeTitle = function(e) {
    Util.exitChangeTitle();
    return;
};

Util.exitChangeTitle = function() {
    var curtitle = document.title;
    var newtitle = $('#changetitle')[0].value;
    $('#changetitleform').unbind('blur');
    $('#changetitle').unbind('submit');
    $('#changetitleform').remove();
    $('#statictitle').show();
    $('#titlecontainer')[0].enabled = false;
    if (newtitle != curtitle) {
        Notebook.Async.changeNotebookTitle(newtitle, Util.changeTitleCallback, Util.changeTitleError);
    }
};

Util.changeTitleCallback = function(response) {
    var system = $("#logo").text();
    var newtitle = "Knoboo - " + response.title + " - " + system + " notebook";
    document.title = newtitle;
    $('#statictitle')[0].innerHTML = response.title;
};

Util.changeTitleError = function(result) {
};

Util.createKeyQ = function(keyCode) {
    var k = keyCode;
    //note
    //var kenter = 13;
    //var kescape = 27;
    //var kspace = 32;
    //Easy way to see a list of keyCodes with MochiKit.Signal._specialKeys    

    if (k == 13 || k == 27 || k == 32 || ((k > 185) && (k < 193)) || 
        ((k > 218) && (k < 223)) || ((k > 47) && (k < 58)) || 
        ((k > 64) && (k < 91)) || ((k > 95) && (k < 106)) || 
        ((k > 105) && (k < 111))) {
        return true;
    }
    return false;
};

Util.uniqueId = function() {
    var d = new Date();
    id = d.getTime() + Math.random().toString().substr(2,8);
    return id;
};

Util.printList =  function(){
    var plist = $("#printers");
    plist.toggle();
    plist.hover(function(){}, function(){
            setTimeout(function(){plist.hide()}, 500);
        });
};

Util.init = function() {
    $("#print_list").click(Util.printList); 
};

