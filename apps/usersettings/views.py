from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AdminPasswordChangeForm

from apps.usersettings import models
from apps.usersettings import forms

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
        settingsform = forms.UserSettingsForm(request.POST, instance=request.user)
        if userform.is_valid():
            print "userform => ", userform.cleaned_data
            userform.save()
        if passform.is_valid():
            print "passform => ", passform.cleaned_data
            passform.save()
        if settingsform.is_valid():
            print "settingsform => ", settingsform.cleaned_data
            settingsform.save()
        return HttpResponseRedirect("/settings/")
    else:
        userform = forms.UserForm(instance=request.user)
        passform = PasswordChangeForm(request.user)
        settingsform = forms.UserSettingsForm()
    return render_to_response(template_name, {'userform':userform, 'passform':passform, 'settingsform':settingsform, 'user':request.user})


