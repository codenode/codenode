######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

from django.http import HttpResponse
from django.contrib.auth import authenticate

def newadmin(request):
    """Check to see if the default admin account exists.

    The default admin account, with username "admin"
    and password "admin", exists by default for 
    convenience.  Once the admin logs in and changes 
    the admin password, then the message will disappear.
    """
    admin = authenticate(username='admin', password='admin')
    if admin is not None:
        resp = """<div id='newadmin'>Login as Username:<b>admin</b> and Password:<b>admin</b>
                 <div>After logging in, go to <b>Settings</b>, change
                 the admin password, and this message will disappear.</div></div>
               """
    else:
        resp = ""
    return HttpResponse(resp)
