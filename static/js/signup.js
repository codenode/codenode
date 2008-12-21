SignUp = {

    init: function() {
        $("form").submit(SignUp.checkInfo);    
    },

    checkInfo: function() {
        var args = {};
        var inpts = $(this).find(".in > input");
        $.each(inpts, function(k, v){
            var name = $(v).attr("name");
            var val = $(v).val();
            args[name] = val;
        });
        $.ajax({
            type:"POST",
            url:"create", 
            dataType:"json",
            data:args,
            success:SignUp.handleCreateResponse
        });
        return false;   
    },

    handleCreateResponse: function(data){
        if (data.errors == "None") {
            var form = $("form")[0];
            form.submit();
        } else {
            $("#errors").text(data.errors).show();
        }
    }
}


$(document).ready(SignUp.init);
