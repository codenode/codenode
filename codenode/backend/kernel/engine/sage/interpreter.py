
from codenode.kernel.engine.python.interpreter import Interpreter as Python
from sage.misc.preparser import preparse


class Interpreter(Python):

    def _pre_execute_filter(self, line):
        line = preparse(line)
        if line[-1] == '?':
            return 'introspect(%s, format="print")'%line[:-1]
        else:
            return line


