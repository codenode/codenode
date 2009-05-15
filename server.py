import sys
import os

from twisted.application import internet, service
from twisted.web import server, proxy, resource, wsgi, static
from twisted.python import threadpool
from twisted.internet import reactor

sys.path.append("knoboo")
os.environ['DJANGO_SETTINGS_MODULE'] = 'knoboo.settings'

from django.core.handlers.wsgi import WSGIHandler


from knoboo import main

class Root(resource.Resource):

    def __init__(self, wsgi_resource):
        resource.Resource.__init__(self)
        self.wsgi_resource = wsgi_resource

    def getChild(self, path, request):
        path0 = request.prepath.pop(0)
        request.postpath.insert(0, path0)
        return self.wsgi_resource

def wsgi_resource():
    pool = threadpool.ThreadPool()
    pool.start()
    reactor.addSystemEventTrigger('after', 'shutdown', pool.stop)
    wsgi_resource = wsgi.WSGIResource(reactor, pool, WSGIHandler())
    return wsgi_resource


application = service.Application('codenode')

wsgi_root = wsgi_resource()
root = Root(wsgi_root)

kernel = main.webService()
root.putChild("asyncnotebook", kernel)

staticrsrc = static.File(os.path.abspath(".")+"/knoboo/static")
root.putChild("static", staticrsrc)

main_site = server.Site(root)
internet.TCPServer(8000, main_site).setServiceParent(application)
