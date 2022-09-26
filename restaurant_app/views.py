from multiprocessing import context
from re import template
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .forms import *
from .models import *
from django.db.models import Q
from django.contrib import messages

# Create your views here.
def home_view(request):
    restaurants = User.objects.filter(role="restaurateur")[:10]
    team = Team.objects.all()
    blogs = Blog.objects.filter(status=True)
    menus = Menu.objects.filter(status=True)[:10]
    context = {'restaurants':restaurants,
               'team':team,
               'blogs':blogs,
               'menus':menus
    }
    template='index.html'
    return render(request, template, context)

def blog_view(request):
    blogs = Blog.objects.filter(status=True)
    # partie permettant de faire filtre de blog par categorie
    categorie = request.GET.get('categorie')
    if categorie:
        blogs = Blog.objects.filter(blogCategorie__slug=categorie, status=True)
    #  partie permettant de faire de recherche   
    q = request.GET.get('q')
    if q:
        blogs = Blog.objects.filter(
            Q(name__icontains=q) & Q(status=True) |
            Q(description__icontains=q) & Q(status=True)| 
            Q(blogCategorie__name__icontains=q) & Q(status=True)
        ).distinct()
    context = {'blogs':blogs}
    template='blog.html'
    return render(request, template, context)




def blog_detail_view(request, slug=None):
    blog = get_object_or_404(Blog, slug=slug)
    blogcategories = BlogCategorie.objects.filter(status=True)
    blogs = Blog.objects.filter(status=True).order_by('-Timestamp').exclude(slug=blog.slug)[:10]
    if request.method =='POST':
        form = CommentaireForm(request.POST)
        if form.is_valid():
            # partie permettant de recuperer directement le champ 
            # blog du commentaire qui devrait etre fait dans form
            obj= form.save(commit=False)
            obj.blog = blog
            form.save()
            messages.success(request, "Votre commentaire a été posté avec succés")
            # pour dire rediriger sur la page courant
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = CommentaireForm()
    context = {
        'blog':blog, 
        'form':form,
        'blogs':blogs,
        'blogcategories':blogcategories
    }
    template='blog-detail.html'
    return render(request, template,context)


def about_view(request):
    context = {}
    template='about.html'
    return render(request, template, context)





def restaurant_view(request):
    restaurants = User.objects.filter(role="restaurateur")
    q = request.GET.get('q')
    if q:
        restaurants = User.objects.filter(
            Q(name__icontains=q) & Q(role="restaurateur") |
            Q(email__icontains=q) & Q(role="restaurateur")
        ).distinct()
    context = {'restaurants':restaurants}
    template='restaurant.html'
    return render(request, template, context)



def restaurant_detail(request, id=None):
    restaurant=get_object_or_404(User, id=id, role='restaurateur')
    menus = Menu.objects.filter(status=True, restaurant=id)
    categories=Categorie.objects.filter(status=True)
    categorie = request.GET.get('categorie')
    if categorie:
        menus = Menu.objects.filter(restaurant=id, categorie__slug=categorie, status=True)
    q = request.GET.get('q')
    if q:
        menus = Menu.objects.filter(
            Q(name__icontains=q) & Q(restaurant=id) & Q(status=True) |
            Q(description__icontains=q) & Q(restaurant=id) & Q(status=True)| 
            Q(categorie__name__icontains=q) & Q(restaurant=id) & Q(status=True)
        ).distinct()
    context = {'restaurant':restaurant,
               'menus':menus,
               'categories':categories
        }
    template = 'restaurant-detail.html'
    return render(request, template, context)



def contact_view(request):
    form = ContactForm()
    if request.method =='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre message a été envoyé avec succés")
            return redirect('/contact')
    else:
        form = ContactForm()
    context = {'form':form}
    template='contact.html'
    return render(request, template, context)


def team_view(request):
    teams = Team.objects.all()
    context = {'teams':teams}
    template = 'team.html'
    return render(request, template, context)




def menu_view(request):
    menus = Menu.objects.filter(status=True)
    q = request.GET.get('q')
    if q:
        menus = Menu.objects.filter(
            Q(name__icontains=q) & Q(status=True) |
            Q(description__icontains=q) & Q(status=True)
        ).distinct()
    context={'menus':menus}
    template ='menu.html'
    return render(request, template, context)




def panier_view(request):
    context={}
    template='panier.html'
    return render(request, template, context)



def panier_add_view(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            men_id=int(request.POST.get('menus_id'))
            menus_check = Menu.objects.get(id=men_id)
            if(menus_check):
                if(Panier.objects.filter(user=request.user.id, menu=men_id)):
                    return JsonResponse({'status':"Le menus existe déjà au panier"})
                else:
                    user_instance = User.objects.get(email=request.user)
                    # men_qtite=str(request.POST.get('menu_qtite')) 
                    # if menus_check.quantite >= men_qtite:
                    Panier.objects.create(user=user_instance, menu=menus_check) 
                    return JsonResponse({'status':"Produit ajouté avec succès"})
                    # else:
                    #     JsonResponse({'status':"Seulement" + str(menus_check.quanite + "quanité non valable")})       
            else:
                return JsonResponse({'status':"Aucun menu trouvé"})
        else:
            return JsonResponse({'status':'connecter pour continuer'})
            
    return redirect('/')
    
   
def panier_view(request):
    cart =Panier.objects.filter(user=request.user)
    context = {'cart':cart}
    template ='cart.html'
    return render(request, template, context)


