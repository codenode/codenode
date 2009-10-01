######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

from twisted.cred import checkers, credentials, error
from twisted.python import log, failure
from twisted.internet import defer
from zope.interface import implements

from codenode.authority import hashpass


class NewHashedPasswordDataBaseChecker(object):
    """Compare given plain text passwords with
       hashed ones store in the database.

       Once a user (with username == avatarId) has authenticated,
       we keep the avatarId in an in-memory cache for efficiency.
    """
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,)

    def __init__(self, dbManager):
        self.dbManager = dbManager
        self.cache = {}

    def requestAvatarId(self, creds):
        try:
            avatarId = self.cache[(creds.username, creds.password)]
            return defer.succeed(avatarId)
        except KeyError:
            user = self.dbManager.get_user_for_login(creds.username)
            print 'userreqestavatar', user
            if user is None:
                return defer.fail(error.UnauthorizedLogin())
            return self.getUser(user, creds)

    def getUser(self, user, creds):
        print 'getuser', user
        avatarId, hashedpass = str(user.id), str(user.password)
        if hashpass.check_password_against_hash(creds.password, hashedpass):
            self.cache[(creds.username, creds.password)] = avatarId
            return defer.succeed(avatarId)
        else:
            return defer.fail(error.UnauthorizedLogin())


class HashedPasswordSQLDBChecker(object):
    """Compare given plain text passwords with
       hashed ones store in the database.
    """
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,)

    def __init__(self, dbManager):
        self.dbManager = dbManager

    def requestAvatarId(self, creds):
        user = self.dbManager.get_user_for_login(creds.username)
        if user is None:
            return defer.fail(error.UnauthorizedLogin())
        return self.getUser(user, creds)

    def getUser(self, user, creds):
        avatarId, hashedpass = str(user.id), str(user.password)
        if hashpass.check_password_against_hash(creds.password, hashedpass):
            return defer.succeed(avatarId)
        else:
            return defer.fail(error.UnauthorizedLogin())



class UserIDSessionKeyChecker(object):
    """Given a user id and a session id, check the database to see if
    this
    """
    


