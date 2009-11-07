import os
import sys
import uuid
import pickle
from StringIO import StringIO

from pylab import show, savefig 

# cache pylab's original show function
_original_show = show

def show(fn=None, *args, **kwargs):
    fn = str(uuid.uuid4()) + '.png'
    realpath = os.path.join(os.path.abspath('.'), fn)
    savefig(realpath, dpi=80, **kwargs)
    f = open(realpath)
    s = StringIO()
    s.write(f.read())
    p = pickle.dumps(s)
    data = "__imagefile__" + p
    f.close()
    os.unlink(realpath)
    sys.stdout.write(data)
    
