######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

import os

from twisted.internet import protocol, reactor, defer, error

from codenode.backend.kernel.engine.python.runtime import build_env

MIN_PORT = 9000
MAX_PORT = 10000

def getUnboundPort(host='localhost', min_port=MIN_PORT, max_port=MAX_PORT):
    """Find an unbound port by attempting to bind to one with in the
    given range. On success, unbind and return the port number.
    TODO: This is blocking. This could be redone in a 'Twisted' async way (look at
    example in begining of oreilly book)
    maybe defer this to a thread...
    """
    import socket
    sock = socket.socket()
    for port in range(min_port, max_port):
        try:
            sock.bind((host, port))
            sock.close()
            return str(port)
        except socket.error:
            pass
    # in the unlikely situation that no ports were available, return 0?
    return 0


class EngineProcessProtocol(protocol.ProcessProtocol):

    def connectionMade(self):
        """A good connection indicates the engine is running.
        """
        self.control.running = 1
        self.control.started()

    def outReceived(self, data):
        """tell control what it was
        look for interrupt?
        """
        self.control.receive(data)
 
    def errReceived(self, data):
        """tell control what it was
        look for interrupt?
        """
        self.control.receive(data)

    def processEnded(self, status_object):
        """processEnded indicates the engine has stopped running.
        """
        self.control.running = 0
        self.control.stopped()

class KernelProcessProtocol(protocol.ProcessProtocol):

    def connectionMade(self):
        """A good connection indicates the kernel server is running.
        """
        self.control.running = 1

    def outReceived(self, data):
        """something
        """
        self.control.receive(data)
 
    def errReceived(self, data):
        """something
        """
        self.control.receive(data)

    def processEnded(self, status_object):
        """processEnded indicates the kernel server has stopped 
        running.
        """
        self.control.running = 0
        self.control.get_twistd_pid()


class BaseProcessControl(object):

    processProtocol = protocol.ProcessProtocol
    executable = None
    args = ()
    env = {}
    path = None
    uid = None
    gid = None
    usePTY = 0
    childFDs = None

    def __init__(self, config):
        self.config = config

    def buildProtocol(self):
        p = self.processProtocol()
        p.control = self
        return p

    def start(self):
        """Spawn a process
        """
        try:
            reactor.spawnProcess(self.protocol,
                                        self.executable,
                                        args=self.args,
                                        env=self.env,
                                        path=self.path,
                                        uid=self.uid,
                                        gid=self.gid,
                                        usePTY=self.usePTY,
                                        childFDs=self.childFDs)
        except OSError, e:
            print 'SPAWN ERROR',e
            raise

    def kill(self):
        self.protocol.transport.signalProcess('KILL')

    def interrupt(self):
        self.protocol.transport.signalProcess('INT')

    def term(self):
        self.protocol.transport.signalProcess(15)

    def receive(self, data):
        """Do something with stdout/err
        """

class EngineProcessControl(BaseProcessControl):
    """
    Provides control interface to specific instance of a computation engine

    """

    processProtocol = EngineProcessProtocol
    executable = 'python'

    def __init__(self):
        self.intsig = None
        self.deferred = None

    def receive(self, data):
        """Catch process output
        """
        print 'Engine log: ', data

    def buildProcess(self, setup):
        self.name = setup.id
        self.port = getUnboundPort()
        self.protocol = self.buildProtocol()
        self.executable = setup.executable()
        self.args = setup.args(self.port)
        self.env = setup.env()
        self.path = setup.path()
        self.uid = setup.uid()
        self.gid = setup.uid()
        setup.write_startup_file()

    def started(self):
        self.manager.processStarted(self.port)

    def stopped(self):
        self.manager.processStopped()

    def interrupt(self):
        """Interrupt computation by repeatedly sending INT signal.
        The EngineProtocol will receive a message on stdout when the
        interpreter has been interrupted.

        return an empty deferred.
        """
        if self.deferred is None:
            self.deferred = defer.Deferred()
            self._interrupt(0)
            return self.deferred
        return 'Already interrupting'

    def _interrupt(self, trys):
        interval = 0.01
        self.intsig = None
        trys +=1
        self.protocol.transport.signalProcess('INT')
        if trys < 20:
            self.intsig = reactor.callLater(interval, self._interrupt, trys)
        else:
            self.deferred.callback('Interrupt Max Retry')
            self.deferred = None

    def cancel_interrupt(self):
        """Process Protocol told us the server caught a KeyboardInterrupt
        exception.
        """
        if self.intsig is not None:
            self.intsig.cancel()
            self.intsig = None
        if self.deferred is not None:
            self.deferred.callback('Interrupted')
            self.deferred = None


class KernelProcessControl(BaseProcessControl):

    processProtocol = KernelProcessProtocol
    pidfilename = 'codenode-kernel.pid'

    def __init__(self, config):
        self.config = config
        self.name = 'kernel-server'
        self.executable = "twistd" #XXX 

    def receive(self, data):
        """
        """
        print 'Kernel Log: \n', data #XXX Implement better logging.

    def get_twistd_pid(self):
        pidfile = os.path.join(self.path, self.pidfilename)
        f = file(pidfile, 'r')
        self.twistdpid = f.read()
        f.close()
        self.protocol.transport.pid = int(self.twistdpid)

    def buildProcess(self):
        self.protocol = self.buildProtocol()
        self.path = self.config.kernel['kernel_path']
        if self.config.kernel['kernel_host'] == 'localhost':
            min_port = int(self.config.kernel['kernel_port'])
            self.server_port = str(getUnboundPort(min_port=min_port))
            self.config.kernel['kernel_port'] = self.server_port
        else:
            self.server_port = self.config.kernel['kernel_port']
        self.args = (self.executable, '-n', '--pidfile=%s' % self.pidfilename, 'codenode-kernel',)
        self.env = build_env()

