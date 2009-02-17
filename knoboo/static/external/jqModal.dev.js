/*
 * jqModal - Minimalist Modaling with jQuery
 *
 * Copyright (c) 2007 Brice Burgess <bhb@iceburg.net>, http://www.iceburg.net
 * Licensed under the MIT License:
 * http://www.opensource.org/licenses/mit-license.php
 * 
 * $Version: 2007.??.?? +r12 beta
 * Requires: jQuery 1.1.3+
 */
(function($) {
/**
 * Initialize a set of elements as "modals". Modals typically are popup dialogs,
 * notices, modal windows, and image containers. An expando ("_jqm") containing
 * the UUID or "serial" of the modal is added to each element. This expando helps
 * reference the modal's settings in the jqModal Hash Object (jQuery.jqm.hash)
 * 
 * Accepts a parameter object with the following modal settings;
 * 
 * (Integer) zIndex - Desired z-Index of the modal. This setting does not override (has no effect on) preexisting z-Index styling (set via CSS or inline style).  
 * (Integer) overlay - [0-100] Translucency percentage (opacity) of the body covering overlay. Set to 0 for NO overlay, and up to 100 for a 100% opaque overlay.  
 * (String) overlayClass - This class is applied to the body covering overlay. Allows CSS control of the overlay look (tint, background image, etc.).
 * (String) closeClass - A close trigger is added to all elements matching this class within the modal.
 * (Mixed) trigger - An open trigger is added to all matching elements within the DOM. Trigger can be a selector String, a jQuery collection of elements, a DOM element, or a False boolean.
 * (Mixed) ajax - If not false; The URL (string) to load content from via an AJAX request.
 *                If ajax begins with a "@", the URL is extracted from the requested attribute of the triggering element.
 * (Mixed) target - If not false; The element within the modal to load the ajax response (content) into. Allows retention of modal design (e.g. framing and close elements are not overwritten by the AJAX response).
 *                  Target may be a selector string, jQuery collection of elements, or a DOM element -- but MUST exist within (as a child of) the modal.
 * (Boolean) modal - If true, user interactivity will be locked to the modal window until closed.
 * (Boolean) toTop - If true, modal will be posistioned as a first child of the BODY element when opened, and its DOM posistion restored when closed. This aids in overcoming z-Index stacking order/containment issues where overlay covers whole page *including* modal.
 * (Mixed) onShow - User defined callback function fired when modal opened.
 * (Mixed) onHide - User defined callback function fired when modal closed.
 * (Mixed) onLoad - User defined callback function fired when ajax content loads.
 *
 * @name jqm
 * @param Map options User defined settings for the modal(s).
 * @type jQuery
 * @cat Plugins/jqModal
 */
$.fn.jqm=function(p){
var o = {
zIndex: 3000,
overlay: 50,
overlayClass: 'jqmOverlay',
closeClass: 'jqmClose',
trigger: '.jqModal',
ajax: false,
target: false,
modal: false,
toTop: false,
onShow: false,
onHide: false,
onLoad: false
};

// For each element (aka "modal") $.jqm() has been called on;
//  IF the _jqm expando exists, return (do nothing)
//  ELSE increment serials and add _jqm expando to element ("serialization")
//    *AND*...
return this.each(function(){if(this._jqm)return;s++;this._jqm=s;

// ... Add this element's serial to the jqModal Hash Object 
//  Hash is globally accessible via jQuery.jqm.hash. It consists of;
//   c: {obj} config/options
//   a: {bool} active state (true: active/visible, false: inactive/hidden)
//   w: {JQ DOM Element} The modal element (window/dialog/notice/etc. container)
//   s: {int} The serial number of this modal (same as "H[s].w[0]._jqm")
//   t: {DOM Element} The triggering element
// *AND* ...
H[s]={c:$.extend(o,p),a:false,w:$(this).addClass('jqmID'+s),s:s};

// ... Attach events to trigger showing of this modal
o.trigger&&$(this).jqmAddTrigger(o.trigger);
});};

// Adds behavior to triggering elements via the hide-show (HS) function.
// 
$.fn.jqmAddClose=function(e){return HS(this,e,'jqmHide');};
$.fn.jqmAddTrigger=function(e){return HS(this,e,'jqmShow');};

// Hide/Show a modal -- first check if it is already shown or hidden via the toggle state (H[{modal serial}].a)
$.fn.jqmShow=function(t){return this.each(function(){!H[this._jqm].a&&$.jqm.open(this._jqm,t)});};
$.fn.jqmHide=function(t){return this.each(function(){H[this._jqm].a&&$.jqm.close(this._jqm,t)});};

$.jqm = {
hash:{},

// Function is executed by $.jqmShow to show a modal
// s: {INT} serial of modal
// t: {DOM Element} the triggering element

// set local shortcuts
//  h: {obj} this Modal's "hash"
//  c: {obj} (h.c) config/options
//  cc: {STR} closing class ('.'+h.c.closeClass)
//  z: {INT} z-Index of Modal. If the Modal (h.w) has the z-index style set it will use this value before defaulting to the one passed in the config (h.c.zIndex)
//  o: The overlay object
// mark this modal as active (h.a === true)
// set the triggering object (h.t) and the modal's z-Index.
open:function(s,t){var h=H[s],c=h.c,cc='.'+c.closeClass,z=/^\d+$/.test(h.w.css('z-index'))&&h.w.css('z-index')||c.zIndex,o=$('<div></div>').css({height:'100%',width:'100%',position:'fixed',left:0,top:0,'z-index':z-1,opacity:c.overlay/100});h.t=t;h.a=true;h.w.css('z-index',z);
 
 // IF the modal argument was passed as true;
 //    Bind the Keep Focus Function if no other Modals are open (!A[0]),
 //    Add this modal to the opened modals stack (A) for nested modal support,
 //    and Mark overlay to show wait cursor when mouse hovers over it.
 if(c.modal) {!A[0]&&F('bind');A.push(s);o.css('cursor','wait');}
 
 // ELSE IF an overlay was requested (translucency set greater than 0);
 //    Attach a Close event to overlay to hide modal when overlay is clicked.
 else if(c.overlay > 0)h.w.jqmAddClose(o);
 
 // ELSE disable the overlay
 else o=false;

 // Add the Overlay to BODY if not disabled.
 h.o=(o)?o.addClass(c.overlayClass).prependTo('body'):false;
 
 // IF IE6;
 //  Set the Overlay to 100% height/width, and fix-position it via JS workaround
 if(ie6&&$('html,body').css({height:'100%',width:'100%'})&&o){o=o.css({position:'absolute'})[0];for(var y in {Top:1,Left:1})o.style.setExpression(y.toLowerCase(),"(_=(document.documentElement.scroll"+y+" || document.body.scroll"+y+"))+'px'");}

 // IF the modal's content is to be loaded via ajax;
 //  determine the target element {JQ} to recieve content (r),
 //  determine the URL {STR} to load content from (u)
 if(c.ajax) {var r=c.target||h.w,u=c.ajax,r=(typeof r == 'string')?$(r,h.w):$(r),u=(u.substr(0,1) == '@')?$(t).attr(u.substring(1)):u;
 
  // Load the Content (and once loaded);
   // Fire the onLoad callback (if exists),
   // Attach closing events to elements inside the modal that match the closingClass,
   // and Execute the jqModal default Open Callback
  r.load(u,function(){c.onLoad&&c.onLoad.call(this,h);cc&&h.w.jqmAddClose($(cc,h.w));O(h);});}
 
 // ELSE the modal content is NOT to be loaded via ajax;
 //  Attach closing events to elements inside the modal that match the closingClass
 else cc&&h.w.jqmAddClose($(cc,h.w));

 // IF toTop was passed and an overlay exists;
 //  Remember the DOM posistion of the modal by inserting a tagged (matching serial) <SPAN> before the modal
 //  Move the Modal from its current position to a first child of the body tag (after the overlay)
 c.toTop&&h.o&&h.w.before('<span id="jqmP'+h.w[0]._jqm+'"></span>').insertAfter(h.o);	
 
 // Execute user defined onShow callback, or else show (make visible) the modal.
 // Execute the jqModal default Open Callback.
 // Return false to prevent trigger click from being followed.
 c.onShow&&c.onShow(h);h.w.show();O(h);return false;
},

// Function is executed by $.jqmHide to hide a modal
  // mark this modal as inactive (h.a === false)
close:function(s){var h=H[s];h.a=false;
 // If modal, remove from modal stack.
   // If no modals in modal stack, unbind the Keep Focus Function
 if(h.c.modal){A.pop();!A[0]&&F('unbind');}
 
 // IF toTop was passed and an overlay exists;
 //  Move modal back to its previous ("remembered") position.
 h.c.toTop&&h.o&&$('#jqmP'+h.w[0]._jqm).after(h.w).remove();
 
 // Execute user defined onHide callback, or else hide (make invisible) the modal and remove the overlay.
 if(h.c.onHide)h.c.onHide(h);else{h.w.hide()&&h.o&&h.o.remove()}return false;
}};

// set jqModal scope shortcuts;
//  s: {INT} serials placeholder
//  H: {HASH} shortcut to jqModal Hash Object
//  A: {ARRAY} Array of active/visible modals
//  ie6: {bool} True if client browser is Internet Explorer 6
//  i: {JQ, DOM Element} iframe placeholder used to prevent active-x bleedthrough in IE6
//    NOTE: It is important to include the iframe styling (iframe.jqm) in your CSS!
//     *AND* ...
var s=0,H=$.jqm.hash,A=[],ie6=$.browser.msie&&($.browser.version == "6.0"),i=$('<iframe src="javascript:false;document.write(\'\');" class="jqm"></iframe>').css({opacity:0}),

//  O: The jqModal default Open Callback;
//    IF ie6; Add the iframe to the overlay (if overlay exists) OR to the modal (if an iframe doesn't already exist from a previous opening)
//    Execute the Modal Focus Function
O=function(h){if(ie6)h.o&&h.o.html('<p style="width:100%;height:100%"/>').prepend(i)||(!$('iframe.jqm',h.w)[0]&&h.w.prepend(i)); f(h);},

//  f: The Modal Focus Function;
//    Attempt to focus the first visible input within the modal
f=function(h){try{$(':input:visible',h.w)[0].focus();}catch(e){}},

//  F: The Keep Focus Function;
//    Binds or Unbinds (t) the Focus Examination Function to keypresses and clicks
F=function(t){$()[t]("keypress",x)[t]("keydown",x)[t]("mousedown",x);},

//  x: The Focus Examination Function;
//    Fetch the current modal's Hash as h (supports nested modals)
//    Determine if the click/press falls within the modal. If not (r===true);
//      call the Modal Focus Function and prevent click/press follow-through (return false [!true])
//      ELSE if so (r===false); follow event (return true [!false])
x=function(e){var h=H[A[A.length-1]],r=(!$(e.target).parents('.jqmID'+h.s)[0]);r&&f(h);return !r;},

// hide-show function; assigns click events to trigger elements that 
//   hide, show, or hide AND show modals.

// Expandos (jqmShow and/or jqmHide) are added to all trigger elements. 
// These Expandos hold an array of modal serials {INT} to show or hide.

//  w: {DOM Element} The modal element (window/dialog/notice/etc. container)
//  e: {DOM Elemet||jQ Selector String} The triggering element
//  y: {String} Type (jqmHide||jqmShow)

//  s: {array} the serial number of passed modals, calculated below;
HS=function(w,e,y){var s=[];w.each(function(){s.push(this._jqm)});

// for each triggering element attach the jqmHide or jqmShow expando (y)
//  or else expand the expando with the current serial array
 $(e).each(function(){if(this[y])$.extend(this[y],s);
 
 // Assign a click event on the trigger element which examines the element's
 //  jqmHide/Show expandos and attempts to execute $.jqmHide/Show on matching modals
 else{this[y]=s;$(this).click(function(){for(var i in {jqmShow:1,jqmHide:1})for(var s in this[i])if(H[this[i][s]])H[this[i][s]].w[i](this);return false;});}});return w;};
})(jQuery);