
from zope.interface import implements 

from twisted.web import xmlrpc
from twisted.web import resource
from twisted.web import server

from django.utils import simplejson as json

from codenode.frontend.notebook import models as nb_models
from codenode.frontend.backend import models as bkend_models

from codenode.backend import engine

class InstanceInterpreterProxy(object):
    """Representative (proxy) of an engine instance running on a Backend.
    @note This is a concept place holder. The proxies to remote services
    should be chain-able. For any primary service, optional/secondary
    services should be arbitrarily called before, or after the main
    service.
    """

    implements(engine.IEngine)

    def __init__(self, address, id):
        self.client = xmlrpc.Proxy(str(address) + '/interpreter/' + str(id))

    def evaluate(self, to_evaluate):
        """
        """
        return self.client.callRemote('evaluate', str(to_evaluate))

    def complete_name(self, to_complete):
        """
        """
        return self.client.callRemote('complete_name', to_complete)

    def complete_attr(self, to_complete):
        """
        """
        return self.client.callRemote('complete_attr', to_complete)


class BackendManager(object):
    """
    When the request gets here, it has already been associated to a User
    via a session ID (stored in the db).

    Filter Notebook table by permitted writer/evaluator (owner and
    collaborator, currently)
    Then, query notebook by id. The result will be either:
     - nb exists (therefore configured with a backend engine type)
      -- get current engine instance id, or create a new instance (implicit
      start up; this is a design decision, maybe it should be configurable)
      Use Backend admin to create new instance. 
      Use Engine client to execute request.
    - nb does not exist; return error.
    """

    def getBackendEngine(self, notebook_id, user_id=None):
        #nb = nb_models.Notebook.objects.filter(owner=user_id).get(guid=notebook_id)
        nb = nb_models.Notebook.objects.get(guid=notebook_id)
        # if there is no instance, create one, the notebook should have a
        # default engine type already configured
        engine_inst = bkend_models.EngineInstance.objects.get(notebook=nb)
        return InstanceInterpreterProxy(engine_inst.backend.address, engine_inst.instance_id)

    def runEngineInstance(self, notebook_id, user_id=None):
        nb = nb_models.Notebook.objects.get(guid=notebook_id)
        backend = nb.engine_type.backend
        client = xmlrpc.Proxy(backend.address + '/admin')
        d = client.callRemote("runEngineInstance", nb.engine_type.name)
        return d




class NotebookEngineRequestHandler(resource.Resource):

    def __init__(self, backend):
        resource.Resource.__init__(self)
        self.backend = backend
        self.putChild("", self)

    def getChild(self, path, request):
        """Path should be notebook id
        """
        engine_instance = self.backend.getBackendEngine(path)
        return NotebookMethods(engine_instance)



class NotebookMethods(resource.Resource):

    def __init__(self, engine):
        resource.Resource.__init__(self)
        self.putChild("evaluate", Evaluate(engine))
        self.putChild("complete", Complete(engine))


def save_cell(notebook_id, cell_id, content, type, style, props):
    cell_id, content, type, style, props = [unicode(w) for w in [cell_id, content, type, style, props]]
    nb = nb_models.Notebook.objects.get(guid=notebook_id)
    #cell, created = models.Cell.objects.get_or_create(guid=id, owner=nb.owner)
    cells = nb_models.Cell.objects.filter(guid=cell_id)
    if len(cells) == 0:
        cell = nb_models.Cell(guid=cell_id, owner=nb.owner)
    else:
        cell = cells[0]
    cell.content = content
    cell.type = type
    cell.style = style
    cell.props = props
    if len(cells) == 0:
        nb.cell_set.add(cell)
        nb.save()
    else:
        cell.save()

class Evaluate(resource.Resource):

    def __init__(self, engine):
        resource.Resource.__init__(self)
        self.engine = engine

    def render(self, req): 
        """Take request args and start callback chain.

        The callback chain includes saving input to database,
        then sending the code to the kernel to be run,
        then saving the result from the kernel to the database.
        """
        cellid = req.args.get('cellid', [None])[0]
        input = req.args.get('input', [""])[0]
        input = input.strip()

        # need notebook id
        #save_cell(cellid, input, type="input", style="input", props="props")
        #         ^^


        d = self.engine.evaluate(input)
        d.addCallback(self._engine_cb, req, cellid)
        req.setHeader("content-type", "application/json")
        return server.NOT_DONE_YET

    def _engine_cb(self, result, request, cellid):
        count, out, err = result['input_count'], result['out'], result['err']
        output = out + err
        if "__image__" in output:
            output = output[9:] + err
            style = "outputimage"
        else:
            style = "outputtext"
        outcellid = cellid + "o" #denote an 'output' cell
        data = {'content':output, 'count':count, 'cellstyle':style, 'cellid':cellid}
        jsobj = json.dumps(data)
        request.write(jsobj)
        request.finish()


class Complete(resource.Resource):

    def __init__(self, engine):
        resource.Resource.__init__(self)
        self.engine = engine

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

class InstanceControlProxy(object):
    """Representative for controlling remote engine instance.
    """


class NotebookDatabaseProxy(object):
    """Representative of read/write access to notebook data.
    """




