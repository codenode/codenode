import os

from pylab import * 

from knoboo_plot import randomfn


# cache pylab's original show function
_original_show = show


def show(fn=None, *args, **kwargs):
    if fn is None:
        fn = randomfn() + ".png"
    realpath = os.path.join(os.path.abspath('.'), fn)
    data = "__imagefile__" + realpath 
    savefig(fn, dpi=80, **kwargs)
    print data
    