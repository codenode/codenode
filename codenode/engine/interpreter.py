######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

"""
Use a python interpreter in an Object Oriented way. 

Eventually, this will be general enough to be used for both pure python and
sage.
Things like the completer, introspection, and preparsing need to be
abstracted out completly 

"""

import sys
import re
from code import softspace, InteractiveInterpreter

#from codenode.kernel.engine.python.outputtrap import OutputTrap
#from codenode.kernel.engine.python.completer import Completer
#from codenode.kernel.engine.python.introspection import introspect
from outputtrap import OutputTrap
from completer import Completer
from introspection import introspect

class codenodeError(Exception):
    pass

class OperationAborted(codenodeError):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Interpreter(InteractiveInterpreter):

    def __init__(self, namespace=None):
        if namespace is not None:
            namespace = namespace()

        InteractiveInterpreter.__init__(self, namespace)
        self.output_trap = OutputTrap()
        self.completer = Completer(self.locals)
        self.input_count = 0
        self.interrupted = False

    def _result_dict(self, out, in_string='', err='', in_count='', cmd_count=''):
        return {'input_count':in_count, 
                    'cmd_count':cmd_count, 
                    'in':in_string, 
                    'out':out, 
                    'err':err}


    #------------------------------------------------
    # Main methods to call external
    # 
    def cancel_interrupt(self):
        self.interrupted = False
        return self._result_dict('ok')

    def evaluate(self, input_string):
        """give the input_string to the python interpreter in the
        usernamespace"""
        self.output_trap.set()
        command_count = self._runcommands(input_string)
        out_values = self.output_trap.get_values()
        self.output_trap.reset()
        self.input_count += 1
        result = {'input_count':self.input_count, 
                    'cmd_count':command_count, 
                    'in':input_string, 
                    'out':out_values[0], 
                    'err':out_values[1]}
        return result

    def introspect(self, input_string):
        """See what information there is about this objects methods and
        attributes."""
        info = introspect(input_string)

    def complete(self, input_string):
        """
        Complete a name or attribute.
        """
        reName = "([a-zA-Z_][a-zA-Z_0-9]*)$"
        reAttribute = "([a-zA-Z_][a-zA-Z_0-9]*[.]+[a-zA-Z_.0-9]*)$"
        nameMatch = re.match(reName, input_string)
        attMatch = re.match(reAttribute, input_string)
        if nameMatch:
            matches = self.completer.global_matches(input_string)
            return {'out':matches}
        if attMatch:
            matches = self.completer.attr_matches(input_string)
            return {'out':matches}
        return {'out':[]}



    def complete_name(self, input_string):
        """See what possible completions there are for this object
        (input_string)."""
        matches = self.completer.global_matches(input_string)
        # return ' '.join(matches)
        return matches

    def complete_attr(self, input_string):

        matches = self.completer.attr_matches(input_string)
        return matches


    # 
    #-----------------------------------------------

    def _runcommands(self, input_string):
        """input_string could contain multiple lines, multiple commands, or
        multiple multiline commands. This method builds a compiled command
        line by line until a complete command has been compiled. Once it
        has a complete command, it execs it in the username space and the
        output is stored in the output trap. There may be more than one
        command; the number of complete commands is counted
        (Based off of ipython1.core.shell.InteractiveShell._runlines)"""

        command_buffer = []
        command_count = 0

        if self.interrupted:
            print>>sys.stderr, 'Aborted.'
            #sys.stderr.write('Aborted')
            return command_count
        lines = input_string.split('\n')
        lines = [l for l in lines if len(l) > 0]
        more = False
        for line in lines:
            line = self._pre_execute_filter(line)
            command_buffer.append(line)
            if line or more:
                torun = '\n'.join(command_buffer)
                try:
                    more = self.runsource(torun)
                except OperationAborted, e:
                    print>>sys.stderr, e.value
                    #sys.stderr.write(e.value)
                    # XXX This could be bad if something other than the
                    # kernelConnection triggers an interrupt
                    #self.interrupted = True
                    return command_count
            if more:
                pass
            else:
                command_buffer = []
                command_count += 1
                more = False
        if more:
            command_buffer.append('\n')
            torun = '\n'.join(command_buffer)
            more = self.runsource(torun)
        return command_count

    def runcode(self, code):
        """Execute a code object.

        When an exception occurs, self.showtraceback() is called to
        display a traceback.  All exceptions are caught except
        SystemExit, which is reraised.

        A note about KeyboardInterrupt: this exception may occur
        elsewhere in this code, and may not always be caught.  The
        caller should be prepared to deal with it.

        """
        try:
            exec code in self.locals
        except SystemExit:
            raise
        except KeyboardInterrupt:
            raise OperationAborted('Interrupted')
        except:
            self.showtraceback()
        else:
            if softspace(sys.stdout, 0):
                print 

    def _pre_execute_filter(self, input_string):
        """Very simple at this point in devel.
        Look for '?' at end of a line."""
        if input_string[-1] == '?':
            return 'introspect(%s, format="print")'%input_string[:-1]
        else:
            return input_string





