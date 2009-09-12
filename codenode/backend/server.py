import os

# Which json lib to use?
import simplejson as json

from twisted.python import log
from twisted.python import usage
from twisted.internet import defer
from twisted.internet import reactor
from twisted.application import service
from twisted.application import internet
from twisted.web import xmlrpc
from twisted.web import resource
from twisted.web import server

from zope.interface import Interface, implements

from codenode.backend import core

from codenode.backend import _settings as settings

BACKEND_VERSION = '0.2'

class BackendAdmin(resource.Resource):
    
    def __init__(self, backend):
        resource.Resource.__init__(self)
        self.backend = backend

        self.putChild("", BackendAdminRC(backend))

    def render(self, request):
        """
        """
        return 'backend admin'

class BackendAdminRC(xmlrpc.XMLRPC):

    def __init__(self, backend):
        xmlrpc.XMLRPC.__init__(self)
        self.backend = backend

    def xmlrpc_listEngineTypes(self):
        return self.backend.listEngineTypes()

    def xmlrpc_allocateEngine(self, engine_type):
        return self.backend.allocateEngine(engine_type)

    def xmlrpc_listEngineInstances(self):
        return self.backend.listEngineInstances()

    def xmlrpc_terminateInstance(self, engine_id):
        self.backend.terminateEngineInstance(engine_id)
        return

    def xmlrpc_interruptInstance(self, engine_id):
        self.backend.interruptEngineIntance(engine_id)
        return

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

    def _success(self, result, request):
        """
        XXX is result already serialized?
        """
        request.write(result)
        request.finish()

    def _fail(self, reason, request):
        """
        """
        request.write(str(reason))
        request.finish()

class EngineBusAdapter(resource.Resource):

    def __init__(self, engine_bus):
        resource.Resource.__init__(self)
        self.engine_bus = engine_bus

    def getChild(self, path, request):
        """XXX Can this refer back to itself?
        """
        return EngineSessionAdapter(self.engine_bus, path)


class BackendRoot(resource.Resource):

    def __init__(self, backend, engine_bus):
        resource.Resource.__init__(self)
        self.backend = backend

        self.putChild("admin", BackendAdmin(backend))
        self.putChild("engine", EngineBusAdapter(engine_bus))
        self.putChild("", self)

    def render(self, request):
        return 'backend root'


class BackendConfig(usage.Options):

    optParameters = [
            ['host', 'h', settings.BACKEND_HOST, 'Interface to listen on'],
            ['port', 'p', settings.BACKEND_PORT, 'Port number to listen on', int],
            ['env_path', 'e', os.path.abspath('.'), 'Codenode environment path'],
            ]

    optFlags = [
            ['devel_mode', 'd', 'Development mode'],
            ]

    def opt_version(self):
        print 'codenode backend version: %s' % BACKEND_VERSION
        sys.exit(0)

class BackendServerServiceMaker(object):

    implements(service.IServiceMaker, service.IPlugin)
    tapname = "codenode-backend"
    description = "Backend server"
    options = BackendConfig

    def makeService(self, options):

        backendServices = service.MultiService()

        clientManager = core.EngineClientManager() #sessions
        clientManager.setServiceParent(backendServices)

        processManager = core.EngineProcessManager()
        processManager.setServiceParent(backendServices)

        backend = core.Backend(processManager, clientManager)
        backend.updateEngineTypes()

        backendEngineBus = core.BackendEngineBus(backend)

        eng_proxy_factory = server.Site(BackendRoot(backend,
            backendEngineBus))
        internet.TCPServer(options['port'], eng_proxy_factory,
                interface=options['host']).setServiceParent(backendServices)

        if options['devel_mode']:
            from twisted.conch.manhole import ColoredManhole
            from twisted.conch.insults import insults
            from twisted.conch.telnet import TelnetTransport, TelnetBootstrapProtocol
            from twisted.internet import protocol

            f = protocol.ServerFactory()
            f.protocol = lambda: TelnetTransport(TelnetBootstrapProtocol,
                                            insults.ServerProtocol,
                                            ColoredManhole, globals())
            telnel_manhole = internet.TCPServer(6024, f)
            telnel_manhole.setServiceParent(backendServices)

        return backendServices



