# -*- test-case-name: knoboo.external.twisted.web2.test.test_xmlrpc -*-
#
# Copyright (c) 2001-2004 Twisted Matrix Laboratories.
# See LICENSE for details.

# 

"""Test XML-RPC support."""

import xmlrpclib

from knoboo.external.twisted.web2 import xmlrpc
from knoboo.external.twisted.web2 import server
from knoboo.external.twisted.web2 import http_headers
from knoboo.external.twisted.web2.xmlrpc import XMLRPC, addIntrospection, Client
from twisted.internet import defer

from knoboo.external.twisted.web2.test.test_server import BaseCase

class TestRuntimeError(RuntimeError):
    """
    Fake RuntimeError for testing purposes.
    """

class TestValueError(ValueError):
    """
    Fake ValueError for testing purposes.
    """

class XMLRPCTestResource(XMLRPC):
    """
    This is the XML-RPC "server" against which the tests will be run.
    """
    FAILURE = 666
    NOT_FOUND = 23
    SESSION_EXPIRED = 42

    addSlash = True # cause it's at the root
    
    # the doc string is part of the test
    def xmlrpc_add(self, request, a, b):
        """This function add two numbers."""
        return a + b

    xmlrpc_add.signature = [['int', 'int', 'int'],
                            ['double', 'double', 'double']]

    # the doc string is part of the test
    def xmlrpc_pair(self, request, string, num):
        """This function puts the two arguments in an array."""
        return [string, num]

    xmlrpc_pair.signature = [['array', 'string', 'int']]

    # the doc string is part of the test
    def xmlrpc_defer(self, request, x):
        """Help for defer."""
        return defer.succeed(x)

    def xmlrpc_deferFail(self, request):
        return defer.fail(TestValueError())

    # don't add a doc string, it's part of the test
    def xmlrpc_fail(self, request):
        raise TestRuntimeError

    def xmlrpc_fault(self, request):
        return xmlrpc.Fault(12, "hello")

    def xmlrpc_deferFault(self, request):
        return defer.fail(xmlrpc.Fault(17, "hi"))

    def xmlrpc_complex(self, request):
        return {"a": ["b", "c", 12, []], "D": "foo"}
    
    def xmlrpc_big(self, request):
        return "hello world"*1024

    def xmlrpc_dict(self, request, map, key):
        return map[key]

    def getFunction(self, functionPath):
        try:
            return XMLRPC.getFunction(self, functionPath)
        except xmlrpc.NoSuchFunction:
            if functionPath.startswith("SESSION"):
                raise xmlrpc.Fault(self.SESSION_EXPIRED, "Session non-existant/expired.")
            else:
                raise

    xmlrpc_dict.help = 'Help for dict.'

class TestAuthHeader(XMLRPCTestResource):
    """ 
    This is used to get the header info so that we can test
    authentication.
    """
    def __init__(self):
        super(XMLRPCTestResource, self).__init__()
        self.request = None

    def render(self, request):
        self.request = request
        return XMLRPCTestResource.render(self, request)

    def xmlrpc_authinfo(self, request):
        authh = request.headers.getHeader("Authorization")
        if not authh:
            user = password = ''
        else:
            basic, upw = authh
            upw = upw.decode('base64')
            user, password = upw.split(':')
        return user, password

class XMLRPCServerBase(BaseCase):
    """
    The parent class of the XML-RPC test classes.
    """
    method = 'POST'
    version = (1, 1)

    def setUp(self):
        self.root = XMLRPCTestResource()
        self.xml = ("<?xml version='1.0'?>\n<methodResponse>\n" +
            "%s</methodResponse>\n")

    def createClient(self, url, method, user=None, password=None, *args):
        p = xmlrpc.Client(url, user, password)
        f = p._buildFactory(method, *args)
        client = f.buildProtocol("")
        return client

class XMLRPCServerGETTest(XMLRPCServerBase):
    """
    Attempt access to the RPC resources as regular HTTP resource.
    """

    def setUp(self):
        super(XMLRPCServerGETTest, self).setUp()
        self.method = 'GET'
        self.errorRPC = ('<html><head><title>XML-RPC responder</title>' +
            '</head><body><h1>XML-RPC responder</h1>POST your XML-RPC ' +
            'here.</body></html>')
        self.errorHTTP = ('<html><head><title>404 Not Found</title>' +
            '</head><body><h1>Not Found</h1>The resource http://host/add ' +
            'cannot be found.</body></html>')

    def test_rootGET(self):
        """
        Test a simple GET against the XML-RPC server.
        """
        return self.assertResponse(
            (self.root, 'http://host/'),
            (200, {}, self.errorRPC))

    def test_childGET(self):
        """
        Try to access an XML-RPC method as a regular resource via GET.
        """
        return self.assertResponse(
            (self.root, 'http://host/add'),
            (404, {}, self.errorHTTP))

