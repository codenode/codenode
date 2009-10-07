######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

from django.forms import ModelForm
from django.contrib.auth.models import User

from codenode.frontend.usersettings.models import UserSettings

class UserForm(ModelForm):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class UserSettingsForm(ModelForm):
    
    class Meta:
        model = UserSettings
        fields = ('notebook_opens_in_new_window',)

