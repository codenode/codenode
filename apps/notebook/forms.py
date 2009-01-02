from django import forms

class ShareNotebook(forms.Form):
    shared_user_list = forms.CharField(widget=forms.Textarea)

