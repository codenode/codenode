import os
#from django.conf import settings
#from codenode.backend.kernel.engine import base






def build_namespace():
    from codenode.backend.kernel.engine.python.introspection import introspect
    from sage.all import *
    try:
        from codenode.external.mmaplotlib.codenode_plot import show
    except ImportError:
        pass
    return locals()


