######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

import os

from twisted.internet import defer

from codenode.external.twisted.web import server, resource

from codenode.external import simplejson as json

from codenode.backend.kernel import remoteclient  
from codenode.backend.kernel import appengineclient  
from codenode.printing import printers

from codenode.frontend.async import dbmanager

from django.conf import settings


class Notebook(resource.Resource):
    """Children of this Resource handle requests for a given Notebook.
  
    If an operation is requested, then check for the exstince of the
    operations resource tree stored in the notebook sessions manager.
    Create one if one does not exist.
    """
    isLeaf = False

    def __init__(self, nbSessionManager): 
        resource.Resource.__init__(self)
        self.nbSessionManager = nbSessionManager

    def getChild(self, path, request):
        """Pass off request to children for a given notebook.

        Important: The 'path' is the Notebook Id.
        """
        rsrc = self.nbSessionManager.getSession(path)
        return rsrc.children[path]

    def render_GET(self, request):
        return "Top level Notebook Resource.  All methods are children of this Resource."


class EngineMethod(resource.Resource):
    """Resource wrapper around an actual engine method.

    """

    def __init__(self, notebook_db, engine=None):
        self.notebook_db = notebook_db
        self.engine = engine


class EngineSession(resource.Resource):
    """Parent resource of computation engine operations.

    This resource tree has access to a computation engine 
    for the notebook session.
    """

    isLeaf = False

    def __init__(self, nbid, notebook_db, engine, env_path): 
        resource.Resource.__init__(self)
        self.nbid = nbid
        self.notebook_db = notebook_db
        self.engine = engine
        self.putChild(nbid, NotebookRoot(nbid, notebook_db, engine, env_path))

class SessionManager(object):

    _engineFactory = remoteclient.EngineFactory

    def __init__(self, options):
        """store notebook operations resources by nbid
        """
        self.engineFactory = self._engineFactory()
        self.sessions = {}
        self.options = options

    def newSession(self, nbid):
        """return a new resource tree
        """
        notebook_db = dbmanager.NotebookSession(nbid)
        kernel_host = settings.KERNEL_HOST
        kernel_port = settings.KERNEL_PORT
        env_path = settings.ENV_PATH
        system = notebook_db.getSystem()
        engine = self.engineFactory.newEngine(nbid, system, kernel_host, kernel_port, env_path)
        self.sessions[nbid] = EngineSession(nbid, notebook_db, engine, env_path)
        return self.sessions[nbid]
        
    def getSession(self, nbid):
        """Get a notebook resource tree by id if it exists.
        If it does not, create a new session.
        """
        try:
            return self.sessions[nbid]
        except KeyError:
            return self.newSession(nbid)

    def endSession(self, nbid):
        """end session by terminating engine process and notebook db
        session.
        """
        try:
            self.sessions[nbid].engine.kill()
            del self.sessions[nbid]
        except KeyError:
            pass

    def endAllSessions(self):
        for nbid, ses in self.sessions.items():
            self.endSession(nbid)

class AppEngineSessionManager(SessionManager):
    """Hack until notebook service is improved
    """

    _engineFactory = appengineclient.EngineFactory

    def newSession(self, nbid):
        notebook_db = dbmanager.NotebookSession(nbid)
        kernel_host = self.options['kernel_host']
        kernel_port = self.options['kernel_port']
        env_path = settings.ENV_PATH
        system = notebook_db.getSystem()
        engine = self.engineFactory.newEngine(kernel_host+':'+str(kernel_port))
        self.sessions[nbid] = EngineSession(nbid, notebook_db, engine, env_path)
        return self.sessions[nbid]
        

