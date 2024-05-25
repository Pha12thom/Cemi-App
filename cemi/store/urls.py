from . import views
from django.urls import path

urlpatterns = [
    path('', views.shop, name='shop'),
    path('base/', views.base, name='base'),
    path('details/<int:item_id>/', views.details, name='details'),
    path("cart/", views.cart, name="cart"),
    path('add_to_cart/<int:item_id>', views.add_to_cart, name='add_to_cart'),
    path('user_register/', views.user_register, name='user_register'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
     path('user_profile/', views.user_profile, name='user_profile'),
    path('reduce_item_quantity/<int:item_id>', views.reduce_item_quantity, name='reduce_item_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('success/', views.success, name='success'),
    path('order/' , views.order, name='order'),
    path('orders/', views.orders, name='orders'),
    path('handling_404/', views.handling_404, name='handling_404'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),




]