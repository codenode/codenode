import os

def build_namespace():
    from codenode.engine.introspection import introspect
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

def find_port():
    import socket
    s = socket.socket()
    s.bind(('',0))
    port = s.getsockname()[1]
    s.close()
    del s
    return port

def ready_notification(port):
    """The backend process manager expects to receive a port number on
    stdout when the process and rpc server within the process are ready.
    """
    import sys
    sys.stdout.write('port:%s' % str(port))

