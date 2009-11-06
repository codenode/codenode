######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################
import os
import uuid
import pickle
#from StringIO import StringIO

from zope.interface import implements 

from twisted.internet import defer
from twisted.web import xmlrpc
from twisted.web import resource
from twisted.web import server
from twisted.web.client import getPage
from twisted.python import log


from django.utils import simplejson as json

from django.conf import settings

from codenode.frontend.notebook import models as notebook_models

def write_image(image):
    fn = str(uuid.uuid4()) + '.png'
    fullpath = os.path.join(settings.PLOT_IMAGES, fn)
    f = open(fullpath, 'w')
    f.write(image)
    f.close()
    return fn


class BackendAdmin:
    """
    This is a base/mix in class for conveniently admin related requests
    (not specific to an engine). These functions still use the rpc client
    instead of the web client. The usage of both clients is kind of an
    experiment still, but the main reason is that the admin client is for
    making specific method calls on the backend. Engine requests are
    (ideally) just passed along to the engine with out inspecting the
    details (which method, etc.); in practice the requests are still
    inspected though, so the natural seam between these interactions hasn't
    fully revealed itself yet...
    """

    @defer.inlineCallbacks
    def newAccessId(self, engine_type):
        """
        Backend administrative call.
        """
        url = os.path.join(self.base_url, 'admin', '')
        client = xmlrpc.Proxy(url)
        access_id = yield client.callRemote('allocateEngine', str(engine_type))
        defer.returnValue(access_id)


class BackendClient(object, BackendAdmin):
    """
    Has address to use for all requests.
    """

    def __init__(self, address):
        """
        """
        self.base_url = str(address)

    def __repr__(self):
        return 'BackendClient("%s")' % self.base_url

    def __str__(self):
        return 'BackendClient @ %s)' % self.base_url

    @defer.inlineCallbacks
    def _send(self, access_id, msg):
        """
        Send to backend engine.
        """
        url = os.path.join(self.base_url, 'engine', str(access_id))
        result = yield getPage(url,
                        contextFactory=None,
                        method='POST',
                        postdata=str(msg))
        defer.returnValue(result)

    @defer.inlineCallbacks
    def send(self, access_id, msg):
        """
        Use JSON for serialization.
        """
        ser_msg = json.dumps(msg)
        log.msg('to _send: %s' % ser_msg)
        result_ser = yield self._send(access_id, ser_msg)
        result = json.loads(result_ser)
        defer.returnValue(result)


class BackendBus(object):
    """
    This holds on to backend clients (which cache backend address).

    The context coming in is the notebook id. Look up the backend to pass
    message to; create backend if one does not exist yet.

    In comes browser to frontend bus message.

    Message has method attribute in header. Depending on this method, route
    message to appropriate component.

    Handle response from backend client.
    - OK, rely response
    - ERR, check reason, take correcting action, or propagate error

    backends dict of backend_name to backend_client instance
    notebook_map dict of notebook_id to (backend, access_id,)
    """

    backendFactory = BackendClient

    def __init__(self):
        """
        """
        self.backends = {}
        self.notebook_map = {}

    def addBackend(self, backend_name, backend_address):
        """
        """
        backend = self.backendFactory(backend_address)
        self.backends[backend_name] = backend
        return backend

    def addNotebook(self, notebook_id):
        """
        """
        nb = notebook_models.Notebook.objects.get(guid=notebook_id)
        access_id = nb.backend.all()[0].access_id
        backend_name = nb.backend.all()[0].engine_type.backend.name
        try:
            backend = self.backends[backend_name]
        except KeyError:
            backend_address = nb.backend.all()[0].engine_type.backend.address
            backend = self.addBackend(backend_name, backend_address)
        # check key d n e
        self.notebook_map[notebook_id] = (backend, access_id,)
        return (backend, access_id,)

    @defer.inlineCallbacks
    def handleRequest(self, notebook_id, msg):
        """
        """
        try:
            backend, access_id = self.notebook_map[notebook_id]
        except KeyError:
            backend, access_id = self.addNotebook(notebook_id)
        log.msg('notebooks backend: %s' % backend)
        result = yield backend.send(access_id, msg)
        status = result['status']
        if status == 'OK':
            defer.returnValue(result['response'])
        if status == 'ERR':
            """check error"""
            log.err('Backend error %s' % str(result['response']))
            err = result['response']
            if err == 'InvalidAccessId':
                #self.reset_access_id(self, notebook_id)
                nb = notebook_models.Notebook.objects.get(guid=notebook_id)
                engine_type = str(nb.backend.all()[0].engine_type.name)
                new_access_id = yield backend.newAccessId(engine_type)
                nb.backend.all()[0].access_id = new_access_id
                nb.save()
                self.notebook_map[notebook_id] = (backend, new_access_id,)
                result_retry = yield backend.send(new_access_id, msg)
                status = result_retry['status']
                # TODO: Better handling. return no matter what for now
                defer.returnValue(result_retry['response'])



class EngineSessionAdapter(resource.Resource):
    """
    There should be a better way to do this, have to figure that out.
    """

    isLeaf = True

    def __init__(self, engine_bus, notebook_id):
        resource.Resource.__init__(self)
        self.engine_bus = engine_bus
        self.notebook_id = notebook_id
        self.putChild("", self)

    def render(self, request):
        """
        This is where we un-serialize the content sent between the frontend
        and backend engine bus.
        """
        content = request.content.read()
        if content:
            msg = json.loads(content)
            log.msg('Engine message deserialized %s' % str(msg))
        else:
            return
        cellid = msg.get('cellid', '')
        d = self.engine_bus.handleRequest(self.notebook_id, msg)
        d.addCallback(self._success, request, cellid)
        d.addErrback(self._fail, request)
        return server.NOT_DONE_YET

    def _success(self, data, request, cellid):
        """
        horrible. not always eval...
        """
        out = data['out']
        if type(out) is str:
            if out.startswith("__imagefile__"):
                image_pick = out[13:]
                image_io = pickle.loads(image_pick)
                image = image_io.getvalue()
                image_file_name = write_image(image)
                data['out'] = image_file_name
                data['cellstyle'] = 'outputimage'
            else:
                data['cellstyle'] = 'outputtext'
        data['cellid'] = cellid
        jsobj = json.dumps(data)
        request.write(jsobj)
        request.finish()

    def _fail(self, reason, request):
        """
        Add conditional to return real traceback...only do it if
        settings.DEBUG is true, or something.
        """
        log.err(reason)
        if settings.DEBUG:
            request.write(str(reason))
        else:
            request.write('err') #XXX improve error handling
        request.finish()

class EngineBusAdapter(resource.Resource):

    def __init__(self, engine_bus):
        resource.Resource.__init__(self)
        self.engine_bus = engine_bus
        self.putChild("", self)

    def getChild(self, path, request):
        """XXX Can this refer back to itself?
        """
        return EngineSessionAdapter(self.engine_bus, path)



