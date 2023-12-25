from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import *


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'username', 'mail', 'password', 'password2', 'avatar']
        widgets = {
            'password': forms.PasswordInput(attrs={'name': 'password', 'type': 'password', 'autocomplete': 'off'}),
            'password2': forms.PasswordInput(attrs={'name': 'password2', 'type': 'password', 'autocomplete': 'off'}),
        }


class MyAuthenticationForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password':forms.PasswordInput(attrs={}),
        }

class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['name', 'surname', 'mail', 'password', 'avatar']