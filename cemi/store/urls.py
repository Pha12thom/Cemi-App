from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('details/<int:item_id>/', views.details, name='details'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
   
]