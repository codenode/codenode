"""Copied from twisted.runner.procmon

Modified to suit our purposes:
    - kill all child processes upon stopping of application.

"""
import os, time
from signal import SIGTERM, SIGKILL
from twisted.python import log
from twisted.internet import protocol, reactor, process
from twisted.application import service
from twisted.protocols import basic

class LineLogger(basic.LineReceiver):

    tag = None
    delimiter = '\n'

    def lineReceived(self, line):
        log.msg('[%s] %s' % (self.tag, line))

class LoggingProtocol(protocol.ProcessProtocol):

    service = None
    name = None
    empty = 1

    def connectionMade(self):
        self.control.running = 1
        self.output = LineLogger()
        self.output.tag = self.name
        self.output.makeConnection(transport)

    def outReceived(self, data):
        self.output.dataReceived(data)
        self.empty = data[-1] == '\n'

    errReceived = outReceived

    def processEnded(self, reason):
        self.control.running = 0
        if not self.empty:
            self.output.dataReceived('\n')
        self.service.connectionLost(self.name)


class ProcessManager(service.Service):

    threshold = 1
    active = 0
    killTime = 5
    consistency = None
    consistencyDelay = 60

    def __init__(self):
        self.processes = {}
        self.protocols = {}
        self.delay = {}
        self.timeStarted = {}
        self.murder = {}

    def __getstate__(self):
        dct = service.Service.__getstate__(self)
        for k in ('active', 'consistency'):
            if dct.has_key(k):
                del dct[k]
        dct['protocols'] = {}
        dct['delay'] = {}
        dct['timeStarted'] = {}
        dct['murder'] = {}
        return dct

    def _checkConsistency(self):
        for name, protocol in self.protocols.items():
            proc = protocol.transport
            try:
                proc.signalProcess(0)
            except (OSError, process.ProcessExitedAlready):
                log.msg("Lost process %r somehow, restarting." % name)
                del self.protocols[name]
                self.startProcess(name)
        self.consistency = reactor.callLater(self.consistencyDelay,
                                             self._checkConsistency)

    def addProcess(self, process):
        """add process by actually passing in a codenode-kernel-engine
        process object
        """
        name = process.name
        if self.processes.has_key(name):
            raise KeyError("remove %s first" % name)
        self.processes[name] = process
        if self.active:
            self.startProcess(name)

    def removeProcess(self, name):
        self.stopProcess(name)
        del self.processes[name]

    def startService(self):
        service.Service.startService(self)
        self.active = 1
        for name in self.processes.keys():
            reactor.callLater(0, self.startProcess, name)
        #self.consistency = reactor.callLater(self.consistencyDelay, self._checkConsistency)

    def stopService(self):
        service.Service.stopService(self)
        self.active = 0
        for name in self.processes.keys():
            print 'stopService names', name
            self.stopProcess(name)
        #self.consistency.cancel()

    def connectionLost(self, name):
        """XXX need to adapt this still...
        """
        if self.murder.has_key(name):
            self.murder[name].cancel()
            del self.murder[name]
        if self.protocols.has_key(name):
            del self.protocols[name]
        if time.time()-self.timeStarted[name]<self.threshold:
            delay = self.delay[name] = min(1+2*self.delay.get(name, 0), 3600)
        else:
            delay = self.delay[name] = 0
        if self.active and self.processes.has_key(name):
            reactor.callLater(delay, self.startProcess, name)

    def startProcess(self, name):
        if self.processes.has_key(name):
            self.processes[name].start()

    def _forceStopProcess(self, proc):
        try:
            proc.kill()
        except process.ProcessExitedAlready:
            pass

    def stopProcess(self, name):
        if not self.processes.has_key(name):
            return
        proc = self.processes[name]
        print 'Stopping process', proc, proc.name
        
        try:
            proc.term()
        except process.ProcessExitedAlready, e:
            print 'Problem Ending Process!',e
            pass
        else:
            self.murder[name] = reactor.callLater(self.killTime, self._forceStopProcess, proc)

    def restartAll(self):
        for name in self.processes.keys():
            self.stopProcess(name)

    def __repr__(self):
        l = []
        for name, proc in self.processes.items():
            uidgid = ''
            if proc[1] is not None:
                uidgid = str(proc[1])
            if proc[2] is not None:
                uidgid += ':'+str(proc[2])

            if uidgid:
                uidgid = '(' + uidgid + ')'
            l.append('%r%s: %r' % (name, uidgid, proc[0]))
        return ('<' + self.__class__.__name__ + ' '
                + ' '.join(l)
                + '>')

