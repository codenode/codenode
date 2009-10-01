######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

import sys
#import logging as log
from SimpleXMLRPCServer import SimpleXMLRPCServer



class EngineRPCServer(SimpleXMLRPCServer):

    def __init__(self, addr, interpreter, namespace):
        SimpleXMLRPCServer.__init__(self, addr)
        self.user_namespace = namespace
        self._interpreter = interpreter
        self.interpreter = self._interpreter(self.user_namespace)

    def _dispatch(self, method, params):
        try:
            func = getattr(self, 'xmlrpc_' + method)
        except AttributeError:
            raise Exception('method %s is not supported' % method)
        else:
            return func(*params)

    def serve_forever(self):
        sys.stdout.flush()
        while True:
            try:
                self.handle_request()
            except KeyboardInterrupt:
                #sys.stderr.flush()
                #sys.stdout.flush()
                continue

    def xmlrpc_hello(self):
        return 'hi'

    def xmlrpc_interpreter_go(self):
        self.interpreter = self._interpreter(self.user_namespace)
        return 'ON'

    def xmlrpc_evaluate(self, to_evaluate):
        """Evaluate code in the python interpreter.
        return a dict containing:
            - stdout 
            - stderr
            - original input (source)
            - number of commands source contained
        """
        try:
            result = self.interpreter.evaluate(to_evaluate)
        except AttributeError:
            result = 'Interpreter Error: Interpeter is probably starting up.'
        return result

    def xmlrpc_complete(self, to_complete):
        """Search for possible completion matches of source in the
        usernamespace.
        return a list of matches
        """
        try:
            result = self.interpreter.complete(to_complete)
        except AttributeError:
            result = 'Interpreter Error: Interpeter is probably starting up.'
        return result


    def xmlrpc_complete_name(self, to_complete):
        """Search for possible completion matches of source in the
        usernamespace.
        return a list of matches
        """
        try:
            result = self.interpreter.complete_name(to_complete)
        except AttributeError:
            result = 'Interpreter Error: Interpeter is probably starting up.'
        return result

    def xmlrpc_complete_attr(self, to_complete):
        """Get the attributes/methods of an object (source).
        return them in a list
        """
        try:
            result = self.interpreter.complete_attr(to_complete)
        except AttributeError:
            result = 'Interpreter Error: Interpeter is probably starting up.'
        return result

    def xmlrpc_introspect(self, to_introspect):
        """Introspect on an object
        """
        try:
            result = self.interpreter.introspect(to_introspect)
        except AttributeError:
            result = 'Interpreter Error: Interpeter is probably starting up.'
        return result

    def xmlrpc_cancel_interrupt(self):
        """Reset interpreters interrupt state
        """
        result = self.interpreter.cancel_interrupt()
        return result




