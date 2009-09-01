######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

from zope.interface import implements

from twisted.spread import pb
from twisted.cred import portal, checkers, credentials
from twisted.internet import reactor

from codenode.backend.kernel.interface import EngineManager

# what should this be called?
class KernelManagerRealm(object):

    implements(portal.IRealm)

    def __init__(self, config, procman, user_pool):
        self.config = config
        self.procman = procman
        self.user_pool = user_pool 

    def requestAvatar(self, avatarId, mind, *interfaces):
        """the avatar persists as long as the perspective connection stays
        alive. 
        """
        if pb.IPerspective not in interfaces:
            raise NotImplementedError
        avatar = EnginePerspective(avatarId, mind, self.config, self.procman, self.user_pool)
        return pb.IPerspective, avatar, lambda: None
        


class EnginePerspective(EngineManager, pb.Avatar):

    def perspective_start(self, system):
        return self.start(system)

    def perspective_stop(self):
        return self.stop()

    def perspective_kill(self):
        return self.kill()

    def perspective_interrupt(self):
        return self.interrupt()

    def perspective_evaluate(self, to_evaluate):
        return self.evaluate(to_evaluate)

    def perspective_complete_name(self, to_complete):
        return self.complete_name(to_complete)

    def perspective_complete_attr(self, to_complete):
        return self.complete_attr(to_complete)

    def perspective_introspect(self, to_introspect):
        return self.introspect(to_introspect)



