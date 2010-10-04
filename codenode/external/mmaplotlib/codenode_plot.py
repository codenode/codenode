import os
import sys
import uuid
import base64
from StringIO import StringIO

from pylab import show, savefig
from pylab import close as close_figure 

# cache pylab's original show function
_original_show = show

def show(fn=None, *args, **kwargs):
    s = StringIO()
    savefig(s, dpi=80, format='png', **kwargs)
    coded = base64.b64encode(s.getvalue())
    data = "__outputimage__data:image/png;base64," + coded + "__outputimage__"
    sys.stdout.write(data)
    close_figure()
    
