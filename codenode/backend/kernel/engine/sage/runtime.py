######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

import os
from django.conf import settings
from codenode.backend.kernel.engine import base



def build_env(config):
    """
    user specific variables:
        HOME
        PYTHONPATH
        SAGE_PATH


    """
    uname = os.uname()[0]
    SAGE_ROOT = config.dconfig.get('sage', 'sage_root')
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
                                [os.path.join(LIBRARY_PATH, 'python')])
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

def build_namespace():
    from codenode.backend.kernel.engine.python.introspection import introspect
    from sage.all import *
    try:
        from codenode.external.mmaplotlib.codenode_plot import show
    except ImportError:
        pass
    return locals()

def engine_startup():
    ENGINE_STARTUP="""
import sys
from codenode.backend.kernel.engine.server import EngineRPCServer
from codenode.backend.kernel.engine.sage.interpreter import Interpreter
from codenode.backend.kernel.engine.sage.runtime import build_namespace
if __name__ == "__main__":
    port = int(sys.argv[1])
    namespace = build_namespace
    print "Sage-Python XML-RPC Kernel Serving on port %s" % str(port)
    server = EngineRPCServer(('localhost', port), Interpreter, namespace)
    server.serve_forever()
"""
    return ENGINE_STARTUP


class ProcessSetup(base.ProcessSetup):

    def executable(self):
        return settings.SAGE_BINARY

    def engine_startup(self, port):
        ENGINE_STARTUP="""\
import sys
from codenode.backend.kernel.engine.server import EngineRPCServer
from codenode.backend.kernel.engine.sage.interpreter import Interpreter
from codenode.backend.kernel.engine.sage.runtime import build_namespace
namespace = build_namespace
server = EngineRPCServer(('127.0.0.1', int(%s)), Interpreter, namespace)
server.serve_forever()""" % (port)
        return ENGINE_STARTUP

    def jailed_engine_startup(self, port, root, uid):
        ENGINE_STARTUP="""
import sys
from codenode.backend.kernel.engine import base
jail = base.Jail('%s', %s)
entered = jail.enter_jail()
if not entered:
    sys.exit(1)
from codenode.backend.kernel.engine.server import EngineRPCServer
from codenode.backend.kernel.engine.sage.interpreter import Interpreter
from codenode.backend.kernel.engine.sage.runtime import build_namespace
namespace = build_namespace
server = EngineRPCServer(('127.0.0.1', %s), Interpreter, namespace)
server.serve_forever()
        """ % (root, uid, port, )
        return ENGINE_STARTUP




