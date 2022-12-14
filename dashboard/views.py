from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from restaurant_app.models import *
from django.contrib import messages
from django.http import JsonResponse
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
    context = {}
    template = 'dashboard/index.html'
    return render(request, template, context)

@login_required
def client_home_view(request):
    user_panier = User.objects.get(email=request.user.email)
    commandes = Commande.objects.filter(client=user_panier)
    context = {'commandes':commandes}
    template = 'dashboard/clients/home.html'
    return render(request, template, context)


@login_required
def restaurant_home_view(request):
    user_panier = User.objects.get(email=request.user.email)
    commandes = Commande.objects.filter(restaurant=user_panier)
    context = {'commandes':commandes}
    template = 'dashboard/restaurants/home.html'
    return render(request, template, context)

@login_required
def commande_modif_view(request, id=None):
    commande = get_object_or_404(Commande, id=id)
    if request.method =='POST':
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre commande a été modifié avec succés")
            return redirect('dashboard:restaurant_home')
    else:
        form = CommandeForm(instance=commande)
    context = {'form':form}
    template = 'dashboard/restaurants/commande-modif.html'
    return render(request, template, context)






@login_required
def plat_view(request):
    user = User.objects.get(email=request.user.email)
    plats = Menu.objects.filter(restaurant=user)
    context = {'plats':plats}
    template = 'dashboard/plats/plats.html'
    return render(request, template, context)



@login_required
def plat_add_view(request):
    categorie = Categorie.objects.all()
    restaurant = User.objects.filter(role="restaurateur")
    if request.method =='POST':
        form = PlatForm(request.POST, request.FILES)
        if form.is_valid():
            obj= form.save(commit=False)
            obj.categorie.id = categorie
            obj.restaurant.id = restaurant
            form.save()
            messages.success(request, "Votre plat a été ajouté avec succés")
            return redirect('dashboard:plats')
    else:
        form = PlatForm()
    context = {'form':form}
    template='dashboard/plats/plat-add.html'
    return render(request, template, context)



@login_required
def plat_modif_view(request, slug=None):
    plat = get_object_or_404(Menu, slug=slug)
    if request.method =='POST':
        form = PlatForm(request.POST, request.FILES, instance=plat)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre plat a été modifié avec succés")
            return redirect('dashboard:plats')
    else:
        form = PlatForm(instance=plat)
    context = {'form':form}
    template = 'dashboard/plats/plat-modif.html'
    return render(request, template, context)


@login_required
def plat_delete_view(request, slug=None):
    plat = get_object_or_404(Menu, slug=slug)
    plat.delete()
    messages.success(request, "ce restaurant a été supprimé avec succés")
    return redirect('dashboard:plats')

@login_required
def plat_detail_view(request, slug=None):
    plat = get_object_or_404(Menu, slug=slug)
    context = {'plat':plat}
    template = 'dashboard/plats/plat-detail.html'
    return render(request, template, context)







@login_required
def categorie_plat_view(request):
    user = User.objects.get(email=request.user.email)
    categorieplats = Categorie.objects.filter(restaurant=user)
    context = {'categorieplats':categorieplats}
    template = 'dashboard/CategoriePlats/CategoriePlats.html'
    return render(request, template, context)


@login_required
def categorieplat_add_view(request):
    if request.method =='POST':
        form = PlatCategorieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre categorie plat a été ajouté avec succés")
            return redirect('dashboard:categorie_plat')
    else:
        form = PlatCategorieForm()
    context = {'form':form}
    template='dashboard/CategoriePlats/CategoriePlats_add.html'
    return render(request, template, context)

@login_required
def categorieplat_delete_view(request, slug=None):
    categorieplat = get_object_or_404( Categorie, slug=slug)
    categorieplat.delete()
    messages.success(request, "ce catégorie de plat a été supprimé avec succés")
    return redirect('dashboard:categorie_plat')









@login_required
def restaurateur_view(request):
    authers = User.objects.filter (role="restaurateur")
    context = {'authers':authers}
    template = 'dashboard/restaurants.html'
    return render(request, template, context)



