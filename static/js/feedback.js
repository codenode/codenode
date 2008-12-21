
function addFeedbackLink() {
    $("#logout").before("<li><a style='font-weight:bold' id='feedback' href='#'>Feedback</a></li>");
}
function addFeedbackContent(hash){
    //console.log(hash);
    $("#fbcontainer")
    .append('<iframe style="height:400px" src="http://feedback.knoboo.com/live" width="100%" border="none"></iframe>')
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
