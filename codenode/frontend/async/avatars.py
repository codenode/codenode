######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

from zope.interface import implements
from twisted.cred import portal, checkers, credentials, error as credError

from codenode.external.twisted.web import resource

from codenode.resources import resources
from codenode.templates import templates



class RegularUserAvatar(resources.UserNotebooks):
    """Top level resource of codenode.
    
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
            return (resource.IResource, r, r.logout) 
        r = RegularUserAvatar(self.nbSessionManager)
        return (resource.IResource, r, r.logout)






