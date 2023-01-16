
from random import random
import random
import string
import secrets
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.forms import FloatField
from django.utils.text import slugify
import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core import validators

from requests import request

def random_string(num):
    res = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(num))
    return str(res)






# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True
    def save_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(('The given email must be set'))
        email = self.normalize_email(email)
        user  = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        return self.save_user(email, password, **extra_fields)

    def create_staffuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = False
        
        return self.save_user(email, password, **extra_fields) 

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('is_superuser should be True'))
        extra_fields['is_staff'] = True
        return self.save_user(email, password, **extra_fields) 
    






ROLE = (
    ("client", ("client")),
    ("restaurateur", ("restaurateur")),
)

JOUR = (
    ('Lundi','Lundi'),
    ('Mardi','Mardi'),
    ('Mercredi','Mercredi'),
    ('Jeudi','Jeudi'),
    ('Vendredi','Vendredi'),
    ('Samedi','Samedi'),
    ('Dimanche','Dimanche'),
)

class User(AbstractBaseUser, PermissionsMixin):
    name       = models.CharField(max_length=250, blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    email     = models.EmailField(max_length=200, unique=True, validators = [validators.EmailValidator()])
    photo     = models.ImageField(upload_to='images', blank=True, null=True)
    address   = models.CharField(max_length=200, blank=True, null=True)
    description= models.TextField(max_length=200, blank=True, null=True)
    phone     = models.CharField(max_length=20, blank=True, null=True)
    # nni       = models.CharField(max_length=20, blank=True, null=True, unique=True)
    start_date= models.CharField(max_length=200, default='', choices = JOUR,  blank=True, null=True)
    end_date  = models.CharField(max_length=200, default='', choices = JOUR,  blank=True, null=True)
    is_staff  = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    i_agree   = models.BooleanField(blank=True, null=True, default=False)
    role      = models.CharField(max_length=100, choices=ROLE, default='client', null=True, blank=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email
    








JOUR = (
    ('Lundi','Lundi'),
    ('Mardi','Mardi'),
    ('Mercredi','Mercredi'),
    ('Jeudi','Jeudi'),
    ('Vendredi','Vendredi'),
    ('Samedi','Samedi'),
    ('Dimanche','Dimanche'),
)
class Profil(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name='user_profil')
    photo     = models.ImageField(upload_to='images', blank=True, null=True)
    address   = models.CharField(max_length=200, blank=True, null=True)
    description= models.TextField(max_length=200, blank=True, null=True)
    phone     = models.CharField(max_length=20, blank=True, null=True, unique=True)
    start_date= models.CharField(max_length=200, default='', choices = JOUR,  blank=True, null=True)
    end_date  = models.CharField(max_length=200, default='', choices = JOUR,  blank=True, null=True)
    
    def __str__(self):
        return self.user.email
    
    

# sauvegarde automatiquement les infos lorsque on creer un superuser
@receiver(post_save, sender=User)
def create_user_profil(sender, instance, created, **kwargs):
    if created:
        Profil.objects.create(user=instance)




class Categorie(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    restaurant = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    Timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True, auto_now_add=False)
    status    = models.BooleanField(default=True)
    slug      = models.SlugField(max_length=200, blank=True, null=True, editable=False, unique=False)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-Timestamp",]

# permet de mettre de mettre (-) entre les mots
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
    name = models.CharField(max_length = 200,null=False, blank = False, unique=True)
    price = models.IntegerField(default=0, null=False, blank = False)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, blank=False, null=False)
    restaurant = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    image = models.ImageField(upload_to='images', blank=False, null=False)
    quantite = models.IntegerField(blank=True, default=1, null=True)
    description = models.TextField(blank=False, null=False)
    Timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True, auto_now_add=False)
    status    = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, blank=True, null=True, editable=False, unique=False)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-Timestamp",]

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
    ('Paypal','Paypal'),
)
class Commande(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name='commande_user')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, blank=False, null=True, related_name='user_com')
    quantite = models.IntegerField(blank=True, null=True, default=1)
    restaurant = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True, related_name='commande_rstaurant')
    Timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True, auto_now_add=False)
    status    = models.BooleanField(default=False)
    ref = models.CharField(max_length=200, blank=True, null=True, unique=True)
    payement = models.CharField(max_length=200, default='Cash', choices = PAYEMENT)

    def __str__(self):
        return self.menu.name
    
    class Meta:
        ordering = ("-Timestamp",)


# partie permettant de calculer le prix total d'un produit
    def multiply(self):
        produit = self.menu.price
        quantity  = self.quantite
        return float(produit*quantity)



class BlogCategorie(models.Model):
    Timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True, auto_now_add=False)
    status    = models.BooleanField(default=True)
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    slug = models.SlugField(max_length=200, blank=True, null=True, editable=False, unique=False)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-Timestamp",]

def create_blogcategorie_slug(instance, new_slug=None):
    slug=slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    ourQuery = BlogCategorie.objects.filter(slug= slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_blogcategorie_slug(instance, new_slug=new_slug)
    return slug
def presave_blogcategorie(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_blogcategorie_slug(instance)
pre_save.connect(presave_blogcategorie, sender=BlogCategorie)
 



class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    blogCategorie = models.ForeignKey(BlogCategorie, on_delete=models.CASCADE, blank=False, null=False)
    Timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True, auto_now_add=False)
    status    = models.BooleanField(default=True)
    description = models.TextField(blank=False, null=False)
    photo     = models.ImageField(upload_to='blog', blank=True, null=True)
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    slug = models.SlugField(max_length=200, blank=True, null=True, editable=False, unique=False)

    def __str__(self):
        return self.name

def create_blog_slug(instance, new_slug=None):
    slug=slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    ourQuery = Blog.objects.filter(slug= slug)
    exists = ourQuery.exists()
    if exists:
        new_slug = "%s-%s" % (slug, ourQuery.first().id)
        return create_blog_slug(instance, new_slug=new_slug)
    return slug
def presave_blog(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_blog_slug(instance)
pre_save.connect(presave_blog, sender=Blog)
    




class Commentaire(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    email = models.EmailField(max_length=250, blank=False, null=False, unique=True)
    message = models.TextField(blank=False, null=False)
    # related_name permet d utiliser ce champ dans Blog
    blog = models.ForeignKey(Blog, blank=False, null=False, on_delete=models.CASCADE, related_name='comment_blog')
    Timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True, auto_now_add=False)
    status    = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    

class Team(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name='user_team')
    position = models.CharField(max_length=200, blank=True, null=False)
    description = models.TextField(blank=False, null=False)
    Timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True, auto_now_add=False)
    status    = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.name
    



class Contact(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    email = models.EmailField(max_length=250, blank=False, null=False, unique=True)
    sujet = models.CharField(max_length=200, blank=False, null=True)
    message = models.TextField(blank=False, null=False)
    Timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True, auto_now_add=False)
    status    = models.BooleanField(default=True)
    phone     = models.CharField(max_length=200, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name
    

class Panier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantite = models.IntegerField(blank=True, null=True, default=1)
    date_ajout = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    
    def __str__(self):
        return self.menu.name
    
    def multiply(self):
        produit = self.menu.price
        quantity  = self.quantite
        return float(produit*quantity)
    
    
    



