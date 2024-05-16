from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('details/<int:item_id>/', views.details, name='details'),
    path("cart/", views.cart, name="cart"),
    path('add_to_cart/<int:item_id>', views.add_to_cart, name='add_to_cart'),
    path('user_register/', views.user_register, name='user_register'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.logout, name='user_logout'),
     path('profile/', views.profile, name='profile'),
    path('reduce_item_quantity/<int:item_id>', views.reduce_item_quantity, name='reduce_item_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('shop/', views.shop, name='shop'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    
    
   
]