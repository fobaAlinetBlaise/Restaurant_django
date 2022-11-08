from tkinter import Widget
from MySQLdb import ROWID
from django import forms
from .models import *
from django.utils.safestring import mark_safe

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from allauth.account.forms import SignupForm
User = get_user_model()



class ContactForm(forms.ModelForm):
    class Meta:
        model= Contact
        fields= [
            'name',
            'email',
            'sujet',
            'message',
            'phone'
        ]
        
        Widgets= {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'sujet': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.TextInput(attrs={'class': 'form-control', 'row':1, 'cols':30}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }



# pas besoin du champ blog aui est cle etrangere 
# on gere depuis view afin de ne pas avoir une liste à selectionner
class CommentaireForm(forms.ModelForm):
    class Meta:
        model= Commentaire
        fields= [
            'name',
            'email',
            'message',
        ]
        
        Widgets= {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.TextInput(attrs={'class': 'form-control', 'row':1, 'cols':30}),
        }
        




class ContactForm(forms.ModelForm):
    class Meta:
        model= Contact
        fields= [
            'name',
            'email',
            'sujet',
            'message',
            'phone'
        ]
        
        Widgets= {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'sujet': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.TextInput(attrs={'class': 'form-control', 'row':1, 'cols':30}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
        






class CommandeForm(forms.ModelForm):
    class Meta:
        model= Commande
        fields= [
            'client',
            'ref',
            'price',
            'payement'
        ]
        
        Widgets= {
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'ref': forms.TextInput(attrs={'class': 'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'payement': forms.TextInput(attrs={'class': 'forml'}),
        }






class TeamForm(forms.ModelForm):
    class Meta:
        model= Team
        fields= [
            'user',
            'position',
            'description',
        ]
        
        Widgets= {
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'row':1, 'cols':30}),
        }



# pas besoin du champ blog aui est cle etrangere 
# on gere depuis view afin de ne pas avoir une liste à selectionner
class BlogForm(forms.ModelForm):
    class Meta:
        model= Blog
        fields= [
            'user',
            'blogCategorie',
            'name',
            'photo',
            'description',
        ]
        
        Widgets= {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'row':1, 'cols':30}),
        }
        
        
        
class BlogCategorieForm(forms.ModelForm):
    class Meta:
        model= BlogCategorie
        fields= [
            'name',
        ]
        
        Widgets= {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        
