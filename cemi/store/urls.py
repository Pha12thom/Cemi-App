from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('details/<int:item_id>/', views.details, name='details'),
    path("cart/", views.cart, name="cart"),
    path('add_to_cart/<int:item_id>', views.add_to_cart, name='add_to_cart'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('reduce_item_quantity/<int:item_id>', views.reduce_item_quantity, name='reduce_item_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    
   
]