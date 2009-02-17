##################################################################### 
# Copyright (C) 2007 Alex Clemesha <clemesha@gmail.com>
#                and Dorian Raymer <deldotdr@gmail.com>
# 
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
##################################################################### 

from zope.interface import implements
from twisted.cred import portal, checkers, credentials, error as credError

from knoboo.external.twisted.web2 import iweb
from knoboo.external.twisted.web2 import http_headers
from knoboo.external.twisted.web2 import http

from knoboo.resources import resources
from knoboo.templates import templates



class RegularUserAvatar(resources.UserNotebooks):
    """Top level resource of Knoboo.
    
    This resource always does a redirect to the
    users bookshelf so that after login (which is
    a POST operation), the postdata will not remain
    in the browser on return.  This method is sometimes
    referred to as the post-redirect-get method.
    """

    def logout(self):
        """take care of shutting down engines...
        """
        self.child_notebook.nbSessionManager.endAllSessions()


class LoginSystem(object):
    implements(portal.IRealm)

    def __init__(self, dbManager, nbSessionManager, config):
        self.dbManager = dbManager
        self.nbSessionManager = nbSessionManager
        self.config = config

    def requestAvatar(self, avatarId, mind, *interfaces):
        """Return resource avatar containing appropriate resource tree.

        """
        if avatarId is checkers.ANONYMOUS:
            return 'fail'
            r = AnonymousAvatar(self.dbManager, self.config)
            return (iweb.IResource, r, r.logout) 
        r = RegularUserAvatar(self.nbSessionManager)
        return (iweb.IResource, r, r.logout)






