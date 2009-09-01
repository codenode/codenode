######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

import os

from zope.interface import Interface, implements

from twisted.internet import defer

from codenode.backend.kernel.process import EngineProcessControl, KernelProcessControl 
from codenode.backend.kernel.client import RPCClient

class IEngine(Interface):

    def start():
        """Start computation engine
        """

    def stop():
        """Cleanly end engine process, possibly saving something.
        """

    def interrupt():
        """Send INT signal to process, aborting any computations.
        """

    def kill():
        """Send KILL signal to process.
        """

    def evaluate(to_evaluate):
        """Evaluate arbitrary input code in interpreter.
        return result as dictionary 
        """

    def complete_name(to_complete):
        """Tab complete: find names begining with to_complete in name
        space.
        """

    def complete_attr(to_complete):
        """Tab complete: find attributes of an object in namespace.
        """

    def introspect(to_introspect):
        """Get data about object to_introspect.
        """

class EngineObject:

    def start(self):
        pass

    def stop(self):
        pass

    def kill(self):
        #return self.control.kill()
        return self.stop()

    def interrupt(self):
        #return self.control.interrupt()
        return self.interrupt()

    def evaluate(self, to_evaluate):
        #return self.client.callRemote('evaluate', to_evaluate)
        return self.call('evaluate', to_evaluate)

    def complete_name(self, to_complete):
        #return self.call('complete_name', to_complete)
        return self.client.callRemote('complete_name', to_complete)

    def complete_attr(self, to_complete):
        #return self.call('complete_attr', to_complete)
        return self.client.callRemote('complete_attr', to_complete)

    def introspect(self, to_introspect):
        #return self.call('introspect', to_introspect)
        return self.client.callRemote('introspect', to_introspect)



class EngineManager(EngineObject):

    def __init__(self, id, mind, config, procman, user_pool=False):
        """need to add system spec in args
        """
        self.id = id
        self.mind = mind
        self.config = config
        self.procman = procman
        self.user_pool = user_pool
        self.interrupted = False
        self.client = None
        #d = self.mind.callRemote('getSystem')
        #d.addCallback(self.start)
        #self.start()

    def start(self, system):
        self.defer_ready = defer.Deferred()
        if system == 'python':
            from codenode.backend.kernel.engine.python import runtime
        elif system == 'sage':
            from codenode.backend.kernel.engine.sage import runtime
        if self.user_pool:
            try:
                self.uid = self.user_pool.pop()
                self.gid = self.user_pool.gid
            except IndexError:
                return 'Max users exceeded. Try again later.'
        else:
            self.uid = self.config['engines-uid']
            self.gid = self.uid
        process_setup = runtime.ProcessSetup(self.config, self.id, self.uid, self.gid)
        self.control = EngineProcessControl()
        self.control.buildProcess(process_setup)
        self.control.manager = self
        self.procman.addProcess(self.control)
        return self.defer_ready

    def stop(self):
        self.procman.removeProcess(self.id)

    def processStarted(self, port):
        url = 'http://localhost:' + port
        self.client = RPCClient(url)
        d = self.client.callRemote('hello')
        d.addCallback(self._engine_ready)
        return d

    def processStopped(self):
        """if the process stops for any reason, the process protocol will
        call this function.
        """
        if self.user_pool:
            self.user_pool.append(self.uid)

    def _engine_ready(self, res):
        self.client.callRemote('interpreter_go')
        self.defer_ready.callback('ok')

    def interrupt(self):
        di = self.control.interrupt()
        d = self.call('cancel_interrupt')
        d.addCallback(self._cancel_interrupt_callback)
        d.addErrback(self._cancel_interrupt_errback)
        self.set_interrupted()
        return d

    def set_interrupted(self):
        self.interrupted = True

    def cancel_interrupt(self):
        self.interrupted = False
        self.control.cancel_interrupt()

    def _cancel_interrupt_callback(self, result):
        #self.control.cancel_interrupt()
        return 'ok' 

    def _cancel_interrupt_errback(self, reason):
        return 'fail'

    def call(self, method, *args):
        """wrapper around callRemote
        """
        d = self.client.callRemote(method, *args)
        d.addCallback(self.clientCallback)
        d.addErrback(self.clientErrback)
        return d

    def clientCallback(self, result):
        """First callback after engine returns
        """
        if self.interrupted:
            self.cancel_interrupt()
        return self.output_type(result)

    def clientErrback(self, res):
        return res


    def output_type(self, output):
        """determine what the output is so eventually the browser can properly
        display it.
        """
        image_preface = "__imagefile__"
        out = output['out']
        if image_preface in out:
            image_path = out[13:]
            image_path = image_path.strip('\n')
            image_name = os.path.basename(image_path) 
            web_path = os.path.join('/data', self.id, image_name)
            web_path = '__image__' + web_path
            output['out'] = web_path
            # d = self.mind.callRemote('writeImage', image, image_name) 
            # d.addCallback(self._output_type_callback, output)
            return output
        return output

    def _output_type_callback(self, result, output):
        return output




class KernelClientManager(object):

    def __init__(self, config, procman):
        self.config = config
        self.procman = procman

    def start(self):
        self.control = KernelProcessControl(self.config)
        self.control.buildProcess()
        #self.control.start()
        self.procman.addProcess(self.control)


class UserPool(list):
    """List of uids for running engine processes
    """

    def __init__(self, maxusers, prefix='nbu', group='notebooks'):
        import pwd
        users = [prefix+str(i) for i in range(maxusers)]
        self.extend([pwd.getpwnam(user)[2] for user in users])
        self.gid = pwd.getpwnam(group)[3]




