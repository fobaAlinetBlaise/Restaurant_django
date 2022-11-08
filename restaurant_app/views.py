from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.core.paginator import Paginator
from .forms import *
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

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
    paginator = Paginator(menus, 4)
    page = request.GET.get('page')
    menus = paginator.get_page(page)
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
    cart =Panier.objects.filter(user=request.user.id)
    context = {'cart':cart}
    template ='cart.html'
    return render(request, template, context)

      
def checkoute(request):
    context = {}
    template ='checkout.html'
    return render(request, template, context)








@login_required
def cart_add(request, id):
    cart = Cart(request)
    product = Menu.objects.get(id=id)
    cart.add(product=product)
    return redirect(request.META['HTTP_REFERER'])




@login_required
def item_clear(request, id):
    cart = Cart(request)
    product = Menu.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")
    




@login_required
def item_increment(request, id):
    cart = Cart(request)
    product = Menu.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required
def item_decrement(request, id):
    cart = Cart(request)
    # if cart == 1:
    #     return messages.success(request, "La quantité minimum doit être 1")
    
    product = Menu.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required
def cart_detail(request):
    return render(request, 'cart.html')






def process_payment(request):
    # order_id = request.session.get('order_id')
    # order = get_object_or_404(Commande, id=order_id)
    
    
    # client = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, unique=True)
    # menu = models.ForeignKey(Menu, on_delete=models.CASCADE, blank=False, null=False)
    # quantite = models.IntegerField(default=1, blank=False, null=False)
    # Timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    # updated   = models.DateTimeField(auto_now=True, auto_now_add=False)
    # status    = models.BooleanField(default=True)
    # ref = models.CharField(max_length=200, blank=True, null=True, unique=True)
    # payement = models.CharField(max_length=200, default='Cash', choices = PAYEMENT)
    order = {'business': 'business'}
    # order = Commande.objects.create(
    #     client = ,
    #     menu = ,
    #     quantite = ,
    #     ref = ,
    #     payement = 
    # )
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': 100,
        'item_name': 'Order',
        'invoice': str(2),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'order': order, 'form': form})




@csrf_exempt
def payment_done(request):
    return render(request, 'payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')




def checkout(request):
    if request.method == 'POST':
        max ={}
        print("==========================")
        obj = request.POST.get("obj")
        # items = list(obj.items())
        for dict in obj:
            # for key in dict.items:
            print(obj['dict'])
        return redirect(request.META['HTTP_REFERER'])
        #     # cart.clear(request)

        #     # request.session['order_id'] = o.id
        #     return redirect('process_payment')


    else:
        return redirect(request.META['HTTP_REFERER'])
