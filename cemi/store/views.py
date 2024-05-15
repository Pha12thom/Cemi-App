from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Store, items, user
from .cart import Cart
from django.contrib import messages
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm, LogoutForm
from decimal import Decimal


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password == confirm_password:
                user.objects.create(username=username, email=email, password=password)
                messages.success(request, 'Account created successfully')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match')
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if user.objects.filter(username=username, password=password).exists():
                messages.success(request, 'Login successful')
                return redirect('home')
            else:
                messages.error(request, 'Username or password is incorrect')
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)

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
"""
def cart(request):
    user_page = user.objects.all()
    store_page = Store.objects.all()
    items_page = items.objects.all()
    context = {
        'user_page': user_page,
        'store_page': store_page,
        'items_page': items_page,
        
    }
    return render(request, 'cart.html', context)
"""


"""def add_to_cart(request, item_id):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        item_id = int(request.POST.get('item_id'))
        item = get_object_or_404(items, id=item_id)
        cart.add(item=item)
        response = JsonResponse({'qty': item.name, 'price': item.price})
        return response
        """
from django.shortcuts import render, redirect
from .cart import Cart
from decimal import Decimal

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
    # Implement your checkout logic here
    return render(request, 'checkout.html')


def add_to_cart(request, item_id):
    item = get_object_or_404(items, id=item_id)
    cart = Cart(request)
    cart.add(item)
    # Calculate total price for the added item
    total_price = Decimal(item.price) * cart.cart[str(item_id)]['quantity']
    return redirect('cart')  # Redirect to the cart page after adding the item
