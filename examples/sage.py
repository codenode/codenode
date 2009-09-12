import os

from codenode.backend.engine import EngineConfigurationBase

SAGE_ROOT = 'path/to/sage/install/root'

boot = """from codenode.engine.server import EngineRPCServer
from codenode.engine.sage.interpreter import Interpreter
from codenode.engine import runtime 
from codenode.engine.sage import runtime as sage_runtime
namespace = sage_runtime.build_namespace
port = runtime.find_port()
server = EngineRPCServer(('localhost', port), Interpreter, namespace)
runtime.ready_notification(port)
server.serve_forever()
"""

def build_env(sage_root):
    """
    user specific variables:
        HOME
        PYTHONPATH
        SAGE_PATH


    """
    uname = os.uname()[0]
    SAGE_ROOT = sage_root
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
    os.environ.update(env)
    return os.environ

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
    bin = os.path.join(SAGE_ROOT, 'local', 'bin', 'python')
    args = ['-c', boot]
    env = build_env(SAGE_ROOT)
    path = SAGE_ROOT

    engine_name = 'sage'

sage = Sage()







