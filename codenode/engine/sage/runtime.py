import os


def build_namespace():
    from codenode.engine.introspection import introspect
    from sage.all import *
    try:
        from codenode.external.mmaplotlib.codenode_plot import show
    except ImportError:
        pass
    return locals()


