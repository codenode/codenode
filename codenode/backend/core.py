
import sys
import time
import uuid

import simplejson as json

from signal import SIGINT

from twisted.python import log
from twisted.runner import procmon
from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet import protocol
from twisted.application import service
from twisted.application import internet
from twisted.plugin import getPlugins
from twisted.web import resource
from twisted.web import server

from zope.interface import Interface, implements

from codenode.backend.engine import EngineInstanceClient
from codenode.backend.engine import IEngineConfiguration

class BackendError(Exception):
    """Invalid backend operation...
    """


class EngineProcessProtocol(protocol.ProcessProtocol):

    def __init__(self):
        self.deferred = defer.Deferred()

    def connectionMade(self):
        """This call means the process has started, but not the
        interpreter, yet.
        """

    def outReceived(self, data):
        """Simple protocol for the interpreter to notify us when it is
        really running.
        """
        if data[0:4] == "port":
            port = data.split(':')[1]
            self.deferred.callback(port)
    
    def errReceived(self, data):
        """
        """
        log.msg("Engine error", data)

    def interrupt(self):
        self.transport.signalProcess(SIGINT)

class EngineProcessManager(procmon.ProcessMonitor):

    engineProtocol = EngineProcessProtocol
    START_TIMEOUT = 60 #seconds

    def __init__(self):
        procmon.ProcessMonitor.__init__(self)

    def addProcess(self, name, proc_config):
        """
        proc_config is an object implementing IEngineConfiguration
        """
        if self.processes.has_key(name):
            raise KeyError("remove %s first" % name)
        p = self.engineProtocol()
        p.service = self
        p.name = name
        proc_config.processProtocol = p
        self.processes[name] = proc_config
        if self.active:
            self.startProcess(name)
        return p.deferred

    def startProcess(self, name):
        """
        """
        if self.protocols.has_key(name):
            return
        p_conf = self.processes[name]
        p = self.protocols[name] = p_conf.processProtocol
        bin = p_conf.bin
        args = [bin] + p_conf.args
        env = p_conf.env
        path = p_conf.path
        self.timeStarted[name] = time.time()
        p.deferred.setTimeout(self.START_TIMEOUT)
        reactor.spawnProcess(p, bin, args=args, env=env, path=path)

    def interruptProcess(self, name):
        """Send INT signal.
        """
        if not self.protocols.has_key(name):
            raise KeyError("No process named %s" % name)
        self.protocols[name].interrupt()


class EngineClientManager(service.Service):
    """
    """

    sessionFactory = EngineInstanceClient

    def __init__(self):
        self.sessions = {}

    def getSession(self, engine_id):
        """
        """
        try:
            return self.sessions[engine_id]
        except KeyError:
            return None#raise?

    def newSession(self, engine_id, port):
        """
        """
        sess = self.sessionFactory(port)
        self.sessions[engine_id] = sess
        return sess

    def removeSession(self, engine_id):
        """
        """


class Backend(service.Service):
    """
    Application level interface for managing, controlling, and accessing
    engine/engine processes.

    This class/service delegates to a processes manager and a
    client-session manager.

    The processes manager knows how to deal with engine processes (os
    processes).

    The client-session manager knows how to communicate with the
    interpreter of the engine processes, and is the place to implement
    protocol parsing/formating outside of the interpreter but before the
    transport.
    """

    def __init__(self, processManager, clientManager):
        """
        processManager manages os processes
        clientManager manages engine client-sessions

        engine_types dict name: config_object
        engine_allocations dict access_id:engine_type
        engine_instances dict access_id:engine_id
        """
        self.processManager = processManager
        self.clientManager = clientManager
        self.engine_types = {}
        self.engine_allocations = {}
        self.engine_instances = {}

    def updateEngineTypes(self):
        engines = getPlugins(IEngineConfiguration)
        self.engine_types = dict([(repr(e), e) for e in engines])

    def listEngineTypes(self):
        self.updateEngineTypes() # change this to a periodic update?
        types = self.engine_types.keys()
        log.msg(types)
        return types

    def listEngineInstances(self):
        return self.processManager.processes.keys()

    def allocateEngine(self, engine_type):
        """Create a new access id for running engines of given type.
        return access_id
        """
        if engine_type not in self.engine_types.keys():
            raise KeyError("%s is not a recognized engine type" % engine_type)
        access_id = uuid.uuid4().hex
        self.engine_allocations[access_id] = engine_type
        return access_id

    def getEngine(self, access_id):
        """Get an engine client
        return deferred
        """
        try:
            engine_id = self.engine_instances[access_id]
        except KeyError:
            return self.runEngine(access_id)
        return defer.maybeDeferred(self.clientManager.getSession, engine_id)

    def runEngine(self, access_id):
        """
        """
        if self.engine_instances.has_key(access_id):
            return #access id already has engine, try terminating it
        try:
            engine_type = self.engine_allocations.get(access_id)
        except KeyError:
            log.err("Engine access_id %s NOT in engine_allocations" % access_id)
            raise BackendError("%s is not a valid access id" % access_id)
        try:
            engine_config = self.engine_types.get(engine_type)
        except KeyError:
            log.err("Engine Type %s not in engine_types (was the engine plugin moved?)" % engine_type)
        engine_id = uuid.uuid4().hex
        self.engine_instances[access_id] = engine_id
        d = self.processManager.addProcess(engine_id, engine_config)
        d.addCallback(self._newClientSession, engine_id)
        d.addErrback(self._engineFailed, engine_id)
        return d

    def _newClientSession(self, port, engine_id):
        """
        """
        return self.clientManager.newSession(engine_id, port)

    def _engineFailed(self, reason, engine_id):
        """
        """
        del self.engine_instances[engine_id]
        return reason



class BackendEngineBus(object):
    """
    Common entry point for all engine requests. 
    Look up engine client by access_id.

    This is responsible for routing the engine message
    from the browser/frontend to the engine by access_id.
    This does not need to process the message (un-serialize, inspect, 
    or otherwise).
    """

    def __init__(self, backend):
        self.backend = backend

    @defer.inlineCallbacks
    def handleRequest(self, access_id, msg):
        """
        msg comes in as dictionary
        """
        engine_client = yield self.backend.getEngine(access_id)
        engine_method = msg.get('method')
        engine_arg = msg.get('input')

        try:
            log.msg('Getting engine method' + engine_method)
            meth = getattr(engine_client, "engine_%s" % (engine_method,))
        except KeyError:
            log.err("Engine client has no method '%s'!" % (engine_method,))
            # return an error code
        # best way to return deferred??
        result = yield meth(engine_arg)
        json_obj = json.dumps(result)
        defer.returnValue(json_obj)




