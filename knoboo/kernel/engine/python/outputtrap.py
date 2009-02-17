"""
Trap for stdout and stderr of the python interpreter.
"""

import sys
from cStringIO import StringIO

class OutputTrap(object):

    def __init__(self):
        self.out = StringIO()
        self.err = StringIO()

    def set(self):
        """Turn on trapping"""

        if sys.stdout is not self.out:
            sys.stdout = self.out

        if sys.stderr is not self.err:
            sys.stderr = self.err

    def unset(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def reset(self):
        """return the out and err.
        close the out and err buffers and open new ones.
        """
        self.out.close()
        self.out = StringIO()
        self.err.close()
        self.err = StringIO()
        self.unset()

    def get_values(self):
        """get the strings from the out and err buffers"""
        out = self.out.getvalue()
        err = self.err.getvalue()
        return (out, err)