@login_required
def restaurant_modif_view(request, id=id):
    restaurant = get_object_or_404(User, id=id)
    if request.method =='POST':
        form = UserForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, "les infos de votre restaurant a été modifié avec succés")
            return redirect('dashboard:restaurant_home')
    else:
        form = UserForm(instance=restaurant)
    context = {'form':form}
    template = 'dashboard/restaurants/restaurant-modif.html'
    return render(request, template, context)




# @login_required
# def restaurant_detail_view(request, id=id):
#     restaurant = get_object_or_404(User, id=id)
#     context = {'restaurant':restaurant}
#     template = 'dashboard/restaurant-detail.html'
#     return render(request, template, context)





# @login_required
# def restaurant_delete_view(request, id=id):
#     restaurant = get_object_or_404(User, id=id)
#     restaurant.delete()
#     messages.success(request, "ce restaurant a été supprimé avec succés")
#     return redirect('dashboard:restaurants')


# @login_required
# def client_view(request):
#     clients = User.objects.filter (role="client")
#     context = {'clients':clients}
#     template = 'dashboard/client.html'
#     return render(request, template, context)



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
def blog_categorie_delete_view(request, slug=None):
    blogcategorie = get_object_or_404(BlogCategorie, slug=slug)
    blogcategorie.delete()
    messages.success(request, "cette categorie de blog a été supprimée avec succés")
    return redirect('dashboard:blog_categorie')



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
        form = TeamForm(request.POST,request.FILES, instance=equipe)
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
        form = BlogForm(request.POST, request.FILES)
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



# @login_required
# def commande_detail_view(request, id=None):
#     commande = get_object_or_404(Commande, id=id)
#     context = {'commande':commande}
#     template = 'dashboard/commande-detail.html'
#     return render(request, template, context)



# @login_required
# def commande_add_view(request):
#     if request.method =='POST':
#         form = CommandeForm(request.POST)
#         if form.is_valid():
#             obj =form.save(commit=False)
#             # ref est un champ du model commande et 
#             # random_string est une fonction definie 
#             # au debut du model. 4 pour que le champ
#             # prendra au moins 4 caractères
#             obj.ref = random_string(4)
#             form.save()
#             messages.success(request, "Votre commande a été ajouté avec succés")
#             return redirect('dashboard:commande')
#     else:
#         form = CommandeForm()
#     context = {'form':form}
#     template='dashboard/commande-add.html'
#     return render(request, template, context)


# @login_required
# def commande_delete_view(request, id=None):
#     commande = get_object_or_404(Commande, id=id)
#     commande.delete()
#     messages.success(request, "cette commande a été supprimée avec succés")
#     return redirect('dashboard:commande')










@login_required
def profil_view(request):
    profils = Profil.objects.all()
    context = {'profils':profils}
    template = 'dashboard/profil.html'
    return render(request, template, context)



# @login_required
# def menu_view(request):
#     menus = Menu.objects.all()
#     context = {'menus':menus}
#     template = 'dashboard/menus.html'
#     return render(request, template, context)





# def panier_add_view(request):
#     if request.method=="POST":
#         if request.user.is_authenticated:
#             men_id=int(request.POST.get('menus_id'))
#             menus_check = Menu.objects.get(id=men_id)
#             if(menus_check):
#                 if(Panier.objects.filter(user=request.user.id, menu=men_id)):
#                     return JsonResponse({'status':"Le menus existe déjà au panier"})
#                 else:
#                     user_instance = User.objects.get(email=request.user)
#                     # men_qtite=str(request.POST.get('menu_qtite')) 
#                     # if menus_check.quantite >= men_qtite:
#                     Panier.objects.create(user=user_instance, menu=menus_check) 
#                     return JsonResponse({'status':"Produit ajouté avec succès"})
#                     # else:
#                     #     JsonResponse({'status':"Seulement" + str(menus_check.quanite + "quanité non valable")})       
#             else:
#                 return JsonResponse({'status':"Aucun menu trouvé"})
#         else:
#             return JsonResponse({'status':'connecter pour continuer'})
            
#     return redirect('/')
    
   
# def panier_view(request):
#     cart =Panier.objects.filter(user=request.user)
#     context = {'cart':cart}
#     template ='cart.html'
#     return render(request, template, context)






