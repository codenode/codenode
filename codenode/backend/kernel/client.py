######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

import xmlrpclib
import urlparse

from twisted.internet import defer, protocol, reactor
from codenode.external.twisted.web.xmlrpc import QueryProtocol, payloadTemplate
from codenode.external.twisted.web.xmlrpc import Proxy
from twisted.python import failure

class RPCQueryFactory(protocol.ReconnectingClientFactory):

    deferred = None
    protocol = QueryProtocol
    maxRetries = 20

    def __init__(self, path, host, method, user=None, password=None, 
                        allowNone=False, args=()):
        self.path, self.host = path, host
        self.user, self.password = user, password
        self.payload = payloadTemplate % (method, 
                xmlrpclib.dumps(args, allow_none=allowNone))
        self.deferred = defer.Deferred()

    def parseResponse(self, contents):
        if not self.deferred:
            return
        self.resetDelay()
        try:
            response = xmlrpclib.loads(contents)
        except:
            print 'parseRESPONSE Error ############'
            self.deferred.errback(failure.Failure())
            self.deferred = None
        else:
            self.deferred.callback(response[0][0])
            self.deferred = None

    def clientConnectionLost(self, _, reason):
        """ReconnectingClientFactory has this method try to reconnect
        automatically. So far, we only want this to happen on the initial
        connection.
        """
        if self.deferred is not None:
            print 'CONECTION LOST', reason
            self.deferred.errback(reason)
            self.deferred = None

    def badStatus(self, status, message):
        """need to fix errors differing between web and web2
        """
        self.deferred.errback(ValueError(status, message))
        #self.deferred.errback(BadResponseCodeError(status, message))
        self.deferred = None

class RPCClient(Proxy):
    queryFactory = RPCQueryFactory


class EngineClient(object):
    """Client is initialized with host and port of engine server.

    The initial connection of the client should be made when the engine
    manager knows the engine process started. 

    The initial connection could be:
     - instantiate interpreter (import namespace)

    """

    def __init__(self, port):
        url = 'http://localhost:' + port
        self.ready = False
        self.deferred = None
        self.queue = []
        #self.client = RPCClient(url)
        self.client = Client(url)

    def __call__(self, method, *args):
        return self.client.callRemote(method, *args)

    def initialize(self):
        return self.client.callRemote('interpreter_go').addCallbacks(
                self._engine_ready,
                self._engine_notready,
                None, None,
                None, None)

    def _engine_ready(self, result):
        self.ready = True
        return self.check_queue()

    def _engine_notready(self, reason):
        self.ready = False
        

    def call(self, method, *args):
        """try remote call
        if fail
            - queue for next good state
        """
        d = defer.Deferred()
        self.client.callRemote(method, *args).addCallbacks(
                self._callRemoteSucess,
                self._callRemoteErr,
                (d,), None,
                (d, method, args), None)
        return d 
        
    def _callRemoteSucess(self, result, d):
        d.callback(result)

    def _callRemoteErr(self, reason, d, method, *args): 
        self.ready = False
        self.queue.append((method, args))

    def check_queue(self):
        """eval requests that can't go because of a bad connection get
        saved in the queue.
        If the queue is checked, then the connection should be ready
        """
        if self.queue:
            pass
















