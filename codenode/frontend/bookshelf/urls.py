######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

from django.conf.urls.defaults import *

from codenode.frontend.bookshelf.views import bookshelf, folders
from codenode.frontend.bookshelf.views import load_bookshelf_data, change_notebook_location
from codenode.frontend.bookshelf.views import empty_trash, new_notebook

urlpatterns = patterns('',
    url(r'^$', bookshelf, name='bookshelf'),
    url(r'^load$', load_bookshelf_data, name='load_bookshelf_data'),
    url(r'^folders$', folders, name='folders'),
    url(r'^move$', change_notebook_location, name='change_notebook_location'),
    url(r'^new$', new_notebook, name='new_notebook'),
    url(r'^emptytrash$', empty_trash, name='empty_trash'),
)
