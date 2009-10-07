######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

"""
Simple http client for app engine kernel requests

April 2009
"""

import urllib2

from twisted.internet import defer
from twisted.web.client import getPage


class RemoteKernel(object):
    """Client for app engine kernel. 
    App engine kernel is very simple. The app implements both the 'kernel'
    functionality (managing engines) and the 'engine' functionality
    (interpreter session).
    """

    def __init__(self, url, session=None):
        self.url = url
        self.session = session
        self.input_count = 0 #hack

    @defer.inlineCallbacks
    def start(self):
        if self.session is None:
            url = self.url + '/sessionmanager'
            res = yield getPage(url)
            self.session = res
        defer.returnValue('ok')


    @defer.inlineCallbacks
    def evaluate(self, input):
        """
        """
        statement = urllib2.quote(input)
        url = self.url + '/evaluate?'
        url += '&session=%s'%self.session
        url += '&statement=%s'%statement
        res = yield getPage(url)
        self.input_count += 1
        res_dict = {'input_count':self.input_count,
                'out':res,
                'err':''}
        defer.returnValue(res_dict)

    @defer.inlineCallbacks
    def complete_name(self, input):
        """
        """
        statement = urllib2.quote(input)
        url = self.url + '/complete?'
        url += '&session=%s'%self.session
        url += '&statement=%s'%statement
        res = yield getPage(url)
        defer.returnValue(res)

    @defer.inlineCallbacks
    def complete_attr(self, input):
        """
        """
        statement = urllib2.quote(input)
        url = self.url + '/complete_attr?'
        url += '&session=%s'%self.session
        url += '&statement=%s'%statement
        res = yield getPage(url)
        defer.returnValue(res)

    def kill(self):
        """N/A
        """
        return 

    def interrupt(self):
        return



class EngineFactory(object):

    def newEngine(self, url, *args):
        return RemoteKernel(url)


