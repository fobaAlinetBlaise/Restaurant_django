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
    
    
    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('cart/cart-detail/', cart_detail,name='cart_detail'),
    
    
    path('checkout/', checkout, name='checkout'),
    path('process-payment/', process_payment, name='process_payment'),
    path('payment-done/', payment_done, name='payment_done'),
    path('payment-cancelled/', payment_canceled, name='payment_cancelled'),
]