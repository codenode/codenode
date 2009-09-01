######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

import os

from twisted.internet import reactor
from twisted.spread import pb
from twisted.spread import flavors
from twisted.cred import credentials


class MindData(pb.Referenceable):

    def __init__(self, system, nbid, env_path):
        self.system = system
        self.nbid = nbid
        self.env_path = env_path

    def remote_getSystem(self):
        return self.system

    def remote_writeImage(self, image, image_name):
        """Remote method for saving images from the engine to the
        app-server file system.
        """
        image_path = os.path.join(self.env_path, 'images', image_name)
        f = file(image_path, 'w')
        f.write(image)
        f.close()
        return


class RemoteKernel:
    def __init__(self, system, nbid, host, port, env_path):
        system, nbid, host, port = map(str, [system, nbid, host, port])
        self.nbid = nbid
        self.system = system
        self.host = host
        self.port = port
        self.env_path = env_path
        self.remote = None
        self.mind = MindData(system, nbid, env_path)
        self.factory = pb.PBClientFactory()

    def connect(self):
        reactor.connectTCP(self.host, int(self.port), self.factory)
        d = self.factory.login(credentials.UsernamePassword(self.nbid, "secret"), 
                client=self.mind)
        return d.addCallback(self.connected)

    def connected(self, perspective):
        self.remote = perspective
        self.remote.notifyOnDisconnect(self._resetRemote)
        d = self.remote.callRemote('start', self.system)
        return d

    def callRemote(self, method, *args):
        if self.remote is None:
            d = self.connect()
            d.addCallback(lambda x: self._callRemote(method, *args))
            return d
        return self._callRemote(method, *args)

    def _callRemote(self, method, *args):
        return self.remote.callRemote(method, *args)

    def _resetRemote(self, r):
        self.remote = None

    def start(self):
        if self.remote is None:
            return self.connect()
        return 'on'

    def kill(self):
        d = self.callRemote('kill')
        d.addCallback(self._kill_callback)
        return d

    def _kill_callback(self, res):
        self.factory.disconnect()
        return res

    def interrupt(self):
        return self.callRemote('interrupt')

    def evaluate(self, input):
        #return self.remote.callRemote('eval', input)
        return self.callRemote('evaluate', input)

    def complete_name(self, input):
        #return self.remote.callRemote('complete_name', input)
        return self.callRemote('complete_name', input)

    def complete_attr(self, input):
        #return self.remote.callRemote('complete_attr', input)
        return self.callRemote('complete_attr', input)


class EngineFactory:

    engine = RemoteKernel

    def __init__(self):
        pass

    def newEngine(self, nbid, system, host, port, env_path):
        e = self.engine(system, nbid, host, port, env_path)
        return e



