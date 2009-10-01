######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################



def introspect(item, format='print'):
    """Print useful information about item."""
    if item == '?':
        print 'Type <object>? for info on that object.'
        return
    _name = 'N/A'
    _class = 'N/A'
    _doc = 'No Documentation.'
    if hasattr(item, '__name__'):
        _name = item.__name__
    if hasattr(item, '__class__'):
        _class = item.__class__.__name__
    _id = id(item)
    _type = type(item)
    _repr = repr(item)
    if callable(item):
        _callable = "Yes"
    else:
        _callable = "No"
    if hasattr(item, '__doc__'):
        _doc = getattr(item, '__doc__')
        _doc = _doc.strip()   # Remove leading/trailing whitespace.
    info = {'name':_name, 'class':_class, 'type':_type, 'repr':_repr, 'doc':_doc}
    if format is 'print':
        for k,v in info.iteritems():
            print k.capitalize(),': ', v
        return
    elif format is 'dict':
        return info