class NotebookRoot(resource.Resource):

    isLeaf = False

    def __init__(self, nbid, notebook_db, engine, env_path):
        resource.Resource.__init__(self)
        self.nbid = nbid
        self.notebook_db = notebook_db
        self.putChild("start", StartEngine(notebook_db, engine))
        self.putChild("nbobject", NotebookObject(notebook_db))
        self.putChild("save", SaveNotebookMetaData(notebook_db))
        self.putChild("delete", DeleteCell(notebook_db, engine))
        self.putChild("change", ChangeNotebookMetaData(notebook_db, engine))
        self.putChild("eval", Evaluate(notebook_db, engine))
        self.putChild("completer", Completer(notebook_db, engine))
        self.putChild("kernel", Control(notebook_db, engine))
        #XXX self.putChild("print", Print(notebook_db, env_path))

    def render(self, request):
        nb = self.notebook_db.get_notebook()
        title = nb.title
        system = nb.system
        #html = templates.notebook(nb.owner, title, system).encode("utf-8")
        return self.__class__.__name__

class StartEngine(EngineMethod):
    """Start the notebooks computation process.

    Trigger the actual process that the notebook's 
    computations will run it to start up.

    The method '_started_yet' calls 'start' until the
    computation process responds with 'on' before
    it finishes the response.
    """

    def render(self, request):
        d = defer.maybeDeferred(self.engine.start)
        d.addCallback(self._success, request)
        d.addErrback(self._failure, request)
        return server.NOT_DONE_YET


    def _success(self, result, request):
        request.setHeader("content-type", "application/json")
        request.write('ok')
        request.finish()

    def _failure(self, result, request):
        request.setHeader("content-type", "application/json")
        request.write('failed')
        request.finish()


class NotebookObject(EngineMethod):
    """Get Notebook json object.
    """

    # @defer.inlineCallbacks
    def render(self, request):
        d = defer.maybeDeferred(self.notebook_db.get_notebook_data)
        d.addCallback(self._success, request)
        d.addErrback(self._failure, request)
        return server.NOT_DONE_YET
        """
        result = yield defer.maybeDeferred(self.notebook_db.get_notebook_data)
        jsobj = json.dumps(result)
        request.setHeader("content-type", "application/json")
        request.write(jsobj)
        request.finish()
        """

    def _success(self, result, request):
        request.setHeader("content-type", "application/json")
        jsobj = json.dumps(result)
        request.write(jsobj)
        request.finish()

    def _failure(self, result, request):
        request.setHeader("content-type", "application/json")
        request.write('failed')
        request.finish()



class SaveNotebookMetaData(EngineMethod):
    """Save non cell data from a notebook to the database.

    This is a resource used from an async call to '/bookshelf/save'
    to save data associated with a notebook.
    """
    def render(self, request):
        orderlist = ",".join(request.args.get('orderlist', []))
        cellsdata = request.args.get('cellsdata', [None])[0]
        cellsdata = json.loads(cellsdata)
        d = defer.maybeDeferred(self.notebook_db.save_notebook_metadata, orderlist, cellsdata)
        d.addCallback(self._success, request) 
        return server.NOT_DONE_YET

    def _success(self, result, request):
        resp = "{'resource':'%s', 'resp':'ok'}" % self.__class__.__name__
        jsobj = json.dumps(resp)
        request.setHeader("content-type", "application/json")
        request.write(jsobj)
        request.finish()

class DeleteCell(EngineMethod):
    """Delete cells from the database.

    Take a list of cellids, and deleted all 
    data associated with the cellid.
    """

    @defer.inlineCallbacks
    def render(self, req): 
        """
        Delete one or more cells.
        """
        #XXX untested - javascript doesn't work right now to delete a cell?
        cellids = json.loads(req.args.get('cellids', [None])[0])
        result = yield defer.maybeDeferred(self.notebook_db.delete_cells, cellids)
        resp = "{'resource':'%s', 'resp':'ok'}" % self.__class__.__name__
        jsobj = json.dumps(resp)
        request.setHeader("content-type", "application/json")
        request.write(jsobj)
        request.finish()


