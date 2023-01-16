from .views import *
from django.urls import path

urlpatterns = [
    path('', home_view, name= 'home'),
    # path('add-to-cart', panier_add_view, name= 'addtocart'),
    # path('cart/', panier_view, name= 'cart'),
    path('about/', about_view, name= 'about'),
    path('contact/', contact_view, name= 'contact'),
    path('restaurant/', restaurant_view, name= 'restaurant'),
    path('menu/', menu_view, name= 'menu'),
    path('restaurant/<int:id>/', restaurant_detail, name= 'restaurant_detail'),
    path('team/', team_view, name= 'team'),
    path('blog/', blog_view, name= 'blog'),
    path('blog/<slug:slug>/', blog_detail_view, name= 'blogdetail'),
    

    path('cart/paniers/', cart_detail_view,name='cart_detail'),
    path('cart/cart-ajouter/<int:id>/', cart_ajouter_view,name='cart_ajouter'),
    path('cart/cart-delete/<int:id>/', cart_delete_produit_view, name='cart_delete_produit'),
    path('cart/cart-delete-panier/', cart_delete_panier_view, name='cart_delete_panier'),
    path('cart/cart-increment/<int:id>/', cart_increment_view, name='cart_increment'),
    path('cart/cart-decrement/<int:id>/', cart_decrement_view, name='cart_decrement'),
    path('cart/cart-commander/', cart_commander_view, name='cart_commander'),
    
    
    # path('checkout/', checkout, name='checkout'),
    # path('process-payment/', process_payment, name='process_payment'),
    # path('payment-done/', payment_done, name='payment_done'),
    # path('payment-cancelled/', payment_canceled, name='payment_cancelled'),
]