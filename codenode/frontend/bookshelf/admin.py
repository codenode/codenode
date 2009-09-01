######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

from django.contrib import admin

from codenode.frontend.bookshelf.models import Folder


class FolderAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', )
    search_fields = ('owner__username', 'owner__first_name', 'owner__last_name', 'title')

admin.site.register(Folder, FolderAdmin)

