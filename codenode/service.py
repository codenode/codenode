######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################
"""
codenode web and kernel services.

"""

import os
import commands

from zope.interface import implements

from codenode.external.twisted.web import server, resource, wsgi, static
from twisted.cred import portal, checkers, credentials
from twisted.internet import reactor, defer
from twisted.application import internet, service
from twisted.python import usage
from twisted.runner import procmon

from codenode.frontend.async import backend

import codenode
lib_path = codenode.__path__[0]

from django.conf import settings
VERSION = '0.2'



class DesktopOptions(usage.Options):
    """Main command line options for the desktop server.
     - host name
     - port number
     - proxy configuration
     - secure, use ssl

    """

    optParameters = [
            ['host', 'h', settings.APP_HOST, 'Host address to listen on'],
            ['port', 'p', settings.APP_PORT, 'Port number to listen on'],
            ['env_path', 'e', os.path.abspath('.'), 'Path to Codenode project dir'],
            ['server_log', None, os.path.join(os.path.abspath('.'), 'server.log'), 
                'log file for codenoded server'],
            ['static_files', None, os.path.join(lib_path, 'frontend', 'static'),
                'Path to static web application files'],
        ]

    optFlags = [
            ['devel_mode', 'd', 'Development mode'],
            ['open_browser', 'b', 'Automatically open web browser']
        ]


    def opt_version(self):
        print 'codenode Desktop version: %s' % VERSION
        sys.exit(0)

class FrontendOptions(usage.Options):
    """Main command line options for the app server.
     - host name
     - port number
     - proxy configuration
     - secure, use ssl

    """

    optParameters = [
            ['host', 'h', settings.APP_HOST, 'Host address to listen on'],
            ['port', 'p', settings.APP_PORT, 'Port number to listen on'],
            ['static_path', None, None, 'Static path for web server'],
            ['url_root', 'u', '/', 'Root url path for web server'],
            ['url_static_root', 's', '/', 'Static root url path for web server'],
            ['env_path', 'e', os.path.abspath('.'), 'Path to Codenode project dir'],
            ['server_log', None, os.path.join(os.path.abspath('.'), 'data', 'server.log'), 
                'log file for codenoded server'],
            ['static_files', None, os.path.join(os.path.abspath('.'), 'frontend', 'static'),
                'Path to static web application files'],
        ]

    optFlags = [
            ['proxy', 'r', 'Use in reverse proxy configuration'],
            ['devel_mode', 'd', 'Development mode'],
        ]


    def opt_version(self):
        print 'codenode WebApp version: %s' % VERSION
        sys.exit(0)




def webResourceFactory(staticfiles, datafiles):
    """This factory function creates an instance of the front end web
    resource tree containing both the django wsgi and the async
    notebook resources.
    """

    class Root(resource.Resource):

        def __init__(self, wsgi_resource):
            resource.Resource.__init__(self)
            self.wsgi_resource = wsgi_resource

        def getChild(self, path, request):
            path0 = request.prepath.pop(0)
            request.postpath.insert(0, path0)
            return self.wsgi_resource


    # The kernel server does not require django, so this step is not
    # required for every import of service.py (this file)
    from django.core.handlers.wsgi import WSGIHandler
    from twisted.python import threadpool

    pool = threadpool.ThreadPool()
    reactor.callWhenRunning(pool.start)
    reactor.addSystemEventTrigger('after', 'shutdown', pool.stop)

    django_wsgi_resource = wsgi.WSGIResource(reactor, pool, WSGIHandler())
    resource_root = Root(django_wsgi_resource)

    static_resource = static.File(staticfiles)
    data_resource = static.File(datafiles)

    backend_bus = backend.BackendBus()

    resource_root.putChild("asyncnotebook", backend.EngineBusAdapter(backend_bus))
    resource_root.putChild("static", static_resource)
    resource_root.putChild("data", data_resource)
    
    return resource_root

class BackendSupervisor(procmon.ProcessMonitor):
    """Quick fix hack until better process supervisor is
    implemented.
    """

    def startProcess(self, name):
        if self.protocols.has_key(name):
            return
        p = self.protocols[name] = procmon.LoggingProtocol()
        p.service = self
        p.name = name
        args, uid, gid = self.processes[name]
        self.timeStarted[name] = procmon.time.time()
        reactor.spawnProcess(p, args[0], args, env=None, uid=uid, gid=gid)



class DesktopServiceMaker(object):

    implements(service.IServiceMaker, service.IPlugin)
    tapname = "codenode"
    description = """A localhost only version for personal desktop-app-like usage."""
    options = DesktopOptions

    def makeService(self, options):
        """
        Return a service collection of two services.
        The web resource tree contains the wsgi interface to django and 
        the async notebook web resources.

        The process manager service will start the kernel server. 
        The kernel server process is another twistd plugin, and needs a 
        few options passed to it.  
        """
        from codenode.frontend.search import search
        search.create_index()

        desktop_service = service.MultiService()

        staticfiles = options['env_path'] + "/frontend/static" #XXX
        datafiles = options['env_path'] + "/data/plot_images" #XXX
        #Temporary hack
        if not os.path.exists(datafiles):
            os.mkdir(datafiles)
        web_resource = webResourceFactory(staticfiles, datafiles)
        serverlog = options['env_path'] + "/data/server.log" #XXX
        web_resource_factory = server.Site(web_resource, logPath=serverlog)

        tcp_server = internet.TCPServer(options['port'],
                                    web_resource_factory,
                                    interface='localhost')
        tcp_server.setServiceParent(desktop_service)

        ################################################
        # local backend server
        #
        twistd_bin = commands.getoutput('which twistd')
        backend_args = [twistd_bin, '-n',
                            '--pidfile', os.path.join(options['env_path'], 'backend.pid'),
                            'codenode-backend',
                            '--env_path', options['env_path']
                        ]
        backendSupervisor = BackendSupervisor()
        backendSupervisor.addProcess('backend', backend_args)
        backendSupervisor.setServiceParent(desktop_service)
        #
        ################################################

        return desktop_service


class FrontendServiceMaker(object):

    implements(service.IServiceMaker, service.IPlugin)
    tapname = "codenode-frontend"
    description = "Frontend Server"
    options = FrontendOptions

    def makeService(self, options):
        """
        This service is like the desktop, but is not responsible for
        controlling the kernel server process.
        """
        from codenode.frontend.search import search
        search.create_index()

        web_app_service = service.MultiService()

        if options['devel_mode']:
            staticfiles = os.path.join(lib_path, 'frontend', 'static')
        else:
            staticfiles = options['static_files']
        datafiles = options['env_path'] + "/data/plot_images" #XXX
        #Temporary hack
        if not os.path.exists(datafiles):
            os.mkdir(datafiles)
        web_resource = webResourceFactory(staticfiles, datafiles)
        serverlog = options['server_log']
        web_resource_factory = server.Site(web_resource, logPath=serverlog)

        frontend_server = internet.TCPServer(options['port'], 
                                    web_resource_factory, 
                                    interface=options['host'])
        frontend_server.setServiceParent(web_app_service)

        if options['devel_mode']:
            from twisted.conch.manhole import ColoredManhole
            from twisted.conch.insults import insults
            from twisted.conch.telnet import TelnetTransport, TelnetBootstrapProtocol
            from twisted.internet import protocol

            f = protocol.ServerFactory()
            f.protocol = lambda: TelnetTransport(TelnetBootstrapProtocol,
                                            insults.ServerProtocol,
                                            ColoredManhole, globals())
            telnel_manhole = internet.TCPServer(6023, f)
            telnel_manhole.setServiceParent(web_app_service)
        return web_app_service






