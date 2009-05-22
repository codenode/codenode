import os
from knoboo import settings
from knoboo.kernel.engine import base

def build_env():
    """PYTHONPATH is usefull when knoboo is not installed in the system
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
    from knoboo.kernel.engine.python.introspection import introspect
    try:
        import matplotlib
        matplotlib.use('Agg')
        from knoboo.external.mmaplotlib import knoboo_plot
        from pylab import *
        USERNAMESPACE = locals()
        USERNAMESPACE.update({"show":knoboo_plot.show, "introspect":introspect})
    except ImportError:
        USERNAMESPACE={"introspect":introspect}
    return USERNAMESPACE


class ProcessSetup(base.ProcessSetup):
    """python uses base code
    """

    def executable(self):
        return settings.PYTHON_BINARY

