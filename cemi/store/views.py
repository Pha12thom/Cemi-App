from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Store, items, UserProfile
from .cart import Cart
from django.contrib import messages
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm, LogoutForm, UserProfileForm
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def user_register(request):
    form = RegisterForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = form.data['username']
            password = form.data['password']
            email = form.data['email']
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            login(request, user)
            return redirect('home')
    return render(request, 'register.html', {'form': form})
                  

def user_login(request):
    form = LoginForm(request.POST)
    if request.method == 'POST':
        username = form.data['username']
        password = form.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    form = LogoutForm(request.POST)
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return render(request, 'logout.html', {'form': form})

        
        
def home(request):
    user_page = UserProfile.objects.all()
    store_page = Store.objects.all()
    items_page = items.objects.all()
    context = {
        'user_page': user_page,
        'store_page': store_page,
        'items_page': items_page,
    }
    return render(request, 'home.html', context)



def base(request):
    cart = Cart(request)
    total_quantity = sum(item['quantity'] for item in cart.cart.values())
    user_page = UserProfile.objects.all()
    store_page = Store.objects.all()
    items_page = items.objects.all()
    
    context = {
        'user_page': user_page,
        'store_page': store_page,
        'items_page': items_page,
        'total_quantity': total_quantity,
        'cart': cart,
    }
    return render(request, 'base.html', context)


def details(request, item_id):
    item = get_object_or_404(items, pk=item_id)
    user_page = UserProfile.objects.all()
    store_page = Store.objects.all()
    items_page = items.objects.all()
    context = {
        'user_page': user_page,
        'store_page': store_page,
        'items_page': items_page,
        'item': item,
    }
    
    return render(request, 'details.html', context)


def cart(request):
    cart = Cart(request)
    total_quantity = sum(item['quantity'] for item in cart.cart.values())
    context = {
        'cart': cart,
        'total_quantity': total_quantity,
    }
    return render(request, 'cart.html', context)

def reduce_item_quantity(request, item_id):
    cart = Cart(request)
    cart.reduce_quantity(item_id)
    return redirect('cart')


def checkout(request):
    
    return render(request, 'checkout.html')


def add_to_cart(request, item_id):
    item = get_object_or_404(items, id=item_id)
    cart = Cart(request)
    cart.add(item)
    total_price = Decimal(item.price) * cart.cart[str(item_id)]['quantity']
    return redirect('cart') 

def profile(request):
    user_profile = UserProfile.objects.get(user=request.User)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'profile.html', {'form': form})

def shop(request):
   
    user_page = UserProfile.objects.all()
    store_page = Store.objects.all()
    items_page = items.objects.all()
    context = {
        'user_page': user_page,
        'store_page': store_page,
        'items_page': items_page,
        
    }
    return render(request, 'shop.html', context)

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')