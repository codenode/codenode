
import sys
import time
import uuid

from signal import SIGINT

from twisted.python import log
from twisted.runner import procmon
from twisted.internet import defer
from twisted.internet import reactor
from twisted.application import service
from twisted.application import internet
from twisted.plugin import getPlugins
from twisted.web import xmlrpc
from twisted.web import resource
from twisted.web import server

from zope.interface import Interface, implements

from codenode.backend.engine import Engine
from codenode.backend.engine import IEngineConfiguration

class EngineProcessLogger(procmon.LoggingProtocol):

    deferred = None

    def connectionMade(self):
        procmon.LoggingProtocol.connectionMade(self)

    def outReceived(self, data):
        procmon.LoggingProtocol.outReceived(self, data)
        if data[0:4] == "port":
            port = data.split(':')[1]
            self.deferred.callback(port)

    def interrupt(self):
        self.transport.signalProcess(SIGINT)

class EngineManager(procmon.ProcessMonitor):

    start_deferreds = {}

    def addProcess(self, name, proc_config):
        """
        """
        if self.processes.has_key(name):
            raise KeyError("remove %s first" % name)
        self.processes[name] = proc_config
        d = defer.Deferred()
        self.start_deferreds[name] = d
        if self.active:
            self.startProcess(name)
        return d

    def startProcess(self, name):
        """
        """
        if self.protocols.has_key(name):
            return
        p = self.protocols[name] = EngineProcessLogger()
        p.service = self
        p.name = name
        d = self.start_deferreds[name]
        del self.start_deferreds[name]
        p.deferred = d
        p_conf = self.processes[name]
        bin = p_conf.bin
        args = [bin] + p_conf.args
        env = p_conf.env
        path = p_conf.path
        self.timeStarted[name] = time.time()
        reactor.spawnProcess(p, bin, args=args, env=env, path=path)

    def interruptProcess(self, name):
        """Send INT signal.
        """
        if not self.protocols.has_key(name):
            raise KeyError("No process named %s", % name)
        self.protocols[name].interrupt()


class EngineProxyManager(service.Service):
    """
    Manages engine clients.

    Like a session manager.

    Store Engine clients by id 
    """

    def __init__(self):
        self.engines = {}

    def getEngine(self, engine_id):
        if not self.engines.has_key(engine_id):
            raise KeyError("Bad engine client id: %s" % engine_id)
        return self.engines[engine_id]

    def addEngine(self, engine):
        self.engines[engine.id] = engine

    def removeEngine(self, engine_id):
        if not self.engines.has_key(engine_id):
            raise KeyError("Engine client %s does not exist" % engine_id)
        del self.engines[engine_id]




def _start_client(port):
    c = Engine(port)
    #c.test
    return

def _fail(reason):
    print reason
    return reason

class IBackend(Interface):

    def listEngineTypes(self):
        """Return a list of the types of Engines registered with the backend. 
        """

    def listEngineInstances(self):
        """Return a list of all running Engine instances.
        """

    def runEngineInstance(self, engine_type):
        """Instantiate an Engine type.
        This spawns an Engine Process, and upon success of that, creates an
        Engine Client/Proxy instance.
        """

    def restartEngineInstance(self, engine_id):
        """Restart an Engine process. 
        This says nothing about persistence of state/namespace
        @todo Formalize implications of persistence.
        """

    def terminateEngineInstance(self, engine_id):
        """Kill an Engine process.
        This says nothing about persistence of state/namespace
        @todo Formalize implications of persistence.
        """

class Backend:
    """
    Backend service.

    Provides an api for managing engine processes and proxying engine
    interpreter interface

    A frontend can use a transport to 
     - connect, 
     - query the list of engine plugins, 
     - query the list of running engine instances.
    A notebook/user makes 
     - requests to running engine interpreter (api) (routed by engine instance name)
     - requests to start/stop engines (by engine type)
    """

    def __init__(self, pm, cm):
        self.client_manager = cm
        self.process_manager = pm
        self.engine_types = {}
        self.updateEngineTypes()

    def listEngineTypes(self):
        return self.engine_types.keys()

    def updateEngineTypes(self):
        engines = getPlugins(IEngineConfiguration)
        self.engine_types = dict([(repr(e), e) for e in engines])

    def listEngineInstances(self):
        insts = self.process_manager.processes.keys()


    def runEngineInstance(self, engine_type):
        """
        Create an engine process with a unique id.
        When the process is running, create a client service object to
        handle requests 

        return unique id of engine instance to be used by the notebook/user
        for interactive requests.
        """
        print 'newEngine'
        if engine_type not in self.engine_types.keys():
            raise KeyError("%s not an engine type" % engine_type)
        engine_config = self.engine_types[engine_type]
        id = uuid.uuid4().hex
        d = self.process_manager.addProcess(id, engine_config)
        d.addCallback(self._start_client, id)
        d.addErrback(_fail)
        return d

    def _start_client(self, port, id):
        print '_start_client', port, id
        c = Engine(port, id)
        self.client_manager.addEngine(c)
        return id

    def terminateEngineInstance(self, engine_id):
        """Stop an engine instance.
        """
        self.proc_manager.stopProcess(engine_id)
        self.client_manager.removeEngine(engine_id)

    def interruptEngineIntance(self, engine_id):
        """Send process SIGINT
        """
        self.proc_manager.interruptProcess(engine_id)


class BackendAdmin(resource.Resource):
    
    def __init__(self, backend):
        resource.Resource.__init__(self)
        self.backend = backend

        self.putChild("RPC2", BackendAdminRC(backend))
        self.putChild("", self)

    def render(self, request):
        """
        """
        return 'backend admin'

class BackendAdminRC(xmlrpc.XMLRPC):

    def __init__(self, backend):
        xmlrpc.XMLRPC.__init__(self)
        self.backend = backend

    def xmlrpc_getEngineTypes(self):
        return self.backend.getEngineTypes()

    @defer.inlineCallbacks
    def xmlrpc_newEngine(self, engine_type):
        d = self.backend.newEngine(engine_type)
        res = yield d
        print 'rpc newengine', res
        defer.returnValue(res)
        

class BackendClient(resource.Resource):

    def __init__(self, backend):
        resource.Resource.__init__(self)
        self.backend = backend

        #self.putChild("RPC2", BackendClientRC(backend))
        self.putChild("", self)

    def getChild(self, path, request):
        return BackendClientRC(self.backend, path)

    def render(self, request):
        return "backend client"

class BackendClientRC(xmlrpc.XMLRPC):

    def __init__(self, backend, id):
        xmlrpc.XMLRPC.__init__(self)
        self.backend = backend
        engine = backend.client_manager.getEngine(id)
        self.engine = engine

    def xmlrpc_evaluate(self, to_evaluate):
        return self.engine.evaluate(to_evaluate)

    def xmlrpc_complete(self, to_complete):
        return self.engine.complete(to_complete)

class BackendRoot(resource.Resource):

    def __init__(self, backend):
        resource.Resource.__init__(self)
        self.backend = backend

        self.putChild("admin", BackendAdmin(backend))
        self.putChild("client", BackendClient(backend))
        self.putChild("", self)

    def render(self, request):
        return 'backend root'

def makeServices():

    backendServices = service.MultiService()
    client_manager = EngineProxyManager() #sessions
    client_manager.setServiceParent(backendServices)
    proc_manager = EngineManager()
    proc_manager.setServiceParent(backendServices)

    backend = Backend(proc_manager, client_manager)

    eng_proxy_factory = server.Site(BackendRoot(backend))
    internet.TCPServer(9001, eng_proxy_factory).setServiceParent(backendServices)
    return backendServices



