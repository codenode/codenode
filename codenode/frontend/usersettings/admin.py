######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as UserAdminDefault
from codenode.frontend.usersettings.models import UserSettings

class UserSettingsInline(admin.StackedInline):
    model = UserSettings

class UserAdmin(UserAdminDefault):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    inlines = [UserSettingsInline,]

#unregister the default so we can use our own:
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

