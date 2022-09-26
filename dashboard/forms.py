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
    role=forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=[('restaurateur','restaurateur'),('client','client')])
    email     = forms.EmailField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    i_agree   = forms.BooleanField(label=mark_safe(('By registering you agree to the Nubatar (<a href="/terms-and-conditions/" target="_blank">Terms of Use</a>)')), required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Password(again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['email', 'i_agree' , 'role', 'password1', 'password2']

    # def save(self, request):
    #     user = super(CustomSignupForm, self).save(request)
    #     # user.role = 'User'
    #     # user.save()
    #     # organization = Organization.objects.create(user=user)
    #     # organization.country = self.cleaned_data['country']
    #     # organization.save()
    #     return user


