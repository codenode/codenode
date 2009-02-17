# -*- test-case-name: knoboo.external.twisted.web2.test.test_xmlrpc -*-
#
# Copyright (c) 2001-2004 Twisted Matrix Laboratories.
# See LICENSE for details.


"""
A generic resource for publishing objects via XML-RPC.

Maintainer: U{Itamar Shtull-Trauring<mailto:twisted@itamarst.org>}
"""

# System Imports
import xmlrpclib
import urlparse

# Sibling Imports
from knoboo.external.twisted.web2 import resource, stream
from knoboo.external.twisted.web2 import responsecode, http, http_headers
from knoboo.external.twisted.web2.client.http import ClientRequest
from knoboo.external.twisted.web2.client.http import HTTPClientProtocol
from twisted.internet import defer, protocol, reactor

from twisted.python import log, reflect, failure

# Useful so people don't need to import xmlrpclib directly
Fault = xmlrpclib.Fault
Binary = xmlrpclib.Binary
Boolean = xmlrpclib.Boolean
DateTime = xmlrpclib.DateTime


class NoSuchFunction(Fault):
    """There is no function by the given name."""
    pass

class BadResponseCodeError(Exception):
    def __init__(self, code, message):
        """The server responded with a non-200 HTTP errorstatus
        
        @param code: The numeric HTTP error code
        @type code: C{int}

        @param message: The HTTP message corresponding to the error code.
        @type message: C{str} or C{unicode}
        """
        Exception.__init__(self)
        self.code = code
        self.message = message

class XMLRPC(resource.Resource):
    """A resource that implements XML-RPC.
    
    You probably want to connect this to '/RPC2'.

    Methods published can return XML-RPC serializable results, Faults,
    Binary, Boolean, DateTime, Deferreds, or Handler instances.

    By default methods beginning with 'xmlrpc_' are published.

    Sub-handlers for prefixed methods (e.g., system.listMethods)
    can be added with putSubHandler. By default, prefixes are
    separated with a '.'. Override self.separator to change this.
    """

    # Error codes for Twisted, if they conflict with yours then
    # modify them at runtime.
    NOT_FOUND = 8001
    FAILURE = 8002

    separator = '.'

    def __init__(self):
        resource.Resource.__init__(self)
        self.subHandlers = {}

    def putSubHandler(self, prefix, handler):
        self.subHandlers[prefix] = handler

    def getSubHandler(self, prefix):
        return self.subHandlers.get(prefix, None)

    def getSubHandlerPrefixes(self):
        return self.subHandlers.keys()

    def render(self, request):
        # For GET/HEAD: Return an error message
        s=("<html><head><title>XML-RPC responder</title></head>"
           "<body><h1>XML-RPC responder</h1>POST your XML-RPC here.</body></html>")
        
        return http.Response(responsecode.OK,
            {'content-type': http_headers.MimeType('text', 'html')},
            s)
    
    def http_POST(self, request):
        parser, unmarshaller = xmlrpclib.getparser()
        deferred = stream.readStream(request.stream, parser.feed)
        deferred.addCallback(lambda x: self._cbDispatch(
            request, parser, unmarshaller))
        deferred.addErrback(self._ebRender)
        deferred.addCallback(self._cbRender, request)
        return deferred

    def _cbDispatch(self, request, parser, unmarshaller):
        parser.close()
        args, functionPath = unmarshaller.close(), unmarshaller.getmethodname()

        function = self.getFunction(functionPath)
        return defer.maybeDeferred(function, request, *args)

    def _cbRender(self, result, request):
        if not isinstance(result, Fault):
            result = (result,)
        try:
            s = xmlrpclib.dumps(result, methodresponse=1)
        except:
            f = Fault(self.FAILURE, "can't serialize output")
            s = xmlrpclib.dumps(f, methodresponse=1)
        return http.Response(responsecode.OK,
            {'content-type': http_headers.MimeType('text', 'xml')},
            s)

    def _ebRender(self, failure):
        if isinstance(failure.value, Fault):
            return failure.value
        log.err(failure)
        return Fault(self.FAILURE, "error")

    def getFunction(self, functionPath):
        """Given a string, return a function, or raise NoSuchFunction.

        This returned function will be called, and should return the result
        of the call, a Deferred, or a Fault instance.

        Override in subclasses if you want your own policy. The default
        policy is that given functionPath 'foo', return the method at
        self.xmlrpc_foo, i.e. getattr(self, "xmlrpc_" + functionPath).
        If functionPath contains self.separator, the sub-handler for
        the initial prefix is used to search for the remaining path.
        """
        if functionPath.find(self.separator) != -1:
            prefix, functionPath = functionPath.split(self.separator, 1)
            handler = self.getSubHandler(prefix)
            if handler is None:
                raise NoSuchFunction(self.NOT_FOUND, "no such subHandler %s" % prefix)
            return handler.getFunction(functionPath)

        f = getattr(self, "xmlrpc_%s" % functionPath, None)
        if not f:
            raise NoSuchFunction(self.NOT_FOUND, "function %s not found" % functionPath)
        elif not callable(f):
            raise NoSuchFunction(self.NOT_FOUND, "function %s not callable" % functionPath)
        else:
            return f

    def _listFunctions(self):
        """Return a list of the names of all xmlrpc methods."""
        return reflect.prefixedMethodNames(self.__class__, 'xmlrpc_')


