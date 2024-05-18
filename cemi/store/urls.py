from . import views
from django.urls import path

urlpatterns = [
    path('', views.user_register, name='user_register'),
    path('base/', views.base, name='base'),
    path('details/<int:item_id>/', views.details, name='details'),
    path("cart/", views.cart, name="cart"),
    path('add_to_cart/<int:item_id>', views.add_to_cart, name='add_to_cart'),
    path('home/', views.home, name='home'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
     path('profile/', views.profile, name='profile'),
    path('reduce_item_quantity/<int:item_id>', views.reduce_item_quantity, name='reduce_item_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('success/', views.success, name='success'),
    path('welcome/', views.welcome, name='welcome'),
    path('order/' , views.order, name='order')
    
   
]