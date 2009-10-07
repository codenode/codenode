/*
######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

 * Indicator.js - Displays messages and stuff.
 */


Notebook.Indicator = {};

Notebook.Indicator.beginMsg = function(text) {
    $("#status_message").text(text);
    $("#status").css("top", "-2px").show();//.animate({"top":"-14"}, 400);
    setTimeout(Notebook.Indicator.endMsg, 3000);
};

Notebook.Indicator.endMsg = function(text) {
    $("#status").animate({"top":"20"}, 500);
};

Notebook.Indicator.endError = function(text) {
    $('.curmsg').text(text).css('background-color','red').fadeOut(10000, function() {
            $(this).remove()});
};

Notebook.Indicator.loading = function() {
    Notebook.Indicator.beginMsg('Loading...');
};

Notebook.Indicator.loaded = function() {
    Notebook.Indicator.endMsg('Notebook Loaded.');
};

Notebook.Indicator.save = function() {
    Notebook.Indicator.beginMsg('Saving...');
};

Notebook.Indicator.saved = function() {
    Notebook.Indicator.endMsg('Saved.');
};

Notebook.Indicator.saveError = function() {
    Notebook.Indicator.endError('Error Saving!');
};
