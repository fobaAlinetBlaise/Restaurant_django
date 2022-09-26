from .views import *
from django.urls import path



app_name='dashboard'

urlpatterns = [
    path('', home_view, name= 'home'),
    path('contact/', contact_view, name= 'contact'),
    path('equipe/', equipe_view, name= 'equipe'),
    path('equipe/detail/<int:id>/', equipe_detail_view, name= 'equipe_detail'),
    path('equipe/modif/<int:id>/', equipe_modif_view, name= 'equipe_modif'),
    path('equipe/delete/<int:id>/', equipe_delete_view, name='equipe_delete'),
    path('equipe/add/', equipe_add_view, name= 'equipe_add'),
    path('contact/delete/<int:id>/', contact_delete_view, name='contact_delete'),
    path('blog/delete/<slug:slug>/', blog_delete_view, name='blog_delete'),
    path('contact/detail/<int:id>/', contact_detail_view, name= 'contact_detail'),
    path('blog/detail/<slug:slug>/', blog_detail_view, name= 'blog_detail'),
    path('blog/modif/<slug:slug>/', blog_modif_view, name= 'blog_modif'),
    path('blog/', blog_view, name= 'blog'),
    # path('cart/', panier_view, name= 'cart'),
    path('commande/add/', commande_add_view, name= 'commande_add'),
    path('commande/modif/<int:id>/', commande_modif_view, name= 'commande_modif'),
    path('commande/delete/<int:id>/', commande_delete_view, name='commande_delete'),
    path('commande/detail/<int:id>/', commande_detail_view, name= 'commande_detail'),
    path('profil/', profil_view, name= 'profil'),
    path('blogcategorie/', blog_categorie_view, name= 'blog_categorie'),
    path('blogcategorie/delete/<int:id>/', blog_categorie_delete_view, name='blog_categorie_delete'),
    path('blogcategorie/modif/<slug:slug>/', blog_categorie_modif_view, name= 'blog_categorie_modif'),
    path('blogcategorie/detail/<slug:slug>/', blog_categorie_detail_view, name= 'blog_categorie_detail'),
    path('blogcategorie/add/', blog_categorie_add_view, name= 'blog_categorie_add'),
    path('blog/add/', blog_add_view, name= 'blog_add'),
    path('menu/', menu_view, name= 'menu'),
    path('categorieplat/', categorie_plat_view, name= 'categorie_plat'),
]