class XMLRPCServerPOSTTest(XMLRPCServerBase):
    """
    Tests for standard XML-RPC usage.
    """
    def test_RPCMethods(self):
        """
        Make RPC calls of the defined methods, checking for the expected 
        results.
        """
        inputOutput = [
            ("add", (2, 3), 5),
            ("defer", ("a",), "a"),
            ("dict", ({"a": 1}, "a"), 1),
            ("pair", ("a", 1), ["a", 1]),
            ("complex", (), {"a": ["b", "c", 12, []], "D": "foo"})]
        dl = []
        for meth, args, outp in inputOutput:
            postdata = xmlrpclib.dumps(args, meth)
            respdata = xmlrpclib.dumps((outp,))
            reqdata = (self.root, 'http://host/', {}, None, None, '', postdata)
            d = self.assertResponse(reqdata, (200, {}, self.xml % respdata))
            dl.append(d)
        return defer.DeferredList(dl, fireOnOneErrback=True)

    def test_RPCFaults(self):
        """
        Ensure that RPC faults are properly processed.
        """
        dl = []
        codeMethod = [
            (12, "fault", 'hello'),
            (23, "noSuchMethod", 'function noSuchMethod not found'),
            (17, "deferFault", 'hi'),
            (42, "SESSION_TEST", 'Session non-existant/expired.')]
        for code, meth, fault in codeMethod:
            postdata = xmlrpclib.dumps((), meth)
            respdata = xmlrpclib.dumps(xmlrpc.Fault(code, fault))
            reqdata = (self.root, 'http://host/', {}, None, None, '', postdata)
            d = self.assertResponse(reqdata, (200, {}, respdata))
            dl.append(d)
        d = defer.DeferredList(dl, fireOnOneErrback=True)
        return d

    def test_RPCFailures(self):
        """
        Ensure that failures behave as expected.
        """
        dl = []
        codeMethod = [
            (666, "fail"),
            (666, "deferFail")]
        for code, meth in codeMethod:
            postdata = xmlrpclib.dumps((), meth)
            respdata = xmlrpclib.dumps(xmlrpc.Fault(code, 'error'))
            reqdata = (self.root, 'http://host/', {}, None, None, '', postdata)
            d = self.assertResponse(reqdata, (200, {}, respdata))
            d.addCallback(self.flushLoggedErrors, TestRuntimeError, TestValueError)
            dl.append(d)
        d = defer.DeferredList(dl, fireOnOneErrback=True)
        return d

class XMLRPCTestIntrospection(XMLRPCServerBase):

    def setUp(self):
        """
        Introspection requires additional setup, most importantly, adding
        introspection to the root object.
        """
        super(XMLRPCTestIntrospection, self).setUp()
        addIntrospection(self.root)
        self.methodList = ['add', 'big', 'complex', 'defer', 'deferFail',
            'deferFault', 'dict', 'fail', 'fault', 'pair',
            'system.listMethods', 'system.methodHelp', 'system.methodSignature']

    def test_listMethods(self):
        """
        Check that the introspection method "listMethods" returns all the
        methods we defined in the XML-RPC server.
        """
        def cbMethods(meths):
            meths.sort()
            self.failUnlessEqual(
                meths,
                )
        postdata = xmlrpclib.dumps((), 'system.listMethods')
        respdata = xmlrpclib.dumps((self.methodList,))
        reqdata = (self.root, 'http://host/', {}, None, None, '', postdata)
        return self.assertResponse(reqdata, (200, {}, self.xml % respdata))

    def test_methodHelp(self):
        """
        Check the RPC methods for docstrings or .help attributes.
        """
        inputOutput = [
            ("defer", "Help for defer."),
            ("fail", ""),
            ("dict", "Help for dict.")]

        dl = []
        for meth, outp in inputOutput:
            postdata = xmlrpclib.dumps((meth,), 'system.methodHelp')
            respdata = xmlrpclib.dumps((outp,))
            reqdata = (self.root, 'http://host/', {}, None, None, '', postdata)
            d = self.assertResponse(reqdata, (200, {}, self.xml % respdata))
            dl.append(d)
        return defer.DeferredList(dl, fireOnOneErrback=True)

    def test_methodSignature(self):
        """
        Check that the RPC methods whose signatures have been set via the
        .signature attribute (on the method) are returned as expected.
        """
        inputOutput = [
            ("defer", ""),
            ("add", [['int', 'int', 'int'],
                     ['double', 'double', 'double']]),
            ("pair", [['array', 'string', 'int']])]

        dl = []
        for meth, outp in inputOutput:
            postdata = xmlrpclib.dumps((meth,), 'system.methodSignature')
            respdata = xmlrpclib.dumps((outp,))
            reqdata = (self.root, 'http://host/', {}, None, None, '', postdata)
            d = self.assertResponse(reqdata, (200, {}, self.xml % respdata))
            dl.append(d)
        return defer.DeferredList(dl, fireOnOneErrback=True)

