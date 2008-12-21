/*

TODO:
    * Loading dialog
    * Undo ability
    * Empty trash / buttons need to reflect current section
    * Don't allow moving of notebooks to current visible section
    * Update bookshelf with new changes (poll for changes) - BUG in 'date' (last modified not working)
    * Test 'niceDate' for notebooks older that 1 year.
*/

BookShelf = {
	
    _view_map: {'all':0, 'trash':1, 'archive':2, 'folder':3}, //folder needs to be generalized
    _current_view: 'all',
    _update_interval: 5000, /*millisecond interval to check for new changes*/
    _register_update: true, /*bool to be set if user is actively viewing/manipulating the bookshelf*/

	init: function() {
        if ($.browser.msie) BookShelf.ieMessage();
        $('#general-folders').find(".drop").click(BookShelf.generalFolderClick);
        $("#search").submit(BookShelf.searchNotebooks);
        $("#refresh").click(BookShelf.loadBookShelf);
        $("#new_folder").click(BookShelf.newFolder);
        $("#delete-folder").click(BookShelf.deleteFolder);
        $("#new_notebook").click(BookShelf.newNotebookList);
        $("#notebook_list li a").click(BookShelf.refreshNotebooks);
        $("#archive_button, #trash_button").click(BookShelf.moveChecked);
        BookShelf.sortCreate();
        BookShelf.loadUserFolders();
        BookShelf.makeListDropable('general-folders');
        BookShelf.ctxMenu();
        $('#_root').click();
	},

    ieMessage: function() {
        var msg = "<h3 style='margin:40px; text-align:center'>Sorry! Internet Explorer support in progress. ";
        msg += " Please use <a href='http://mozilla.com'>Firefox</a> or <a href='http://apple.com'>Safari</a>.</h3>";
        $("body").empty().append(msg);
        return;
    },

    /*Get current bookshelf data from the server.

    The 'folder' arg is to access all the notebooks in
    a given folder if that is the current view.

    The 'sort' arg specifies what the resulting data
    should be sorted on.  The sorting occurs on the
    server, but may change to the client in the future.*/
    loadBookShelf: function(){
        var folder = window.location.hash.split('#')[1];
        var sort = BookShelf.getSortState();
        var url = 'load?location=' + folder + '&' + sort; 
        $.getJSON(url, BookShelf.populateTable);
        //$(window).focus(BookShelf.isUpdateNeeded);
    },

    sectionMessage: function() {
        var hash = window.location.hash.split('#')[1];
        var message = '';
        switch(hash) {
            case 'root':
                message = "You have no notebooks.  Click 'New Notebook' to get started."; 
                break;
            case 'trash':
                message = "The trash is empty.";
                break;
            case 'archive':
                message = "You have no archived notebooks.";
                break;
            default:
                message = "There are no notebooks in this folder.";
                break;
        }
        var p = $.P({id:"table_empty"}, message);
        $('table.notebookview').after(p);
    },

    populateTable: function(data) {
        $('tbody.notebooktbody').empty();
        $('#table_empty, #empty-trash').remove();
        if (data.length < 1) {
            BookShelf.sectionMessage();
            return;
        };

        /* Enable the 'Empty Trash' functionality */
        var hash = window.location.hash.split('#')[1];
        if (hash == 'trash') {
            var p = $.P({id:"empty-trash", class:"pointer"}, " Empty Trash");
            $('table.notebookview').before(p);
            $("#empty-trash").click(BookShelf.emptyTrash);
        }

        var trs = [];
        for (var i in data) {
            var nbid = data[i][0];
            var nbtitle = data[i][1];
            var nbkernel = data[i][2];
            var nbtimemod = data[i][3];
            var nblocation = data[i][4];

            var nbpath = '/notebook/'+nbid;

            var td1 = $.TD({width:2, className:nblocation}, $.INPUT({type:'checkbox', className:'deleteradio'}));
            var td2 = $.TD({}, $.A({href:nbpath, className:'nblink', target:'_blank'}, nbtitle));
            var td3 = $.TD({className:'td_kernel'}, nbkernel);
            var td4 = BookShelf.dateTD(nbtimemod);
            var tr = $.TR({id:nbid},[td1, td2, td3, td4]);
            trs.push(tr);
        };
        $('tbody.notebooktbody').append(trs);
        BookShelf.redrawTable();
        BookShelf.dragCreate();
        var folder = window.location.hash.split('#')[1];
        //$('#location').text(folder);
    },

    redrawTable: function(){
        $("tbody.notebooktbody tr:even").attr('className', 'even');
        $("tbody.notebooktbody tr:odd").attr('className', 'odd');
    },

    newNotebookList: function(){
        var nblist = $("#notebook_list");
        nblist.toggle();
        nblist.hover(function(){}, function(){
                setTimeout(function(){nblist.hide();}, 500);
            });
    },

    refreshNotebooks: function(){
        setTimeout(BookShelf.loadBookShelf, 500);
    },

    loadUserFolders: function() {
        var url = 'folders';
        $.getJSON(url, BookShelf.populateUserFolders);
    },

    populateUserFolders: function(data) {
        var folders = [];
        for (var i in data) {
            var id = '_'+data[i][0];
            var name = data[i][1];

            var folder = $.LI({}, 
                    $.DIV({className:'area-selected'},
                        $.DIV({id:id, className:'drop user-folder'}, name)
                        )
                    );
            folders.push(folder);
        }
        $('div#user-folders > ul').empty();
        $('div#user-folders > ul').append(folders);
        $('#user-folders').find(".drop").click(BookShelf.userFolderClick);
        BookShelf.makeListDropable('user-folders');
    },

    newFolder: function(){
        var data = {"create":"New Folder"};
        $.ajax({
            type:"POST",
            url:"folders", 
            dataType:"json",
            data:data,
            success:BookShelf.newFolderCallback
        });
    },

    newFolderCallback: function(data) {
        var id = '_'+data[0][0];
        var name = data[0][1];
        var folder = $.LI({}, 
                $.DIV({className:'area-selected'},
                    $.DIV({id:id, className:'drop user-folder'}, name)
                    )
                );
        $('div#user-folders > ul').append(folder);
        BookShelf.makeListDropable('user-folders');
        $('#'+id).click(BookShelf.userFolderClick).click();
        $('input.location-name').focus();
    },

    deleteFolder: function(){
        var deleteOk = confirm("Are you sure?\nThis will delete the Folder and ALL CONTENTS.\nThis action CANNOT be undone.");
        if (!deleteOk) {
            return;
        } else {
            var folderid = window.location.hash.split('#')[1];
            var nbids = [];
            /* The notebook ids are the #id attributes of the notebook <table> <tr> elements */
            $.each($("tbody tr"), function(k,v){nbids.push($(v).attr("id"))}) 
            var data = {'delete':'1', 'folderid':folderid, 'nbids':nbids};
            $.ajax({
                type:"POST",
                url:"folders", 
                dataType:"json",
                data:data,
                success:BookShelf.deleteFolderCallback
            });
        }
    },

    deleteFolderCallback: function(){
        /*Could be made 'cleaner', but this does the job:*/
        window.location.reload();
    },

    emptyTrash: function(){
        var emptyOk = confirm("Are you sure?\nThis will delete ALL CONTENTS.\nThis action CANNOT be undone.");
        if (!emptyOk) {
            return;
        } else {
            var nbids = [];
            /* The notebook ids are the #id attributes of the notebook <table> <tr> elements */
            $.each($("tbody tr"), function(k,v){nbids.push($(v).attr("id"))}) 
            var data = {'nbids':nbids};
            $.ajax({
                type:"POST",
                url:"emptytrash", 
                dataType:"json",
                data:data,
                success:BookShelf.emptyTrashCallback
            });
        }
    },

    emptyTrashCallback: function(){
       $("#_root").click(); 
    },

    _folderClick: function() {
        //add clicked class to elements with drop class (css)
        $(".area_selected, .drop").css("backgroundColor", "#F5F5F5");
        //move styling to style sheet, set class selected
        $(this).css("backgroundColor", "#DCDCDC");
        $(this).parent(".area_selected").css("backgroundColor", "#DCDCDC");

        var id = $(this).attr("id").split('_')[1];
        var name = $(this).text();
        InfoBar.setLocation(id, name);
        /*
        var userfolderQ = $(this).parents('#user-folders');
        if (userfolderQ.length) {
            var dorename = true;
        } else {
            var dorename = false;
        }
        InfoBar.setLocation(id, name, dorename);
        */
    },

    generalFolderClick: function() {
        $(".area_selected, .drop").css("backgroundColor", "#F5F5F5");
        $(this).css("backgroundColor", "#DCDCDC");
        $(this).parent(".area_selected").css("backgroundColor", "#DCDCDC");
        $('.drop').removeClass('active');
        $(this).addClass('active');
        var id = $(this).attr("id").split('_')[1];
        var name = $(this).text();
        $("div.infobar").hide();
        InfoBar.setLocation(id, name);
        BookShelf.loadBookShelf();
    },

    userFolderClick: function() {
        $(".area_selected, .drop").css("backgroundColor", "#F5F5F5");
        $(this).css("backgroundColor", "#DCDCDC");
        $(this).parent(".area_selected").css("backgroundColor", "#DCDCDC");
        $('.drop').removeClass('active');
        $(this).addClass('active');
        var id = $(this).attr("id").split('_')[1];
        var name = $(this).text();
        InfoBar.setRename(id, name);
        $("div.infobar").show();
        BookShelf.loadBookShelf();

    },

    moveData: function(nbid, destination) {
        var data = {'dest':destination, 'nbid':nbid};
        $.map(nbid, function(n,i) {$('#'+n).remove();});
        BookShelf.redrawTable();
        $.ajax({
            type:"POST",
            url:"move", 
            dataType:"json",
            data:data,
            success:BookShelf.moveDataCallback
        });
    },

    moveDataCallback: function(res) {
    },

	moveChecked: function(){
        var destination = $(this).attr("id").split("_")[0];
        var checked = $("input:checked").parents('tr');
        var checkedid = $.map(checked, function(n, i) {
            return $(n).attr('id');
            });
        if (checkedid.length == 0) {
            StatusDialog.beginMsg("No notebooks are selected.");
            return;
        }
        BookShelf.moveData(checkedid, destination);
    },


    movectxMenu: function(e, dest){
        //if (self._current_view == dest) return;
        BookShelf.moveData(BookShelf._contextSelected, BookShelf._view_map[dest]);
        $("#drop_"+dest).animate({backgroundColor:"#FF0"},200).animate({backgroundColor:"#EEF2F5"},200);
        BookShelf._contextSelected = '';
        BookShelf.loadBookShelf(); //Optimize this (no server call).
    },

    ctxMenu: function(){
        var ctx_opts = {
            bindings: {
                "ctx_all": function(t) {
                    return BookShelf.movectxMenu(t, "all");
                },
                "ctx_folder": function(t) {
                    return BookShelf.movectxMenu(t, "folder");
                },
                "ctx_archive": function(t) {
                    return BookShelf.movectxMenu(t, "archive");
                },
                "ctx_trash": function(t) {
                    return BookShelf.movectxMenu(t, "trash");
                }
            },
            onContextMenu: function(e) {
                var what = $(e.originalTarget).parents('tr');
                if (what) {
                    BookShelf._contextSelected = $(what).attr('id');
                    return true;
                }
                return false;
            },
            onShowMenu: function(e, menu) {
                menu.what = e.what;
                return menu;
            }
        };
        $("tbody").contextMenu("ctxmenu", ctx_opts);
    },


    /* === Search of notebooks functionality === 
     *
     *     The submit event of the search form and 
     *     the 'click' event of the Search button
     *     by the 'searchNotebooks' function.
     *
     *     On success of the search query, the notebooks
     *     table is redrawn with the data of all matched notebooks.
     */
    searchNotebooks: function() {
        var q = $("#searchquery").attr("value");
        if (q) {
            $.ajax({
                type: "GET",
                url: "search", 
                data: {"q": q}, 
                dataType: "json",
                success: BookShelf.searchResults
            });
        }
        return false;
    },

    /* 'searchResults' first clears any last search results 
     *  from the _history["search"] array.
     *
     *  The we loop over all existing notebooks and take
     *  all the notebooks (in the _history["all"] array)
     *  and redraw a new notebook table with the matches
     */
    searchResults: function(data) {
        var msgs = [$.SPAN({},"Search results for:"), $.SPAN({className:'squery'}, data.query)];
        var msg = $.P({id:"tablestate_search"}, msgs);
        //$("table").before(msg);
        BookShelf.populateTable(data.results);
    },
    /* === End Search notebooks functionality === */


    dragCreate: function(){
        var colorDrag = function() {
            var uid = new Date().getTime();
            var c = $(this).clone().attr({id:uid}).css({"backgroundColor":"#9BC2E9", "border-width": "2px"});
            return c;
        }
        var startLog = function() {
            return;
        }
        var stopDrag = function(){
        };

        $("tbody tr").draggable({
            opacity:0.8, 
            revert:true, 
            helper:colorDrag, 
            start:startLog,
            stop:stopDrag
        });
	},

    makeListDropable: function(listid) {
        var getDropped = function(ev, ui){
            $(ui.helper).hide();
            $(ui.droppable.element).animate({backgroundColor:"#FF0"},200)
            .animate({backgroundColor:$(this).css("backgroundColor")},200);

            var drop_id = $(ui.droppable.element).attr("id");
            var drag_id = $(ui.draggable.element).attr("id");
            var destination = drop_id.split('_')[1]; 
            //Destination id should be set in template?
            BookShelf.moveData([drag_id], destination);
            };
        var overfun = function(ev, ui){$.extend(ui.draggable.options, {revert:false})};
        var outfun = function(ev, ui){$.extend(ui.draggable.options, {revert:true})};

        $('#'+listid).find(".drop").droppable({
            accept:"tr",
            tolerance: "pointer",
            hoverClass: "drop_ok",
            //over: overfun,
            //out: outfun,
            drop: getDropped
        });
    },

    sortCreate: function() {
        $('thead td.sortable').click(BookShelf.sortClick);
        $('td#column_lastmodified').addClass('active desc');
    },

    sortClick: function(e) {
        if ($(this).hasClass('active')) {
            $(this).hasClass('asc') ? $(this).removeClass('asc').addClass('desc') :
                $(this).removeClass('desc').addClass('asc');
        } else {
            $('thead td').removeClass('active asc desc');
            $(this).addClass('active desc');
        }
        BookShelf.loadBookShelf();
    },

    getSortState: function() {
        var col = $('thead td.active');
        var order = $(col).attr('id').split('_')[1];
        var sort = $(col).hasClass('asc') ? 'asc' : 'desc';
        return $.param({'order':order, 'sort':sort});
    },

    niceDate: function(dat){
        var offset = (new Date()).getTimezoneOffset() * 60 * 1000;
        var local = (dat.getTime() - offset); 
        var diff = (((new Date()).getTime() - local) / 1000);
		var day_diff = Math.floor(diff / 172800);

        if ( isNaN(day_diff) || day_diff < 0 || day_diff >= 31 )
            return;
        return day_diff == 0 && (
            diff < 60 && "just now" ||
            diff < 120 && "1 minute ago" ||
            diff < 3600 && Math.floor( diff / 60 ) + " minutes ago" ||
            diff < 7200 && "1 hour ago" ||
            diff < 172800 && Math.floor( diff / 3600 ) + " hours ago") ||
            day_diff == 1 && "Yesterday" ||
            day_diff < 7 && day_diff + " days ago" ||
            day_diff < 31 && Math.ceil( day_diff / 7 ) + " weeks ago";
    },

    dateTD: function(data){
        var DAYS = ['Sun', 'Mon','Tues','Wed','Thurs','Fri','Sat']; 
        var MONTHS = ['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec'];
        var data = data.replace(/-/g, "/");
        var d = new Date(data);
        var day = DAYS[d.getDay()];
        var dates = d.getDate();
        var month = MONTHS[d.getMonth()];
        var minutes = d.getMinutes();
        if (parseInt(minutes/10) == 0) minutes = "0"+minutes;
        var hours = d.getHours();
        if (hours/12 > 1) {
            var td = hours-12;
            var t = td+":"+minutes+"pm";
        } else {
            if (hours == 0) hours = 12;
            var t = hours+":"+minutes+"am";
        }
        var nicedate = day+", "+month+" "+dates+", "+t; 
		var epoch = Math.floor(d.getTime()); 
        /* var data = data.replace(/-/g, "/");// + ' GMT'
        //console.log(data);
        var dateobj = new Date(data);
        var nicedate = BookShelf.niceDate(dateobj);
        console.log(dateobj);
		var epoch = Math.floor(dateobj.getTime());*/ 
        return $.TD({id:epoch, className:'td_datemod'}, nicedate); //+" - "+d.getFullYear());
    }

};