class XMLRPCIntrospection(XMLRPC):
    """Implement the XML-RPC Introspection API.

    By default, the methodHelp method returns the 'help' method attribute,
    if it exists, otherwise the __doc__ method attribute, if it exists,
    otherwise the empty string.

    To enable the methodSignature method, add a 'signature' method attribute
    containing a list of lists. See methodSignature's documentation for the
    format. Note the type strings should be XML-RPC types, not Python types.
    """

    def __init__(self, parent):
        """Implement Introspection support for an XMLRPC server.

        @param parent: the XMLRPC server to add Introspection support to.
        """

        XMLRPC.__init__(self)
        self._xmlrpc_parent = parent

    def xmlrpc_listMethods(self, request):
        """Return a list of the method names implemented by this server."""
        functions = []
        todo = [(self._xmlrpc_parent, '')]
        while todo:
            obj, prefix = todo.pop(0)
            functions.extend([prefix + name for name in obj._listFunctions()])
            todo.extend([(obj.getSubHandler(name),
                           prefix + name + obj.separator)
                          for name in obj.getSubHandlerPrefixes()])
        functions.sort()
        return functions

    xmlrpc_listMethods.signature = [['array']]

    def xmlrpc_methodHelp(self, request, method):
        """Return a documentation string describing the use of the given method.
        """
        method = self._xmlrpc_parent.getFunction(method)
        return (getattr(method, 'help', None)
                or getattr(method, '__doc__', None) or '')

    xmlrpc_methodHelp.signature = [['string', 'string']]

    def xmlrpc_methodSignature(self, request, method):
        """Return a list of type signatures.

        Each type signature is a list of the form [rtype, type1, type2, ...]
        where rtype is the return type and typeN is the type of the Nth
        argument. If no signature information is available, the empty
        string is returned.
        """
        method = self._xmlrpc_parent.getFunction(method)
        return getattr(method, 'signature', None) or ''

    xmlrpc_methodSignature.signature = [['array', 'string'],
                                        ['string', 'string']]


def addIntrospection(xmlrpc):
    """Add Introspection support to an XMLRPC server.

    @param xmlrpc: The xmlrpc server to add Introspection support to.
    """
    xmlrpc.putSubHandler('system', XMLRPCIntrospection(xmlrpc))