class XMLRPCClient(XMLRPCServerBase):
    def testErroneousResponse(self):
        """
        Test that requesting a non existent method returns an exception
        """
        method = "someMethod"
        client = self.createClient("http://127.0.0.1/", method)
        headers = client._prepareHeaders()
        
        error = 23, 'function ' + method + ' not found'
        error_response = xmlrpclib.dumps(xmlrpc.Fault(*error))
        
        reqdata = (self.root, 'http://127.0.0.1/', headers, None, None, '', client.factory.payload)
        return self.assertResponse(reqdata, (200, {}, error_response))
    
    def testCorrect(self):
        """
        Test that calling an existing method works fine.
        """
        inputOutput = [
            ("add", (2, 3), 5),
            ("defer", ("a",), "a"),
            ("dict", ({"a": 1}, "a"), 1),
            ("pair", ("a", 1), ["a", 1]),
            ("complex", (), {"a": ["b", "c", 12, []], "D": "foo"})]
        dl = []
        for meth, args, outp in inputOutput:
            client = self.createClient("http://127.0.0.1", meth, None, None, *args)
            respdata = xmlrpclib.dumps((outp,))
            
            reqdata = (self.root, 'http://host/', {}, None, None, '', client.factory.payload)
            d = self.assertResponse(reqdata, (200, {}, self.xml % respdata))
            dl.append(d)
        return defer.DeferredList(dl, fireOnOneErrback=True)
    
    def testHeaders(self):
        """
        Test that headers are correctly generated.
        """
        client = self.createClient("http://127.0.0.1", "someMethod")
        headers = client._prepareHeaders()
        
        self.assertEquals(headers.getHeader('user-agent'), 'Twisted Web2/XMLRPClib')
        self.assertEquals(headers.getHeader('host'), client.factory.host)
        self.assertEquals(headers.getHeader('content-length'), len(client.factory.payload))
        self.assertEquals(headers.getHeader('content-type'), http_headers.MimeType.fromString('text/xml'))
        

class XMLRPCTestAuthenticated(XMLRPCServerBase):
    """
    Test with authenticated proxy. We run this with the same input/output as
    above.
    """
    user = "username"
    password = "asecret"

    def setUp(self):
        super(XMLRPCTestAuthenticated, self).setUp()
        self.root = TestAuthHeader()

    def testAuthenticationHeader(self):
        """
        Test Authentication header presence and check its value.
        """
        client = self.createClient("http://%s:%s@127.0.0.1/" % (self.user, self.password), "authinfo")
        headers = client._prepareHeaders()

        auth = '%s:%s' % (self.user, self.password)
        auth = auth.encode('base64').strip()
        return self.assertEquals(headers.getHeader("Authorization"), ('basic', auth))

    def testAuthInfoInURL(self):
        """
        Test authentication information put in the URL.
        """
        client = self.createClient("http://%s:%s@127.0.0.1/" % (self.user, self.password), "authinfo")
        headers = client._prepareHeaders()

        outp = xmlrpclib.dumps(([self.user, self.password],))
        reqdata = (self.root, 'http://127.0.0.1/', headers, None, None, '', client.factory.payload)
        
        return self.assertResponse(reqdata, (200, {}, self.xml % outp))

    def testExplicitAuthInfo(self):
        """
        Test authentication information sent in the body of the request
        """
        client = self.createClient("http://127.0.0.1/", "authinfo", self.user, self.password)
        headers = client._prepareHeaders()
        
        outp = xmlrpclib.dumps(([self.user, self.password],))
        reqdata = (self.root, 'http://127.0.0.1/', headers, None, None, '', client.factory.payload)
        return self.assertResponse(reqdata, (200, {}, self.xml % outp))

    def testExplicitAuthInfoOverride(self):
        """
        Authentication information passed in the constructor has precedence
        over what is written in the URL.
        """
        client = self.createClient("http://wrong:info@127.0.0.1/", "authinfo", self.user, self.password)
        headers = client._prepareHeaders()
        
        outp = xmlrpclib.dumps(([self.user, self.password],))
        reqdata = (self.root, 'http://127.0.0.1/', headers, None, None, '', client.factory.payload)        
        return self.assertResponse(reqdata, (200, {}, self.xml % outp))

class XMLRPCRealServerBase(BaseCase):
    """
    Parent class for all the XML-RPC test classes that use the real network.
    """
    method = 'POST'
    version = (1, 1)
    rootResource = XMLRPC

    def setUp(self):
        from twisted.internet import reactor
        from knoboo.external.twisted.web2 import channel
        self.resource = self.rootResource()
        site = server.Site(self.resource)
        self.p = reactor.listenTCP(0, channel.HTTPFactory(site), interface="127.0.0.1")
        self.port = self.p.getHost().port

    def tearDown(self): 
        return self.p.stopListening()

class TestFailingCalls(XMLRPCRealServerBase):
    def testFailingCallRemote(self):
        """Test an actual failing call of client.callRemote"""
        client = xmlrpc.Client("http://localhost:%d/" % (self.port,))
        def _eb(err):
            self.assertEquals(err.value.code, 404)
            self.assertEquals(err.value.message, "Not Found")
        return client.callRemote("whatever").addErrback(_eb)

class TestWorkingCalls(XMLRPCRealServerBase):
    rootResource = XMLRPCTestResource
    def testCallRemote(self):
        """Test a working client.callRemote call"""
        client = xmlrpc.Client("http://localhost:%d" % (self.port,))
        return client.callRemote("big").addCallback(self.assertEquals, "hello world"*1024)
        