InfoBar = {
    setLocation: function(loc, name) {
        window.location.assign('#'+loc);
    },

    setRename: function(loc, name) {
        InfoBar.setLocation(loc, name);
        InfoBar.reset();
        $('input.location-name').val(name);
        InfoBar.activateRename();

    },

    reset: function() {
        $('#rename-folder').unbind();
        $('input.location-name').removeClass('active');
        $('input.location-name')[0].readOnly = true;
    },

    activateRename: function() {
        //$('input.location-name').hover(self.overCallback, self.outCallback);
        $('input.location-name').addClass('active');
        $('#rename-folder').submit(InfoBar.rename);
        $('input.location-name')[0].readOnly = false;
    },

    overCallback: function(e) {

    },

    overCallback: function(e) {

    },

    click: function(e) {

    },

    rename: function() {
        var id = window.location.hash.split('#')[1];
        var newname = $('input.location-name').val();
        var data = {'update':'1', 'newname':newname, 'id':id};
        $(this).children('input').blur();
        $.ajax({
            type:"POST",
            url:"folders", 
            dataType:"json",
            data:data,
            success:InfoBar.renameFolderCallback
        });
        return false;
    },

    renameFolderCallback: function(data) {
        var id = '_'+data[0][0];
        var name = data[0][1];
        $('#'+id).text(name); 
    }
};

