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

def build_env():
    """PYTHONPATH is usefull when codenode is not installed in the system
    """
    #env = {'PYTHONPATH':os.getenv('PYTHONPATH'),
    #        'HOME':os.getenv('HOME')}
    env = {}
    if os.environ.has_key('PYTHONPATH'):
        env['PYTHONPATH'] = os.getenv('PYTHONPATH') 
    if os.environ.has_key('HOME'):
        env['HOME'] = os.getenv('HOME') 
    if os.environ.has_key('PATH'):
        env['PATH'] = os.getenv('PATH') 
    return env


def build_namespace():
    from codenode.backend.kernel.engine.python.introspection import introspect
    try:
        import matplotlib
        matplotlib.use('Agg')
        from codenode.external.mmaplotlib import codenode_plot
        from pylab import *
        USERNAMESPACE = locals()
        USERNAMESPACE.update({"show":codenode_plot.show, "introspect":introspect})
    except ImportError:
        USERNAMESPACE={"introspect":introspect}
    return USERNAMESPACE


class ProcessSetup(base.ProcessSetup):
    """python uses base code
    """

    def executable(self):
        return settings.PYTHON_BINARY

