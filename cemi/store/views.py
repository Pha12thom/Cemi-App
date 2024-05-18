from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Store, items, Profile
from .cart import Cart
from django.contrib import messages
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm, LogoutForm, UserProfileForm
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import OrderForm
from .models import Order
from .cart import Cart  # Import your Cart class
from django.contrib.auth.decorators import login_required


def activateEmail(request, user, to_email):
    messages.success(request, f'You have successfully registered. \n Please check your email {to_email} to activate your account.')

def user_register(request):
    form = RegisterForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = form.data['username']
            password = form.data['password']
            email = form.data['email']
            user = User.objects.create_user(username=username, password=password, email=email)
            user.is_active = True
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
      
            login(request, user)
            messages.success(request, 'You have successfully registered.')
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
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    form = LogoutForm(request.POST)
    if request.method == 'POST':
        logout(request)
        return redirect('user_login')
    return render(request, 'logout.html', {'form': form})

        
        
def home(request):
    user_page = Profile.objects.all()
    store_page = Store.objects.all()
    items_page = items.objects.all()
    context = {
        'user_page': user_page,
        'store_page': store_page,
        'items_page': items_page,
    }
    return render(request, 'home.html', context)



def base(request):
    if 'q' in request.GET:
        q = request.GET['q']
        items_page = items.objects.filter(name__icontains=q)
    else:
        items_page = items.objects.all()    
    cart = Cart(request)
    total_quantity = sum(item['quantity'] for item in cart.cart.values())
    user_page = Profile.objects.all()
    store_page = Store.objects.all()
    
    context = {
        'user_page': user_page,
        'store_page': store_page,
        'items_page': items_page,
        'total_quantity': total_quantity,
        'cart': cart,
    }
    return render(request, 'base.html', context)

@login_required
def details(request, item_id):
    item = get_object_or_404(items, pk=item_id)
    user_page = Profile.objects.all()
    store_page = Store.objects.all()
    items_page = items.objects.all()
    context = {
        'user_page': user_page,
        'store_page': store_page,
        'items_page': items_page,
        'item': item,
    }
    
    return render(request, 'details.html', context)

@login_required
def cart(request):
    cart = Cart(request)
    total_quantity = sum(item['quantity'] for item in cart.cart.values())
    
    # Fetch the item objects including images
    items_with_prices = []
    total_price = 0  # Initialize total price
    
    for item_id, item_info in cart.cart.items():
        item = get_object_or_404(items, id=item_id)
        item.quantity = item_info['quantity']  # Add quantity to the item object
        total_item_price = item.price * item_info['quantity']
        total_price += total_item_price  # Add item's total price to the total price
        items_with_prices.append((item, total_item_price))  # Append tuple of item and total price
    
    context = {
        'cart': cart,
        'total_quantity': total_quantity,
        'items_with_prices': items_with_prices,  # Pass the items with total prices to the template
        'total_price': total_price,  # Pass total price to the template
    }
    return render(request, 'cart.html', context)


@login_required
def reduce_item_quantity(request, item_id):
    cart = Cart(request)
    cart.reduce_quantity(item_id)
    return redirect('cart')

@login_required
def checkout(request):
    cart = Cart(request)
    total_quantity = sum(item['quantity'] for item in cart.cart.values())
    
    # Fetch the item objects including images
    items_with_prices = []
    total_price = 0  # Initialize total price
    
    for item_id, item_info in cart.cart.items():
        item = get_object_or_404(items, id=item_id)
        item.quantity = item_info['quantity']  # Add quantity to the item object
        total_item_price = item.price * item_info['quantity']
        total_price += total_item_price  # Add item's total price to the total price
        items_with_prices.append((item, total_item_price))  # Append tuple of item and total price
    context = {
        'cart': cart,
        'total_quantity': total_quantity,
        'items_with_prices': items_with_prices,  # Pass the items with total prices to the template
        'total_price': total_price,  # Pass total price to the template
    } 
    return render(request, 'checkout.html', context)

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(items, id=item_id)
    cart = Cart(request)
    cart.add(item)
    total_price = Decimal(item.price) * cart.cart[str(item_id)]['quantity']
    return redirect('cart') 

@login_required
def user_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    latest_order = Order.objects.filter(user=request.user).order_by('-created_at').first()
    
    context = {
        'profile': profile,
        'latest_order': latest_order,
    }
    
    return render(request, 'profile.html', context)

@login_required
def shop(request):
    if 'q' in request.GET:
        q = request.GET['q']
        items_page = items.objects.filter(name__icontains=q)
    else:
        items_page = items.objects.all()
    user_page = Profile.objects.all()
    store_page = Store.objects.all()
    context = {
        'user_page': user_page,
        'store_page': store_page,
        'items_page': items_page,   
    }
    return render(request, 'shop.html', context)



def about(request):
    return render(request, 'about.html')

def success(request):
    return render(request, 'success.html')

def welcome(request):
    user_page = Profile.objects.all()
    store_page = Store.objects.all()
    items_page = items.objects.all()
    context = {
        'user_page': user_page,
        'store_page': store_page,
        'items_page': items_page,
    }
    return render(request, 'welcome.html', context)


@login_required
def order(request):
    cart = Cart(request)
    items_with_prices = []
    total_price = 0
    
    for item_id, item_info in cart.cart.items():
        item = get_object_or_404(items, id=item_id)
        total_item_price = item.price * item_info['quantity']
        total_price += total_item_price
        items_with_prices.append((item, total_item_price))

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order(
                user=request.user,
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                delivery_address=form.cleaned_data['delivery_address'],
                items=str(items_with_prices),
                total_price=total_price
            )
            order.save()

            # Send confirmation email
            send_mail(
                'Order Confirmation',
                f'Thank you for your order! Here are the details:\n\nItems: {items_with_prices}\nTotal Price: {total_price}\nDelivery Address: {order.delivery_address}',
                settings.DEFAULT_FROM_EMAIL,
                [order.email],
                fail_silently=False,
            )

            # Clear the cart
            cart.clear()

            return redirect('success')
    else:
        form = OrderForm()

    return render(request, 'order.html', {
        'form': form,
        'total_price': total_price,
    })

from .forms import ProfileForm


@login_required
def user_profile(request):
    if request.method == 'POST':
        
        form = ProfileForm(request.POST)
        
    
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile created successfully!')
            return redirect('user_profile')
        else:
            messages.error(request, 'An error occurred while creating the profile.')
    else:
        form = ProfileForm()
    
    return render(request, 'user_profile.html', {'form': form})

def orders(request):
    profile = get_object_or_404(Profile, user=request.user)
    latest_order = Order.objects.filter(user=request.user).order_by('-created_at').first()
    
    context = {
        'profile': profile,
        'latest_order': latest_order,
    }
    
    return render(request, 'orders.html', context)
    