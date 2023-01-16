from tkinter import Widget
from unicodedata import name
from MySQLdb import ROWID
from django import forms
from .models import *
from django.utils.safestring import mark_safe

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from allauth.account.forms import SignupForm
User = get_user_model()







class CustomSignupForm(UserCreationForm):
    # role=forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=[('restaurateur','restaurateur'),('client','client')])
    first_name     = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name     = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email     = forms.EmailField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    i_agree   = forms.BooleanField(label=mark_safe(('Etes-vous Sùr? (<a href="#" target="_blank">Terme Utilisation</a>)')), required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Password(again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['email', 'i_agree' , 'first_name', 'last_name', 'password1', 'password2']




