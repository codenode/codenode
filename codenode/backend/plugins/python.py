
import os

from codenode.backend.engine import EngineConfigurationBase

boot = """from codenode.backend.kernel.engine.server import EngineRPCServer
from codenode.backend.kernel.engine.python.interpreter import Interpreter
from codenode.backend.kernel.engine.python.runtime import build_namespace
namespace = build_namespace
import sys
import socket
s = socket.socket()
s.bind(('',0))
port = s.getsockname()[1]
s.close()
del s
server = EngineRPCServer(('localhost', port), Interpreter, namespace)
sys.stdout.write('port:%s' % str(port))
server.serve_forever()
"""

print os.environ['PATH']

class Python(EngineConfigurationBase):
    bin = 'python'
    args = ['-c', boot]
    env = os.environ
    path = '/tmp'


python = Python()

