import os
import random
import md5
import time

def randomfn():
    "Generate random filename for images"
    randstr = "%s_%s" % (str(random.random()), str(time.time()))
    return md5.new(randstr).hexdigest()


def show(fn=None, *args, **kwargs):
    if fn is None:
        fn = randomfn() + ".png"
    realpath = os.path.join(os.path.abspath('.'), fn)
    data = "__imagefile__" + realpath 
    from pylab import *
    savefig(fn, dpi=80, **kwargs)
    print data
    

def Xshow(gobj=None, fn=None, *args, **kwargs):
    """Show a plot.

    This function takes either an Graphics object
    instance, or it attempts to render the current
    plot image from a 'pylab' session.
    """
    if fn is None:
        fn = randomfn() + ".png"
    realpath = os.path.join(os.path.abspath('.'), fn)
    base = os.path.basename(os.path.abspath('.'))
    abspath = os.path.join("/images", base, fn)
    data = "__imagefile__" + realpath 
    if gobj is not None:
        gobj.save(filename=fn, *args, **kwargs)
        print data
        return
    try:
        import pylab
    except ImportError:
        print "Please import 'pylab' for plotting"
        return
    pylab.savefig(fn, dpi=80, **kwargs)
    print data
