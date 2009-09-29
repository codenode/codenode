
import os

from codenode.backend.engine import EngineConfigurationBase

boot = """from codenode.engine.server import EngineRPCServer
from codenode.engine.interpreter import Interpreter
from codenode.engine import runtime
namespace = runtime.build_namespace
port = runtime.find_port()
server = EngineRPCServer(('localhost', port), Interpreter, namespace)
runtime.ready_notification(port)
server.serve_forever()
"""


class Python(EngineConfigurationBase):
    bin = 'python'
    args = ['-c', boot]
    env = os.environ
    path = os.path.expanduser('~')


python = Python()

