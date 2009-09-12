import os

from zope.interface import implements 

from twisted.internet import defer
from twisted.web import xmlrpc
from twisted.web import resource
from twisted.web import server
from twisted.web.client import getPage
from twisted.python import log


from django.utils import simplejson as json

from codenode.frontend.notebook import models as nb_models
from codenode.frontend.backend import models as bkend_models

class EngineSession:
    """
    Engine Session. Client for interacting with backend engine.
    (Simple cache of parameters for communicating with backend process.)

    Translate notebook id to instance id.
    Keep current instance id in db. If it ever becomes invalid, replace it
    with the current valid instance.

    """

    def __init__(self, access_id, address):
        """
        """
        self.base_url = os.path.join(str(address), 'engine', str(access_id))

    @defer.inlineCallbacks
    def send(self, msg):
        """
        Send serialized JSON message to backend engine.
        """
        postdata = json.dumps(msg)
        result = yield getPage(self.base_url,
                        contextFactory=None,
                        method='POST',
                        postdata=postdata)
        defer.returnValue(result)



class BackendSessionManager(object):
    """
    Keep persistent web resource/rpc-clients, one per active
    notebook/engine.

    Keep track of EngineSessions by notebook id.
    Engine Sessions are inited with an engine type name and a possible 
    engine instance id.

    Engine Sessions are responsible for updating the engine instance id
    (which is updated when ever a new instance is created to replace the
    last instance).

    Engine Sessions are responsible for reporting errors:
     - Bad Engine Type, the current Engine Type does not exist on the
       backend
     - Instance Failure (can't start engine)
     - Instance Termination (instance died, possibly mid-evaluation)

    Engine Sessions keep track of last accessed time.
    Periodic watch dog scans for idle sessions and executes a clean-up
    operation governed by the users configuration/preference/etc.
     - remove front end session, kill backend instance
     - remove front end session, don't kill backend instance
     - don't remove front end session

    """

    sessionFactory = EngineSession

    def __init__(self):
        self.sessions = {}


    def getSession(self, notebook_id):
        """
        return session object
        """
        try:
            return self.sessions[notebook_id]
        except KeyError:
            return self.newSession(notebook_id)

    def newSession(self, notebook_id):
        """
        XXX figure out simpler efficient db query here
        """
        nb = nb_models.Notebook.objects.get(guid=notebook_id)
        nb_record = bkend_models.NotebookBackendRecord.objects.get(notebook=nb)
        address = nb_record.engine_type.backend.address
        access_id = nb_record.access_id
        sess = self.sessionFactory(access_id, address)
        self.sessions[notebook_id] = sess 
        return sess




class FrontendEngineBus(object):
    """
    """

    def __init__(self, backend_sessions):
        """
        The frontend bus forwards messages to the backend bus, and inspects
        the message to see if local action is required as well. 
        Messages from the client (javascript in browser) 

        XXX create common use cell save function in model so this can carry
        a simple convenience method for saving

        Mediates backend engine sessions with frontend data
        storing/retrieving. 
        """
        self.backend_sessions = backend_sessions

    def handleRequest(self, notebook_id, msg):
        """
        msg comes in as dictionary
        """
        engine_sess = self.backend_sessions.getSession(notebook_id)

        engine_method = str(msg['method'])
        d = engine_sess.send(msg)
        d.addErrback(self._backendErrback, notebook_id)

        if engine_method == 'evaluate':
            """Save result returned from backend 
            """
            d.addCallback(self._evaluateCallback, msg['cellid'])
            #self.saveCell(msg)
        if engine_method == 'complete':
            d.addCallback(self._competeCallback)

        return d

    def _evaluateCallback(self, result, cellid):
        """
        """
        log.msg('Engine result ', result)
        result = json.loads(result)
        count, out, err = result['input_count'], result['out'], result['err']
        output = out + err
        if "__image__" in output:
            output = output[9:] + err
            style = "outputimage"
        else:
            style = "outputtext"
        outcellid = cellid + "o" #denote an 'output' cell
        data = {'content':output, 'count':count, 'cellstyle':style, 'cellid':cellid}
        return data

    def _competeCallback(self, result):
        """
        """
        data = {'completions':result}
        return data

    def _backendErrback(self, reason, notebook_id):
        """
        """

    def saveCell(self, cell_data, notebook_id):
        """
        """



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
        else:
            return
        d = self.engine_bus.handleRequest(self.notebook_id, msg)
        d.addCallback(self._success, request)
        d.addErrback(self._fail, request)
        return server.NOT_DONE_YET

    def _success(self, data, request):
        jsobj = json.dumps(data)
        request.write(jsobj)
        request.finish()

    def _fail(self, reason, request):
        """
        """
        log.err(reason)
        request.write(str(reason))
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


















