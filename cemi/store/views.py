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


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Create the user
            user = User.objects.create(username=username, email=email, password=password)
            # Log in the user after successful registration
            return redirect('login')  # Redirect to the home page
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login(request): 
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User = authenticate(request, username=username, password=password)
            if User is not None:
                return redirect('base')
            else:
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid username or password.'})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})




def logout(request):
    form = LogoutForm()
    if request.method == 'POST':
        form = LogoutForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Logout successful')
            return redirect('login')
    context = {
        'form': form,
    }
    return render(request, 'logout.html', context)


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