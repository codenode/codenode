
from zope.interface import Interface, implements

from twisted.web import xmlrpc
from twisted.plugin import IPlugin
from twisted.internet import defer


class IEngineConfiguration(Interface):
    """Engine process plugin
    """

class EngineConfigurationBase(object):
    """
    Container of system specific configuration necessary and sufficient 
    to execute a program.

    The bin executable should be the interpreters bin file; it should not
    be a shell script wrapping/spawning another bin executable.  

    The recommended way to create an engine plugin is to create a subclass
    of this class with a name denoting the type of engine (e.g. Python). 

    @param args List of command line arguments passed to the bin
    @param env Environment variables.
    @param path Full path of directory to run the process in
    """

    implements(IPlugin, IEngineConfiguration)

    bin = '' #Full path of program to run
    args = [] #List of command line args to pass
    env = {} #Dictionary of environment variables
    path = '' #Directory to run process in

    def __init__(self):
        self.name = self.__class__.__name__

    def __repr__(self):
        """Name is used as the unique identifier.
        Make sure all engine plugins have unique class names.
        """
        return "%s" % self.name

    def __str__(self):
        return "%s engine: %s %s" % (self.name, self.bin, str(self.args))

class IEngine(Interface):
    """
    Client representing an engine.

    The result of a new Engine request.

    This is independent of the server protocol/transport.
    This is to be adapted to some kind of server.

    The methods of this api are the basic/fundamental ways to use the
    interpreter:
     - evaluate
     - complete
    """

    def evaluate(to_evaluate):
        """
        Evaluate arbitrary code @param to_evaluate

        return result as deferred
        """

    def complete(to_complete):
        """
        Get the list of possible completions from the current namespace or
        from an objects set of attributes.
        """



class Engine:
    """
    Implementation of IEngine using an xml rpc client.
    """

    implements(IEngine)


    def __init__(self, d, id):
        """
        @param client configured xml rpc client
        """
        self.id = id
        self.client = None
        self.deferred = d
        d.addCallback(self._start)
        d.addErrback(self._fail)
        self.ready = False

    def _start(self, port):
        self.client = xmlrpc.Proxy("http://localhost:%s" % port)
        self.ready = True
        return True

    def _fail(self, r):
        return False

    @defer.inlineCallbacks
    def evaluate(self, to_evaluate):
        """
        return a Deferred
        """
        if not self.ready:
            is_ready_now = yield self.deferred
            if not is_ready_now:
                defer.returnValue("Engine Failed To Start")
        result = yield self.client.callRemote('evaluate', to_evaluate)
        defer.returnValue(result)

    @defer.inlineCallbacks
    def complete(self, to_complete):
        """
        return a Deferred
        """
        if not self.ready:
            is_ready_now = yield self.deferred
            if not is_ready_now:
                defer.returnValue("Engine Failed To Start")
        result = yield self.client.callRemote('complete', to_complete)
        defer.returnValue(result)