class QueryProtocol(HTTPClientProtocol):
    
    def _prepareHeaders(self):
        rawHeaders = {
            'User-Agent': ['Twisted Web2/XMLRPClib'],
            'Host': [self.factory.host],
            'Content-Type': ['text/xml'],
            'Content-Length': [str(len(self.factory.payload))],
        }
        if self.factory.user:
            auth = '%s:%s' % (self.factory.user, self.factory.password)
            auth = auth.encode('base64').strip()
            rawHeaders.update({
                'Authorization': ['Basic %s' % (auth,)],
            })
        headers = http_headers.Headers(rawHeaders=rawHeaders)
        return headers
    
    def connectionMade(self):
        headers = self._prepareHeaders()
        req = ClientRequest('POST', self.factory.path, headers,
            self.factory.payload)
        d = self.submitRequest(req)
        d.addCallback(self._cbGotResponse)
        d.addErrback(self._ebGotError)
        return d

    def _cbGotResponse(self, resp):
        if resp.code != 200:
            msg = responsecode.RESPONSES[resp.code]
            self.factory.badStatus(resp.code, msg)
        
        contents = []
        def _aggregate(data):
            contents.append(data)
        d = stream.readStream(resp.stream, _aggregate)
        d.addCallback(lambda _: self.handleResponse(''.join(contents)))
        return d

    def _ebGotError(self, error):
        # XXX what's the best way to do this?
        print error.getErrorMessage()

    def handleResponse(self, contents):
        self.factory.parseResponse(contents)


payloadTemplate = """<?xml version="1.0"?>
<methodCall>
<methodName>%s</methodName>
%s
</methodCall>
"""


class QueryFactory(protocol.ClientFactory):

    deferred = None
    protocol = QueryProtocol

    def __init__(self, path, host, method, user=None, password=None, *args):
        self.path, self.host = path, host
        self.user, self.password = user, password
        self.payload = payloadTemplate % (method, xmlrpclib.dumps(args))
        self.deferred = defer.Deferred()

    def parseResponse(self, contents):
        if not self.deferred:
            return
        try:
            response = xmlrpclib.loads(contents)
        except:
            self.deferred.errback(failure.Failure())
            self.deferred = None
        else:
            self.deferred.callback(response[0][0])
            self.deferred = None

    def clientConnectionLost(self, _, reason):
        if self.deferred is not None:
            self.deferred.errback(reason)
            self.deferred = None

    clientConnectionFailed = clientConnectionLost

    def badStatus(self, status, message):
        self.deferred.errback(BadResponseCodeError(status, message))
        self.deferred = None


class Client(object):
    """A Client for making remote XML-RPC calls.

    Pass the URL of the remote XML-RPC server to the constructor.

    Use proxy.callRemote('foobar', *args) to call remote method
    'foobar' with *args.

    """

    def __init__(self, url, user=None, password=None):
        """
        @type url: C{str}
        @param url: The URL to which to post method calls.  Calls will be made
        over SSL if the scheme is HTTPS.  If netloc contains username or
        password information, these will be used to authenticate, as long as
        the C{user} and C{password} arguments are not specified.

        @type user: C{str} or None
        @param user: The username with which to authenticate with the server
        when making calls.  If specified, overrides any username information
        embedded in C{url}.  If not specified, a value may be taken from C{url}
        if present.

        @type password: C{str} or None
        @param password: The password with which to authenticate with the
        server when making calls.  If specified, overrides any password
        information embedded in C{url}.  If not specified, a value may be taken
        from C{url} if present.
        """
        scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
        netlocParts = netloc.split('@')
        if len(netlocParts) == 2:
            userpass = netlocParts.pop(0).split(':')
            self.user = userpass.pop(0)
            try:
                self.password = userpass.pop(0)
            except:
                self.password = None
        else:
            self.user = self.password = None
        hostport = netlocParts[0].split(':')
        self.host = hostport.pop(0)
        try:
            self.port = int(hostport.pop(0))
        except:
            self.port = None
        self.path = path
        if self.path in ['', None]:
            self.path = '/'
        self.secure = (scheme == 'https')
        if user is not None:
            self.user = user
        if password is not None:
            self.password = password
    
    def _buildFactory(self, method, *args):
        return QueryFactory(self.path, self.host, method, self.user,
                    self.password, *args)

    def callRemote(self, method, *args):
        factory = self._buildFactory(method, *args)
        if self.secure:
            from twisted.internet import ssl
            reactor.connectSSL(self.host, self.port or 443,
                               factory, ssl.ClientContextFactory())
        else:
            reactor.connectTCP(self.host, self.port or 80, factory)
        return factory.deferred

__all__ = ["XMLRPC", "NoSuchFunction", "Fault", "Client"]