/* Styling and visual feedback for the BookShelf */
BookShelfStyling = {
    init: function(){
        var split_opts = {type: 'v', initA: true, splitbarClass: 'panehandle'};
        $('#splitpane').splitter(split_opts);
    	$("#attach_overlay").jqm();
        $("#search input").focus(function(){$(this).css("color", "#F00").attr("value", "Sorry! Work in progress.")});
        $("#search input").blur(function(){$(this).css("color", "#9F9F9F").attr("value", "Search Notebooks")});
    	$("#control").corner({autoPad:true, antiAlias:true, tl:{radius:4}, tr:{radius:4}, bl:{radius:0}, br:{radius:0}});
        $("#status_close, .button, .drop").hover(function(){$(this).addClass('pointer');}, function(){$(this).removeClass('pointer');});
        $(window).bind('resize', function() {
                $('#splitpane').trigger('resize');
                }).trigger('resize');
        setTimeout(BookShelfStyling.roundButtons, 10); 
    },

    roundButtons: function() {
    	$(".button").corner({autoPad:true, antiAlias:true, tl:{radius:4}, tr:{radius:4}, bl:{radius:4}, br:{radius:4}});
    }
};

StatusDialog = {

    beginMsg: function(msg){
        $("#status_message").text(msg);
        $("#status").show().animate({"top":"-14"}, 400);
        setTimeout(StatusDialog.endMsg, 3000);
    },

    endMsg: function(){
        $("#status").animate({"top":"16"}, 500);
    }
};


