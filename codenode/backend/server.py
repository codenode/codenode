import os

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

    def xmlrpc_listEngineInstances(self):
        return self.backend.listEngineInstances()

    def xmlrpc_runEngineInstance(self, engine_type):
        return self.backend.runEngineInstance(engine_type)

    def xmlrpc_terminateInstance(self, engine_id):
        self.backend.terminateEngineInstance(engine_id)

    def xmlrpc_interruptInstance(self, engine_id):
        self.backend.interruptEngineIntance(engine_id)
        return


class BackendClient(resource.Resource):

    def __init__(self, backend):
        resource.Resource.__init__(self)
        self.backend = backend

        #self.putChild("RPC2", BackendClientRC(backend))
        self.putChild("", self)

    def getChild(self, path, request):
        engine = self.backend.getEngine(path)
        return BackendClientRC(engine)

    def render(self, request):
        return "backend client"

class BackendClientRC(xmlrpc.XMLRPC):

    def __init__(self, engine):
        xmlrpc.XMLRPC.__init__(self)
        #self.backend = backend
        #engine = backend.client_manager.getEngine(id)
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
        self.putChild("interpreter", BackendClient(backend))
        self.putChild("", self)

    def render(self, request):
        return 'backend root'


class BackendConfig(usage.Options):

    optParameters = [
            ['host', 'h', settings.BACKEND_HOST, 'Interface to listen on'],
            ['port', 'p', settings.BACKEND_PORT, 'Port number to listen on', int],
            ['env_path', 'e', os.path.abspath('.'), 'Codenode environment path'],
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
        client_manager = core.EngineProxyManager() #sessions
        client_manager.setServiceParent(backendServices)
        proc_manager = core.EngineManager()
        proc_manager.setServiceParent(backendServices)

        backend = core.Backend(proc_manager, client_manager)

        eng_proxy_factory = server.Site(BackendRoot(backend))
        internet.TCPServer(options['port'], eng_proxy_factory,
                interface=options['host']).setServiceParent(backendServices)
        return backendServices



