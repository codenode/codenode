import os
import sys
import uuid
import pickle
from StringIO import StringIO

from pylab import show, savefig
from pylab import close as close_figure 

# cache pylab's original show function
_original_show = show

def show(fn=None, *args, **kwargs):
    s = StringIO()
    savefig(s, dpi=80, **kwargs)
    p = pickle.dumps(s)
    data = "__outputimage__" + p + "__outputimage__"
    sys.stdout.write(data)
    close_figure()
    
