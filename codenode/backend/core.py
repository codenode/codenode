######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

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

class InvalidEngineType(BackendError):
    """Invalid Name of Engine Type"""

class InvalidAccessId(BackendError):
    """Invalid Engine Access Id"""


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

    def newSession(self, engine_id, port, backend):
        """
        """
        sess = self.sessionFactory(port)
        sess.engine_id = engine_id
        sess.backend = backend
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
        log.msg('Allocated engine access id: %s for type: %s' % (access_id, engine_type,))
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
        #if self.engine_instances.has_key(access_id):
        #    return #access id already has engine, try terminating it
        try:
            engine_type = self.engine_allocations[access_id]
            log.msg('Running new engine type: %s for access id: %s' % (engine_type, access_id))
        except KeyError:
            log.err("Engine access_id %s NOT in engine_allocations" % access_id)
            raise InvalidAccessId("%s is not a valid access id" % access_id)
        try:
            engine_config = self.engine_types.get(engine_type)
            log.msg('engine config for type: %s  %s' % (engine_type, str(engine_config)))
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
        XXX added hack reference to processManager. Improve this next
        iteration.
        """
        return self.clientManager.newSession(engine_id, port, self)

    def _engineFailed(self, reason, engine_id):
        """
        """
        del self.engine_instances[engine_id]
        return reason

    def interruptEngine(self, engine_id):
        self.processManager.interruptProcess(engine_id)

    def stopEngine(self, engine_id):
        """XXX hacky. improve next iteration.
        """
        for access_id, v in self.engine_instances.iteritems():
            if engine_id == v:
                self.processManager.stopProcess(engine_id)
                del self.engine_instances[access_id]
                break

class EngineBus(object):
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
        log.msg('handling engine request for %s' % access_id)
        try:
            engine_client = yield self.backend.getEngine(access_id)
            log.msg('got engine Client %s' % str(engine_client))
        except InvalidAccessId:
            err = {'status':'ERR', 'response':'InvalidAccessId'}
            log.err('InvalidAccessId %s' % access_id)
            defer.returnValue(err)

        result = yield engine_client.send(msg)
        sucs = {'status':'OK', 'response':result}
        defer.returnValue(sucs)


class EngineSessionAdapter(resource.Resource):
    """
    There should be a better way to do this, have to figure that out.
    """

    def __init__(self, engine_bus, access_id):
        resource.Resource.__init__(self)
        self.engine_bus = engine_bus
        self.access_id = access_id

    def render(self, request):
        """
        This is where we un-serialize the content sent between the frontend
        and backend engine bus.
        """
        content = request.content.read()
        msg = json.loads(content)
        d = self.engine_bus.handleRequest(self.access_id, msg)
        d.addCallback(self._success, request)
        d.addErrback(self._fail, request)
        return server.NOT_DONE_YET

    def _success(self, result_ser, request):
        """
        XXX is result already serialized?
        """
        result = json.dumps(result_ser)
        request.write(result)
        request.finish()

    def _fail(self, reason, request):
        """
        """
        log.err('EngineSessionAdapter fail %s' % reason)
        result = json.dumps({'status':'ERR', 'response':str(reason)})
        request.write(result)
        request.finish()

class EngineBusAdapter(resource.Resource):

    def __init__(self, engine_bus):
        resource.Resource.__init__(self)
        self.engine_bus = engine_bus

    def getChild(self, path, request):
        """XXX Can this refer back to itself?
        """
        return EngineSessionAdapter(self.engine_bus, path)




