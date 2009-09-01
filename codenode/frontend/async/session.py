######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

import random
import time
import md5

from twisted.internet import task, defer
from twisted.cred import credentials
from zope.interface import implements
from codenode.external.twisted.web2 import iweb
from codenode.external.twisted.web2 import server, resource


class Session(object):
    """A single users session, defined by the uid.
    """
    def __init__(self, uid, sessionManager):
        self.uid = uid #the cookie, a unique identifier (md5 hash)
        self.creationTime = self.lastAccessed = time.time()
        self.sessionManager = sessionManager
        self.authenticatedAs = None
        #self.setLifetime(60)
    
    def set_authCreds(self, creds):
        self.authenticatedAs = creds

    def get_authCreds(self):
        return self.authenticatedAs

    def get_uid(self):
        return self.uid

    def touch(self):
        self.lastAccessed = time.time()

    def setAvatar(self, avatar):
        self.avatar = avatar

    def getAvatar(self):
        return self.avatar

    def getResource(self):
        return self.avatar[0]

    def logout(self):
        res, logout = self.avatar
        logout()

class codenodeSession(Session):
    """A single users session that has associated running notebooks
    """

    def __init__(self, uid, sessionManager):
        Session.__init__(self, uid, sessionManager)
        self.uid = uid 
        self.creationTime = self.lastAccessed = time.time()
        self.sessionManager = sessionManager
        self.authenticatedAs = None

class SessionManager(object):
    """Manages all logged in users' sessions.
    """
    tickTime = 10000 #SESSION_CLEAN_FREQUENCY
    sessionLifetime = 1000000 #TRANSIENT_SESSION_LIFETIME
    sessionPersistentLifetime = 1000000 #PERSISTENT_SESSION_LIFETIME
    
    sessionFactory = codenodeSession
    
    def __init__(self):
        self.sessions = {}
        self.tick = task.LoopingCall(self._tick)

    def createSession(self):
        session = self.sessionFactory(self.createSessionID(), self)
        uid = session.get_uid()
        self.sessions[uid] = session
        if not self.tick.running and len(self.sessions) > 0:
            self.tick.start(self.tickTime)
        return uid
    
    def expireSession(self, session):
        session.logout()
        uid = session.get_uid()
        del self.sessions[uid]

    def getSession(self, uid):
        session = self.sessions.get(uid, None)
        if session:
            session.touch()
        return session

    def createSessionID(self):
        """Generate a new session ID."""
        data = "%s_%s" % (str(random.random()) , str(time.time()))
        return md5.new(data).hexdigest()

    def _tick(self):
        """Remove expired sessions.
        """
        now = time.time()
        for uid, session in self.sessions.items():
            age = now - session.lastAccessed
            max = self.sessionLifetime
            #if session.persistent:
            #    max = self.sessionPersistentLifetime
            if age > max:
                self.expireSession(session)
        if not self.sessions and self.tick.running:
            self.tick.stop()


class MindManager(object):
    """The only use of the mind is to pass the session id to the avatar.
    The Login resource sets the users cookie with this session id as 'sid'
    """
    def __init__(self, uid):
        self.sid = uid

class SessionWrapper(object):
    """This wrapper acts as a state-full layer for HTTP requests.

    Every request is the result of a client using the HTTP protocol to
    connect to this server system, therefore, every request must be
    authenticated so that the server can decide how to handle the request.
    The result of a request is a resource tree. A persistent connection is
    simulated by storing the resource tree in an avatar the first time it
    is created. Later requests for that same resource refer to the avatar.

    The session holds on to 'avatars' dealt out by the 'realm'.
    The 'portal' authenticates 'credentials', associating them with an
    avatarId upon successful authentication.

    This wrapper implements iweb.IResource, therefore, it must provide two
    methods for the framework to call:
     - locateChild(req, segments)
       return (resource, remaining-path-segments)
     - renderHTTP(req)
     
     (documentation on those exists in web2.iweb and web2.resource)

    
    server.Site takes in something that implements IResource

    This is like an adapter. It makes the portal look like a resource.

    The portal has two main methods
     - login
     - registerChecker

    This adapter calls login (registerChecker should be called on the
    portal before it is adapted)
    """
    implements(iweb.IResource)

    credInterface = iweb.IResource

    mindFactory = MindManager

    def __init__(self, portal):
        self.portal = portal
        self.sessionManager = SessionManager()

    def locateChild(self, request, segments):
        """Before returning a resource and segments, determine what
        resource to fetch by checking the following conditions:
          - (authenticated user) request has cookie with valid session id
            return users resource tree
          - (authenticating user) request is a POST with username password
            credentials and path is 'login'
              return users resource tree if authenticated, or an anonymous
              resource tree otherwise
          - (anonymous user) request may have invalid credentials, or no
            credentials
              return an anonymous resource tree
        """
        session = self.getSession(request)
        if session:
            if segments[0] == 'logout':
                self.sessionManager.expireSession(session)
                return self.anonymousLogin(request, segments)
            res = session.getResource()
            return res, segments 
        if segments[0] == 'login':
            d = server.parsePOSTData(request)
            d.addCallback(lambda _: self.login(request, segments))
            return d
            #return self.login(request, segments)
        return self.anonymousLogin(request, segments)

    def renderHTTP(self, request):
        return http.Response(responsecode.NOT_FOUND)

    def login(self, request, segments):
        """Attempt to login an unauthenticated user
        Create a tentative session for this login.
        Upon success, store the session and return the avatar.
        Upon failure, return an anonymous avatar.
        """
        creds = self.getCredentials(request)
        uid = self.sessionManager.createSession()
        mind = self.mindFactory(uid)
        return self.portal.login(
                creds, 
                mind, 
                self.credInterface).addCallbacks(
                        self._loginSucceedded,
                        self._loginFailed,
                        (uid, segments,), None,
                        (request, segments,), None)

    def getSession(self, request):
        """check request for session id.
        In this case, the cookie is checked.
        Session id's could also live in the url
        """
        cookiedata = request.headers.getHeader('cookie')
        cookie = ''
        if cookiedata:
            for c in cookiedata:
                if c.name == 'sessionid':
                    cookie = c.value
        session = self.sessionManager.getSession(cookie)
        return session
 
    def anonymousLogin(self, request, segments):
        creds = credentials.Anonymous()
        return self.portal.login(creds, None,
                self.credInterface).addCallback(lambda a: (a[1], segments))

    def _loginSucceedded(self, (iface, res, logout), uid, segments):
        self.sessionManager.sessions[uid].setAvatar((res, logout))
        return res, segments

    def _loginFailed(self, res, request, segments):
        return self.anonymousLogin(request, segments)

    def getCredentials(self, request):
        """Get username, password from post args.
        """
        username = request.args.get('username', [''])[0]
        password = request.args.get('password', [''])[0]
        return credentials.UsernamePassword(username, password)