AttachData = {
    init: function(){
        $("#uploadform").submit(AttachData.handleUpload); 
        $("#remote_attach").submit(AttachData.handleRemoteFile); 
        $("#attach_buttons button:first").click(AttachData.handleClick); 
    },

    handleClick: function(){
        var idoc = $("iframe")[0];
        upform = $(idoc.contentWindow.document.getElementById("uploadform"));
        var input = upform.find("input").val();
        if (input != ""){
            return AttachData.handleUpload(); 
        }
        var input2 = $("#remote_attach input:first").val();
        if (input2 != "") {
            return AttachData.handleRemoteFile(input2); 
        }
        //console.log("click => ", $(this));
    },

    handleRemoteFile: function(url){
        $.ajax({
            type: "GET",
            url: "attachremote", 
            data: {"url": url}, 
            dataType: "json",
            success: function(data){return;}//console.log(data)}
        });
        return false;
    },
    
    handleUpload: function(){
        var e = $(this);
        var idoc = $("iframe")[0];
        //console.log(e, idoc);
        var btn = $(idoc.contentWindow.document.getElementById("upload_btn"));
        var form = idoc.contentWindow.document.getElementById("uploadform");
        $(btn).click(function(){ form.submit(); });
    }
};
    
$(document).ready(function(){
    BookShelf.init();
    BookShelfStyling.init();
    AttachData.init();    
});

