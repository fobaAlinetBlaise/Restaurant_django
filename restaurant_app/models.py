from genericpath import exists
from math import fabs
from random import random
import secrets
import string
from unicodedata import name
from weakref import ref
from xmlrpc.client import Boolean
from MySQLdb import Timestamp
import random
import string
import secrets
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
import os

# Create your models here.

def renomer_image(instance, filename):
    upload_to = 'image/'
    ext = filename.split('.')[-1]
    if instance.user.username:
        filename = "photo/{}.{}".format(instance.user.username, ext)
    return os.path.join(upload_to, filename)


def random_string(num):
    res = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(num))
    return str(res)




USER_TYPE = (
    ('client','client'),
    ('restaurateur','restaurateur'),
    ('administrateur','administrateur'),
)
class Profil(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name='user_profil')
    photo     = models.ImageField(upload_to=renomer_image, blank=True, null=True)
    address   = models.CharField(max_length=200, blank=True, null=True)
    name      = models.CharField(max_length=200, blank=True, null=True)
    description= models.TextField(max_length=200, blank=True, null=True)
    phone     = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(max_length=200, default='client', choices = USER_TYPE,  blank=False, null=False)
    start_date= models.DateField(blank=True, null=True)
    end_date  = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender= User)
def create_user_profil(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            Profil.objects.create(user = instance, user_type='administrateur')
        else:
            Profil.objects.create(user = instance)




class Categorie(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    restaurant = models.ForeignKey(Profil, on_delete=models.CASCADE, blank=False, null=False)
    Timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True, auto_now_add=False)
    status    = models.BooleanField(default=True)
    slug      = models.SlugField(max_length=200, blank=True, null=True, editable=False, unique=False)

    def __str__(self):
        return self.name

def create_cateorie_slug(instance, new_slug=None):
    slug=slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    ourQuery = Categorie.objects.filter(slug= slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_cateorie_slug(instance, new_slug=new_slug)
    return slug
def presave_categorie(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_cateorie_slug(instance)
pre_save.connect(presave_categorie, sender=Categorie)






class Menu(models.Model):
    name = models.CharField(max_length = 200,null=False, blank = False)
    prix = models.IntegerField(default=0, null=False, blank = False)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, blank=False, null=False)
    restaurant = models.ForeignKey(Profil, on_delete=models.CASCADE, blank=False, null=False)
    photo = models.ImageField(upload_to='images', blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    Timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True, auto_now_add=False)
    status    = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, blank=True, null=True, editable=False, unique=False)

    def __str__(self):
        return self.name

def create_menu_slug(instance, new_slug=None):
    slug=slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    ourQuery = Menu.objects.filter(slug= slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_menu_slug(instance, new_slug=new_slug)
    return slug
def presave_menu(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_menu_slug(instance)
pre_save.connect(presave_menu, sender=Menu)
 
 
 
 
PAYEMENT = (
    ('Cash','Cash'),
)
class Commande(models.Model):
    client = models.ForeignKey(Profil, on_delete=models.CASCADE, blank=False, null=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, blank=False, null=False)
    quantite = models.IntegerField(default=1, blank=False, null=False)
    Timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True, auto_now_add=False)
    status    = models.BooleanField(default=True)
    ref = models.CharField(max_length=200, blank=True, null=True)
    payement = models.CharField(max_length=200, default='Cash', choices = PAYEMENT)

    def __str__(self):
        return self.menu.name

