from django.forms import ModelForm
from django.contrib.auth.models import User

from knoboo.frontend.usersettings.models import UserSettings

class UserForm(ModelForm):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class UserSettingsForm(ModelForm):
    
    class Meta:
        model = UserSettings
        fields = ('notebook_opens_in_new_window',)

