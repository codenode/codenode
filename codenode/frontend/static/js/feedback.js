/*
######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################
*/
function addFeedbackLink() {
    $("#logout").before("<li><a style='font-weight:bold' id='feedback' href='#'>Feedback</a></li>");
}
function addFeedbackContent(hash){
    //console.log(hash);
    $("#fbcontainer")
    .append('<iframe style="height:400px" src="http://feedback.codenode.org/live" width="100%" border="none"></iframe>')
    .show();
}
function removeFeedbackContent(hash){
    $("#fbcontainer iframe").remove();
    $("#fbcontainer").hide();
    hash.o.remove();
}

$(document).ready(function(){
    addFeedbackLink();
    $("#fbcontainer").jqm({trigger:"#feedback", onShow:addFeedbackContent, onHide:removeFeedbackContent});
});
