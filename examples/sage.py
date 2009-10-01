######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

import os

import codenode
from codenode.backend.engine import EngineConfigurationBase

SAGE_ROOT = '/path/to/sage_root'

boot = """import sys
sys.path.append('%s')
from codenode.engine.server import EngineRPCServer
from codenode.engine.sage.interpreter import Interpreter
from codenode.engine import runtime 
from codenode.engine.sage import runtime as sage_runtime
namespace = sage_runtime.build_namespace
port = runtime.find_port()
server = EngineRPCServer(('localhost', port), Interpreter, namespace)
runtime.ready_notification(port)
server.serve_forever()
"""%(codenode.__path__[0][:-9])

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
    SAGE_DOC = os.path.join(SAGE_ROOT, 'devel', 'sage', 'doc')
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

    SINGULARPATH = os.path.join(SAGE_LOCAL, 'share', 'singular')


    DOT_SAGE = os.path.join(os.getenv('HOME'), '.sage') #kernel_env path

    MATPLOTLIBRC = DOT_SAGE


    PYTHONPATH = build_path_list(['SAGE_PATH', 'PYTHONPATH'],
                                [os.path.join(LIBRARY_PATH, 'python'),])
                                    #codenode_path])
    PYTHONHOME = SAGE_LOCAL

    SAGE_TESTDIR = os.path.join(SAGE_ROOT, 'tmp')

    LD_LIBRARY_PATH = build_path_list(['LD_LIBRARY_PATH'],
                                [LIBRARY_PATH, 
                                os.path.join(LIBRARY_PATH, 'openmpi'),
                                os.path.join(LIBRARY_PATH, 'R', 'lib')])


    if uname == 'Darwin':
        DYLD_LIBRARY_PATH =  build_path_list([
            'DYLD_LIBRARY_PATH'
            ],
            [LD_LIBRARY_PATH,
            os.path.join(SAGE_LOCAL, 'lib/R/lib')]
            )
    else:
        DYLD_LIBRARY_PATH = ''

    RHOME = os.path.join(LIBRARY_PATH, 'R')

    env = dict([('SAGE_ROOT', SAGE_ROOT),
                ('SAVEDIR', SAVEDIR),
                ('SAGE_PACKAGES', SAGE_PACKAGES),
                ('SAGE_LOCAL', SAGE_LOCAL),
                ('SAGE_DATA', SAGE_DATA),
                ('SAGE_BIN', SAGE_BIN),
                ('SAGE_DOC', SAGE_DOC),
                ('PATH', PATH),
                ('LIBRARY_PATH', LIBRARY_PATH),
                ('GP_DATA_DIR', GP_DATA_DIR),
                ('GPHELP', GPHELP),
                ('GPDOCDIR', GPDOCDIR),
                ('SINGULARPATH', SINGULARPATH),
                ('DOT_SAGE', DOT_SAGE),
                ('MATPLOTLIBRC', MATPLOTLIBRC),
                ('PYTHONPATH', PYTHONPATH),
                ('PYTHONHOME', PYTHONHOME),
                ('LD_LIBRARY_PATH', LD_LIBRARY_PATH),
                ('SAGE_TESTDIR', SAGE_TESTDIR),
                ('RHOME', RHOME),
                ('DYLD_LIBRARY_PATH',DYLD_LIBRARY_PATH)])
    environ = os.environ.copy()
    environ.update(env)
    return environ

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







