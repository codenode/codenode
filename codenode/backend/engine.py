######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

from zope.interface import Interface, implements

from twisted.web import xmlrpc
from twisted.plugin import IPlugin
from twisted.python import log
from twisted.internet import defer


class IEngineConfiguration(Interface):
    """Engine process plugin
    """

class EngineConfigurationBase(object):
    """
    Container of system specific configuration necessary and sufficient 
    to execute a program.

    The bin executable should be the interpreters bin file; it should not
    be a shell script wrapping/spawning another bin executable.  

    The recommended way to create an engine plugin is to create a subclass
    of this class with a name denoting the type of engine (e.g. Python). 

    @param args List of command line arguments passed to the bin
    @param env Environment variables.
    @param path Full path of directory to run the process in
    """

    implements(IPlugin, IEngineConfiguration)

    bin = '' #Full path of program to run
    args = [] #List of command line args to pass
    env = {} #Dictionary of environment variables
    path = '' #Directory to run process in

    def __init__(self):
        self.name = self.__class__.__name__

    def __repr__(self):
        """Name is used as the unique identifier.
        Make sure all engine plugins have unique class names.
        """
        return "%s" % self.name

    def __str__(self):
        return "%s engine: %s %s" % (self.name, self.bin, str(self.args))

class IEngine(Interface):
    """
    Client representing an engine.

    The result of a new Engine request.

    This is independent of the server protocol/transport.
    This is to be adapted to some kind of server.

    The methods of this api are the basic/fundamental ways to use the
    interpreter:
     - evaluate
     - complete
    """

    def evaluate(to_evaluate):
        """
        Evaluate arbitrary code @param to_evaluate

        return result as deferred
        """

    def complete(to_complete):
        """
        Get the list of possible completions from the current namespace or
        from an objects set of attributes.
        """



class EngineInstanceClient(object):
    """
    This does not properly implement IEngine yet.

    The context of the cellid is needed here still; this context should
    remain in the Frontend bus instead.
    """

    #implements(IEngine)
    
    def __init__(self, port):
        """
        """
        self.client = xmlrpc.Proxy("http://localhost:%s" % port)
        self.engine_id = ''
        self.backend = None

    def __str__(self):
        return 'Engine Client %s' % str(self.engine_id)

    def __repr__(self):
        return 'Engine Client %s' % str(self.engine_id)

    @defer.inlineCallbacks
    def send(self, msg):
        """simple version of general way to send something to the engine
        process. 
        """
        log.msg('Engine client send msg content: %s' % str(msg))
        engine_method = msg['method']
        log.msg('Engine method %s' % engine_method)
        engine_arg = msg.get('input', None)
        cellid = msg.get('cellid', None)
        try:
            log.msg('Getting engine method' + engine_method)
            meth = getattr(self, "engine_%s" % engine_method)
        except KeyError:
            log.err("Engine client has no method '%s'!" % (engine_method,))
            defer.returnValue({'result':'err'})
        result = yield meth(engine_arg, cellid)
        defer.returnValue(result)

    @defer.inlineCallbacks
    def engine_start(self, args, arg):
        """dummy
        """
        defer.returnValue({'result':'started'})


    @defer.inlineCallbacks
    def engine_evaluate(self, to_evaluate, cellid):
        """
        This makes the actual remote call. Possible to add hooks around
        this.
        return a Deferred
        """
        result = yield self.client.callRemote('evaluate', to_evaluate)
        defer.returnValue(result)

    @defer.inlineCallbacks
    def engine_complete(self, to_complete, cellid):
        """
        return a Deferred
        """
        result = yield self.client.callRemote('complete', to_complete)
        defer.returnValue(result)

    def engine_interrupt(self, a, b):
        self.backend.interruptEngine(self.engine_id)

    def engine_kill(self, a, b):
        self.backend.stopEngine(self.engine_id)


