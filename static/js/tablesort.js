TableSort = {

	init: function() {
        $("td").click(TableSort.startsortingColumn);
    },


    startsortingColumn: function() {
        var id = $(this).attr("id").split("_")[1];
        var cls = $(this).attr("class");
        var updown = "up";
        $(".updown").remove();
        if (cls == "downsort") {
            $(this).removeClass("downsort").addClass("upsort").append("<span class='updown'>&#8593;</span>");
        } else if (cls == "upsort") { 
            $(this).removeClass("upsort").addClass("downsort").append("<span class='updown'>&#8595;</span>");
            updown = "down";
        } else { 
            $(this).addClass("upsort").append("<span class='updown'>&#8593;</span>");
        }
        TableSort.sortColumn(id, updown);
    },

    sortColumn: function(id, updown) {
        var data = BookShelf._history[BookShelf._current_view];
        if (data.length == 0) return;
        if (id == "cells") {
                data.sort(function(a, b){
                          var aval = parseInt($(a).find(".td_totcells").text());
                          var bval = parseInt($(b).find(".td_totcells").text());
                          if (updown == "up") {return bval-aval;} else {return aval-bval;} 
                         });
        } else if (id == "date") {
                data.sort(function(a, b){
                          var aval = parseInt($(a).find(".td_datemod").attr("id"));
                          var bval = parseInt($(b).find(".td_datemod").attr("id"));
                          if (updown == "up") {return bval-aval;} else {return aval-bval;} 
                         });
        } else if (id == "title") {
                var cmpTitle = function(a, b){
                      var i = 0;
                      var atext = $(a).find(".nblink").text().toLowerCase();
                      var btext = $(b).find(".nblink").text().toLowerCase();
                      aval = atext.charCodeAt(0);
                      bval = btext.charCodeAt(0);
                      while (aval == bval) {
                          i += 1;
                          aval = atext.charCodeAt(i);
                          bval = btext.charCodeAt(i);
                      }
                      if (updown == "up") {return aval-bval;} else {return bval-aval;} 
                }
                data.sort(cmpTitle);
        }
        BookShelf.switchTableBody(data);
    }
}