class ChangeNotebookMetaData(EngineMethod):
    """Change notebook title ... could be more general.
    """

    # @defer.inlineCallbacks
    def render(self, request): 
        newtitle = request.args.get('newtitle', [None])[0]
        d = defer.maybeDeferred(self.notebook_db.change_notebook_metadata, newtitle)
        d.addCallback(self._success, request) 
        return server.NOT_DONE_YET

    def _success(self, result, request):
        newtitle = request.args.get('newtitle', [None])[0]
        data = {'response':'ok', 'title':newtitle}
        jsobj = json.dumps(data)
        request.setHeader("content-type", "application/json")
        request.write(jsobj)
        request.finish()


class Evaluate(EngineMethod):

    def render(self, req): 
        """Take request args and start callback chain.

        The callback chain includes saving input to database,
        then sending the code to the kernel to be run,
        then saving the result from the kernel to the database.
        """
        cellid = req.args.get('cellid', [None])[0]
        input = req.args.get('input', [""])[0]
        input = input.strip()
        d = defer.maybeDeferred(
                self.notebook_db.save_cell,
                    cellid, input,
                    type="input", style="input", props="props")
        d.addCallback(self.callEngine, req, cellid, input)
        req.setHeader("content-type", "application/json")
        return server.NOT_DONE_YET

    def _save_output(self, result, request, cellid):
        count, out, err = result['input_count'], result['out'], result['err']
        output = out + err
        if "__image__" in output:
            output = output[9:] + err
            style = "outputimage"
        else:
            style = "outputtext"
        outcellid = cellid + "o" #denote an 'output' cell
        d = defer.maybeDeferred(
                self.notebook_db.save_cell,
                    outcellid, output,
                    type="output", style=style, props="props")
        data = {'content':output, 'count':count, 'cellstyle':style, 'cellid':cellid}
        jsobj = json.dumps(data)
        request.write(jsobj)
        request.finish()

    def callEngine(self, result, request, cellid, input):
        d = self.engine.evaluate(input)
        d.addCallback(self._save_output, request, cellid)
        d.addErrback(self._kernel_err, request, cellid)
        return d

    def _kernel_err(self, result, request, cellid):
        output = 'Kernel Error: The interpreter might still be starting up. Try again.'
        count = '!'
        outputstyle = 'outputtext'
        #TODO Make an errortext style 
        # It could be cool to have tracebacks be errors and
        # kernel errors could be some other sort of message/warning
        data = {'content':output, 'count':count, 'cellstyle':outputstyle, 'cellid':cellid}
        jsobj = json.dumps(data)
        request.write(jsobj)
        request.finish()

class Completer(EngineMethod):
    """Complete either a name or an attribute
    """
    
    #@defer.inlineCallbacks
    def render(self, request): 
        mode = request.args['mode'][0]
        input = request.args['input'][0].strip()
        if mode == 'name':
            d = self.engine.complete_name(input)
        else:
            d = self.engine.complete_attr(input)
        d.addCallback(self._success, request)
        return server.NOT_DONE_YET #inlineCallbacks was 'working', thus old method, why?

    def _success(self, result, request):
        cellid = request.args['cellid'][0]
        data = {'completions':str(result), 'cellid':cellid}
        jsobj = json.dumps(data)
        request.setHeader("content-type", "application/json")
        request.write(jsobj)
        request.finish()

class Control(EngineMethod):
    """Handle requests for controlling the kernel process.
    Two signals can be sent to the kernel
    Interrupt is supposed to stop the kernel from computing (if it is)
        - any pending eval requests will be aborted once the current one is
          interrupted
    Kill is supposed to completely take out the kernel process (if it is
    running) no matter what!
    """
 
    #@defer.inlineCallbacks
    def render(self, request):
        action = request.args['action'][0].strip()
        actions = {'kill':self.engine.kill, 'interupt':self.engine.interrupt}
        d = defer.maybeDeferred(actions[action]) #XXX add error handling
        d.addCallback(self._success, request)
        return server.NOT_DONE_YET

    def _success(self, result, request):
        #resp = "{'resp':'failed', 'msg':'Bad process command. No such action'}"
        jsobj = json.dumps(result)
        request.setHeader("content-type", "application/json")
        request.write(jsobj)
        request.finish()

