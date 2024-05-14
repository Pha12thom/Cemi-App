from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('base/', views.base, name='base'),
   
]