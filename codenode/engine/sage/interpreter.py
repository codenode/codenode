######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

from codenode.engine.interpreter import Interpreter as Python
from sage.misc.preparser import preparse


class Interpreter(Python):

    def _pre_execute_filter(self, line):
        line = preparse(line)
        if line[-1] == '?':
            return 'introspect(%s, format="print")'%line[:-1]
        else:
            return line


