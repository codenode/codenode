######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AdminPasswordChangeForm

from codenode.frontend.usersettings import models
from codenode.frontend.usersettings import forms

@login_required
def usersettings(request, template_name='usersettings/usersettings.html'):
    """Render a Users settings page.

    If this is the first time a user is visting the settings page,
    a default settings instance is created for this user.
    """
    try:
        profile = request.user.get_profile()
    except models.UserSettings.DoesNotExist:
        s = models.UserSettings(user=request.user)
        s.save()
        profile = request.user.get_profile()
    if request.method == "POST":
        userform = forms.UserForm(data=request.POST, instance=request.user)
        passform = PasswordChangeForm(request.user, data=request.POST)
        settingsform = forms.UserSettingsForm(data=request.POST, instance=profile)
        if userform.is_valid():
            userform.save()
        if passform.is_valid():
            passform.save()
        if settingsform.is_valid():
            settingsform.save()
        return HttpResponseRedirect("/bookshelf/")
    else:
        userform = forms.UserForm(instance=request.user)
        passform = PasswordChangeForm(request.user)
        settingsform = forms.UserSettingsForm(instance=profile)
    return render_to_response(template_name, {'userform':userform, 'passform':passform, 'settingsform':settingsform, 'user':request.user})


