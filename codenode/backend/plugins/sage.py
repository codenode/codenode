import os

from codenode.backend.engine import EngineConfigurationBase

boot = """from codenode.backend.kernel.engine.server import EngineRPCServer
from codenode.backend.kernel.engine.sage.interpreter import Interpreter
from codenode.backend.kernel.engine.sage.runtime import build_namespace
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

def build_env():
    """
    user specific variables:
        HOME
        PYTHONPATH
        SAGE_PATH


    """
    uname = os.uname()[0]
    SAGE_ROOT = '' # PUT PATH TO SAGE ROOT HERE!! <----
    SAVEDIR = SAGE_ROOT
    SAGE_PACKAGES = os.path.join(SAGE_ROOT, 'spkg')
    SAGE_LOCAL = os.path.join(SAGE_ROOT, 'local')
    SAGE_DATA = os.path.join(SAGE_ROOT, 'data')
    SAGE_BIN = os.path.join(SAGE_LOCAL, 'bin')
    if uname == 'Darwin':
        PATH = ':'.join([
            os.path.join(SAGE_LOCAL,'Frameworks/Python.framework/Versions/2.5/bin'), 
            os.getenv('PATH')
            ])
    else:
        PATH = ':'.join([SAGE_ROOT, SAGE_BIN, os.getenv('PATH')]) 

    LIBRARY_PATH = os.path.join(SAGE_LOCAL, 'lib')

    GP_DATA_DIR = os.path.join(SAGE_LOCAL, 'share', 'pari')
    GPHELP = os.path.join(SAGE_LOCAL, 'bin', 'gphelp')
    GPDOCDIR = os.path.join(SAGE_LOCAL, 'share', 'pari', 'doc')


    DOT_SAGE = os.path.join(os.getenv('HOME'), '.sage') #kernel_env path

    MATPLOTLIBRC = DOT_SAGE


    PYTHONPATH = build_path_list(['SAGE_PATH', 'PYTHONPATH'],
                                [os.path.join(LIBRARY_PATH, 'python'),])
                                    #codenode_path])
    PYTHONHOME = SAGE_LOCAL

    LD_LIBRARY_PATH = build_path_list(['LD_LIBRARY_PATH'],
                                [LIBRARY_PATH, os.path.join(LIBRARY_PATH, 'openmpi')])

    if uname == 'Darwin':
        DYLD_LIBRARY_PATH =  build_path_list([
            'DYLD_LIBRARY_PATH'
            ],
            [LD_LIBRARY_PATH,
            os.path.join(SAGE_LOCAL, 'lib/R/lib')]
            )
    else:
        DYLD_LIBRARY_PATH = ''

    env = dict([('SAGE_ROOT', SAGE_ROOT),
                ('SAVEDIR', SAVEDIR),
                ('SAGE_PACKAGES', SAGE_PACKAGES),
                ('SAGE_LOCAL', SAGE_LOCAL),
                ('SAGE_DATA', SAGE_DATA),
                ('SAGE_BIN', SAGE_BIN),
                ('PATH', PATH),
                ('LIBRARY_PATH', LIBRARY_PATH),
                ('GP_DATA_DIR', GP_DATA_DIR),
                ('GPHELP', GPHELP),
                ('GPDOCDIR', GPDOCDIR),
                ('DOT_SAGE', DOT_SAGE),
                ('MATPLOTLIBRC', MATPLOTLIBRC),
                ('PYTHONPATH', PYTHONPATH),
                ('PYTHONHOME', PYTHONHOME),
                ('LD_LIBRARY_PATH', LD_LIBRARY_PATH),
                ('DYLD_LIBRARY_PATH',DYLD_LIBRARY_PATH)])
    return env

def build_path_list(env_variables, other_paths):
    path = []
    for v in env_variables:
        if os.environ.has_key(v):
            path.append(os.getenv(v))
    if other_paths:
        path.extend(other_paths)
    path = ':'.join(path)
    return path

class Sage(EngineConfigurationBase):
    bin = '/_BASE_PATH_/sage/local/bin/python' #REPLACE _BASE_PATH_ <--
    args = ['-c', boot]
    env = build_env()
    path = '/tmp' # <----- Path where process is run


sage = Sage()







