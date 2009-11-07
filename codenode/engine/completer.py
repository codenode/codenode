######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

"""
Complete partial function, variable, attribute, etc. names
Introspect an objects attributes/methods...

FIXME: need to handle errors
    example: introspect (attr_matches) on class. errors because class is a
    builtin.

"""

import rlcompleter


class Completer:
    def __init__(self, namespace=None):
        self.completer = rlcompleter.Completer(namespace)

    def global_matches(self, text):
        return self.completer.global_matches(text)

    def attr_matches(self, text):
        m = self.completer.attr_matches(text)
        m = list(set(m))
        m.sort()
        return m
