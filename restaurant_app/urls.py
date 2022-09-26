from .views import *
from django.urls import path


urlpatterns = [
    path('', home_view, name= 'home'),
    path('add-to-cart', panier_add_view, name= 'addtocart'),
    path('cart/', panier_view, name= 'cart'),
    path('about/', about_view, name= 'about'),
    path('contact/', contact_view, name= 'contact'),
    path('restaurant/', restaurant_view, name= 'restaurant'),
    path('menu/', menu_view, name= 'menu'),
    path('restaurant/<int:id>/', restaurant_detail, name= 'restaurant_detail'),
    path('team/', team_view, name= 'team'),
    path('blog/', blog_view, name= 'blog'),
    path('blog/<slug:slug>/', blog_detail_view, name= 'blogdetail'),
]