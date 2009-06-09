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
