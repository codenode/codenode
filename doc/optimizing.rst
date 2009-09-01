Optimizing `codenode` for Efficiency, Scaleability, and Security
================================================================

These are advance configurations, not usually needed
if you are just getting start, or are running `codenode`
on your local machine, with no other users but yourself.


Make `codenode` fast for users, in terms of page loading time
-------------------------------------------------------------
For *best results* serving `codenode` as a web application
for many remote Users, consider some of following steps:

#. Enable 'django-compress' functionality (included in `codenode`).
#. Use a fast webserver (Nginx, Apache, etc) to serve all static content (with URLs that start with '/static') 
#. Use another webserver to server Django (via WSGI).
#. Set 'expires' headers to something large (30days+) so that browers will cache these js files. (If changes are made to any of the js files, you would recompile them all with this script, which would add new dates to the files, so all browers will get the new files).  
#. Have your webserver gzip content.


Run `codenode` under a reverse proxy
------------------------------------

* Nginx:
    http://wiki.codemongers.com/Main
    (TODO: actually write nice how-to, instead of pointing to the Nginx wiki)

* Apache:
    TODO
