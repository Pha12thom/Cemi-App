from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Store, items, user

def home(request):
    user_page = user.objects.all()
    store_page = Store.objects.all()
    items_page = items.objects.all()
    context = {
        'user_page': user_page,
        'store_page': store_page,
        'items_page': items_page,
    }
    return render(request, 'home.html', context)



def base(request):
    user_page = user.objects.all()
    store_page = Store.objects.all()
    items_page = items.objects.all()
    context = {
        'user_page': user_page,
        'store_page': store_page,
        'items_page': items_page,
    }
    return render(request, 'base.html', context)

def details(request, item_id):
    item = get_object_or_404(items, pk=item_id)
    user_page = user.objects.all()
    store_page = Store.objects.all()
    items_page = items.objects.all()
    context = {
        'user_page': user_page,
        'store_page': store_page,
        'items_page': items_page,
        'item': item,
    }
    
    return render(request, 'details.html', context)



def add_to_cart(request, item_id):
    item = get_object_or_404(items, pk=item_id)
    user_page = user.objects.all()
    store_page = Store.objects.all()
    items_page = items.objects.all()
    context = {
        'user_page': user_page,
        'store_page': store_page,
        'items_page': items_page,
        'item': item,
    }
    return render(request, 'cart.html', context)
