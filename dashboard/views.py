import imp
import profile
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from restaurant_app.models import *
from django.contrib import messages
from django.core.paginator import Paginator
from restaurant_app.forms import *
from django.contrib.auth.decorators import login_required
from allauth.account.views import PasswordChangeView




# permet de faire une redirection vers profil
class PasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('dashboard:profil')



# Create your views here.
@login_required
def home_view(request):
    commandes = Commande.objects.all()
    context = {'commandes':commandes}
    template = 'dashboard/commandes.html'
    return render(request, template, context)



@login_required
def contact_view(request):
    contacts = Contact.objects.all()
    context = {'contacts':contacts}
    template = 'dashboard/contact.html'
    return render(request, template, context)


@login_required
def contact_detail_view(request):
    contact = get_object_or_404(Contact, id=id)
    context = {'contact':contact}
    template = 'dashboard/contact-detail.html'
    return render(request, template, context)

@login_required
def contact_delete_view(request, id=id):
    contact = get_object_or_404(Contact, id=id)
    contact.delete()
    messages.success(request, "ce contact a été supprimé avec succés")
    return redirect('dashboard:contact')



@login_required
def blog_delete_view(request, slug=None):
    blog = get_object_or_404(Blog, slug=slug)
    blog.delete()
    messages.success(request, "ce blog a été supprimé avec succés")
    return redirect('dashboard:blog')



@login_required
def blog_categorie_delete_view(request, id=None):
    blogcategorie = get_object_or_404(BlogCategorie, id=id)
    blogcategorie.delete()
    messages.success(request, "cette categorie de blog a été supprimée avec succés")
    return redirect('dashboard:blogcategorie')



@login_required
def equipe_delete_view(request, id=None):
    equipe = get_object_or_404(Team, id=id)
    equipe.delete()
    messages.success(request, "ce equipe a été supprimé avec succés")
    return redirect('dashboard:equipe')



@login_required
def contact_detail_view(request, id=None):
    contact = get_object_or_404(Contact, id=id)
    context = {'contact':contact}
    template = 'dashboard/contact-detail.html'
    return render(request, template, context)



@login_required
def blog_detail_view(request, slug=None):
    blog = get_object_or_404(Blog, slug=slug)
    context = {'blog':blog}
    template = 'dashboard/blog-detail.html'
    return render(request, template, context)

@login_required
def blog_categorie_detail_view(request, slug=None):
    blogcategorie = get_object_or_404(BlogCategorie, slug=slug)
    context = {'blogcategorie':blogcategorie}
    template = 'dashboard/blog-categorie-detail.html'
    return render(request, template, context)


@login_required
def equipe_detail_view(request, id=None):
    equipe = get_object_or_404(Team, id=id)
    context = {'equipe':equipe}
    template = 'dashboard/equipe-detail.html'
    return render(request, template, context)



@login_required
def blog_modif_view(request, slug=None):
    blog = get_object_or_404(Blog, slug=slug)
    if request.method =='POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre blog a été modifié avec succés")
            return redirect('dashboard:blog')
    else:
        form = BlogForm(instance=blog)
    context = {'form':form}
    template = 'dashboard/blog-modif.html'
    return render(request, template, context)


@login_required
def blog_categorie_modif_view(request, slug=None):
    blogcategorie = get_object_or_404(BlogCategorie, slug=slug)
    if request.method =='POST':
        form = BlogCategorieForm(request.POST, instance=blogcategorie)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre categorie de blog a été modifié avec succés")
            return redirect('dashboard:blog_categorie')
    else:
        form = BlogCategorieForm(instance=blogcategorie)
    context = {'form':form}
    template = 'dashboard/blog-categorie-modif.html'
    return render(request, template, context)



@login_required
def equipe_modif_view(request, id=None):
    equipe = get_object_or_404(Team, id=id)
    if request.method =='POST':
        form = TeamForm(request.POST, instance=equipe)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre equipe a été modifié avec succés")
            return redirect('dashboard:equipe')
    else:
        form = TeamForm(instance=equipe)
    context = {'form':form}
    template = 'dashboard/equipe-modif.html'
    return render(request, template, context)




