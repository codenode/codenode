##################################################################### 
# Copyright (C) 2007 Alex Clemesha <clemesha@gmail.com>
#                and Dorian Raymer <deldotdr@gmail.com>
# 
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
##################################################################### 

import os

from twisted.internet import defer

from twisted.web import server, resource

from knoboo.external import simplejson as json

from knoboo.kernel.remoteclient import EngineFactory
from knoboo.printing import printers

from knoboo import settings
from knoboo.async import dbmanager


class Notebook(resource.Resource):
    """If request is not an operation, render returns the notebook template
    with which the browser sets up the boilerplace notebook html and
    javascript

    If an operation is requested, then check for the exstince of the
    operations resource tree stored in the notebook sessions manager.
    Create one if one does not exist.
    """
    isLeaf = False

    def __init__(self, nbSessionManager): 
        resource.Resource.__init__(self)
        self.nbSessionManager = nbSessionManager

    def getChild(self, path, request):
        print " ==************************== ***********======== ", path, self.__class__.__name__, request.prepath
        rsrc = self.nbSessionManager.getSession(path)
        return rsrc.children[path]
        #return self
        #return rsrc, segments

    def render_GET(self, request):
        return "NOTEBOOK"


class EngineMethod(resource.Resource):
    """A resource of this type is like a wrapper around an actual engine
    method.

    """

    def __init__(self, notebook_db, engine=None):
        self.notebook_db = notebook_db
        self.engine = engine

    def respondJson(self, jsonobj):
        #request.setHeader("content-type", "application/json")
        return jsonobj

class EngineSession(resource.Resource):
    """A parent resource of computation engine operations.
    This resource tree has access to a computation engine for the notebook
    session.
    """

    addSlash = True

    def __init__(self, nbid, notebook_db, engine, env_path): 
        resource.Resource.__init__(self)
        self.nbid = nbid
        self.notebook_db = notebook_db
        self.engine = engine
        print "PPPPPPPPPPPPPPPPCCCCCCCCCCCCCCCCCCCC"
        self.putChild(nbid, NotebookRoot(nbid, notebook_db, engine, env_path))

class SessionManager(object):


    def __init__(self):
        """store notebook operations resources by nbid
        """
        self.engineFactory = EngineFactory()
        self.sessions = {}

    def newSession(self, nbid):
        """return a new resource tree
        """
        print nbid
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


class NotebookRoot(resource.Resource):

    addSlash = True

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
        #self.putChild("print", Print(notebook_db, env_path))

    def render(self, request):
        nb = self.notebook_db.get_notebook()
        title = nb.title
        system = nb.system
        #html = templates.notebook(nb.owner, title, system).encode("utf-8")
        return self.__class__.__name__

class StartEngine(EngineMethod):
    """Start the notebooks computation process.
    """

    def render(self, request):
        d = defer.maybeDeferred(self.engine.start)
        d.addCallback(self._success)
        d.addErrback(self._failure)
        return d

    def _success(self, result):
        return self.respondJson('ok')

    def _failure(self, result):
        return self.respondJson('failed')

class NotebookObject(EngineMethod):
    """Notebook js object.
    """

    def render(self, request):
        d = defer.maybeDeferred(self.notebook_db.get_notebook_data)
        d.addCallback(self._success)
        return d

    def _success(self, result):
        jsobj = json.dumps(result)
        return self.respondJson(jsobj)

class SaveNotebookMetaData(EngineMethod):
    """Save non cell data from a notebook to the database.

    This is a resource used from an async call to '/bookshelf/save'
    to save data associated with a notebook.
    """
    def render(self, request):
        orderlist = request.args.get('orderlist', [])
        orderlist = ','.join(orderlist)
        cellsdata = request.args.get('cellsdata', [None])[0]
        cellsdata = json.loads(cellsdata)
        d = defer.maybeDeferred(self.notebook_db.save_notebook_metadata,
                orderlist, cellsdata)
        d.addCallback(self._success)
        d.addErrback(self._failed)
        return d

    def _success(self, result):
        return self.respondJson("ok")

    def _failed(self, result):
        return self.respondJson("failed")

class DeleteCell(EngineMethod):
    """Delete cells from the database.

    Take a list of cellids, and deleted all 
    data associated with the cellid.
    """

    def render(self, req): 
        """
        Delete one or more cells.
        """
        #XXX untested - javascript doesn't work right now to delete a cell?
        cellids = json.loads(req.args.get('cellids', [None])[0])
        d = defer.maybeDeferred(self.notebook_db.delete_cells,
                cellids)
        d.addCallback(self._success)
        return d

    def _success(self, result):
        return self.respondJson("ok")

class ChangeNotebookMetaData(EngineMethod):
    """Change notebook title ... could be more general.
    """

    def render(self, request): 
        newtitle = request.args.get('newtitle', [None])[0]
        d = defer.maybeDeferred(self.notebook_db.change_notebook_metadata,
                newtitle)
        d.addCallback(self._success, newtitle)
        return d

    def _success(self, result, newtitle):
        data = {'response':'ok', 'title':newtitle}
        jsobj = json.dumps(data)
        return self.respondJson(jsobj)

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
        output = 'Kernel Error: The interpreter might still be starting up.'
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
    
    def _success(self, result, cellid):
        output = str(result)
        data = {'completions':output, 'cellid':cellid}
        jsobj = json.dumps(data)
        return self.respondJson(jsobj)

    def render(self, req): 
        """What initially handles the request.
        Get all the post args and go into the chain of defereds.
        """
        cellid = req.args['cellid'][0]
        mode = req.args['mode'][0]
        input = req.args['input'][0].strip()
        if mode == 'name':
            d = self.engine.complete_name(input)
        else:
            d = self.engine.complete_attr(input)
        d.addCallback(self._success, cellid)
        return d

class Control(EngineMethod):
    """Handle requests for controlling the kernel process.
    Two signals can be sent to the kernel
    Interrupt is supposed to stop the kernel from computing (if it is)
        - any pending eval requests will be aborted once the current one is
          interrupted
    Kill is supposed to completely take out the kernel process (if it is
    running) no matter what!
    """
 
    def _bad_request(self, result):
        html = "Bad process command. No such action"
        return self.respondHtml(html)

    def _signalCallback(self, result):
        #if result:
        html = str(result)
        return self.respondHtml(html)

    def render(self, req):
        action = req.args['action'][0].strip()
        
        actions = {'kill':self.engine.kill, 'interupt':self.engine.interrupt}
        if actions.has_key(action):
            d = defer.maybeDeferred(actions[action])
            d.addCallback(self._signalCallback)
        else:
            #FIXME: this might be bad code here! where is the callback
            # triggered?
            d = defer.Deferred()
            d.addCallback(self._bad_request)
        return d