@login_required
def equipe_view(request):
    equipes = Team.objects.all()
    context = {'equipes':equipes}
    template = 'dashboard/equipe.html'
    return render(request, template, context)






@login_required
def blog_categorie_view(request):
    blogcategories = BlogCategorie.objects.all()
    context = {'blogcategories':blogcategories}
    template = 'dashboard/blog-categorie.html'
    return render(request, template, context)






@login_required
def blog_view(request):
    blogs = Blog.objects.filter(status=True)
    blogcategories = BlogCategorie.objects.filter(status=True)
    categorie = request.GET.get('categorie')
    if categorie and categorie=='all':
        blogs = Blog.objects.filter(status=True)
    elif categorie and categorie != 'all':
        blogs = Blog.objects.filter(blogCategorie__slug=categorie, status=True)
    
    paginator = Paginator(blogs, 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    context = {
        'blogs':page_obj,
        'blogcategories':blogcategories
    }
    template = 'dashboard/blog.html'
    return render(request, template, context)





@login_required
def blog_add_view(request):
    if request.method =='POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre blog a été ajouté avec succés")
            return redirect('dashboard:blog')
    else:
        form = BlogForm()
    context = {'form':form}
    template='dashboard/blog-add.html'
    return render(request, template, context)

@login_required
def blog_categorie_add_view(request):
    if request.method =='POST':
        form = BlogCategorieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre categorie blog a été ajouté avec succés")
            return redirect('dashboard:blog_categorie')
    else:
        form = BlogCategorieForm()
    context = {'form':form}
    template='dashboard/blog-categorie-add.html'
    return render(request, template, context)





@login_required
def equipe_add_view(request):
    if request.method =='POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre equipe a été ajouté avec succés")
            return redirect('dashboard:equipe')
    else:
        form = TeamForm()
    context = {'form':form}
    template='dashboard/equipe-add.html'
    return render(request, template, context)




# @login_required
# def commande_view(request):
#     commandes = Commande.objects.all()
#     context = {'commandes':commandes}
#     template = 'dashboard/commandes.html'
#     return render(request, template, context)



@login_required
def commande_detail_view(request, id=None):
    commande = get_object_or_404(Commande, id=id)
    context = {'commande':commande}
    template = 'dashboard/commande-detail.html'
    return render(request, template, context)



@login_required
def commande_add_view(request):
    if request.method =='POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            obj =form.save(commit=False)
            # ref est un champ du model commande et 
            # random_string est une fonction definie 
            # au debut du model. 4 pour que le champ
            # prendra au moins 4 caractères
            obj.ref = random_string(4)
            form.save()
            messages.success(request, "Votre commande a été ajouté avec succés")
            return redirect('dashboard:commande')
    else:
        form = CommandeForm()
    context = {'form':form}
    template='dashboard/commande-add.html'
    return render(request, template, context)


@login_required
def commande_delete_view(request, id=None):
    commande = get_object_or_404(Commande, id=id)
    commande.delete()
    messages.success(request, "cette commande a été supprimée avec succés")
    return redirect('dashboard:commande')




@login_required
def commande_modif_view(request, id=None):
    commande = get_object_or_404(Commande, id=id)
    if request.method =='POST':
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre commande a été modifié avec succés")
            return redirect('dashboard:commande')
    else:
        form = CommandeForm(instance=commande)
    context = {'form':form}
    template = 'dashboard/commande-modif.html'
    return render(request, template, context)





@login_required
def profil_view(request):
    profils = Profil.objects.all()
    context = {'profils':profils}
    template = 'dashboard/profil.html'
    return render(request, template, context)



@login_required
def menu_view(request):
    menus = Menu.objects.all()
    context = {'menus':menus}
    template = 'dashboard/menus.html'
    return render(request, template, context)


@login_required
def categorie_plat_view(request):
    categorieplats = Categorie.objects.all()
    context = {'categorieplats':categorieplats}
    template = 'dashboard/categorie-plat.html'
    return render(request, template, context)