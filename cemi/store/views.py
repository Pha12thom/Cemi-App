from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Store, items, Profile, Review
from .cart import Cart
from django.contrib import messages
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm, LogoutForm, UserProfileForm, ReviewForm
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


def custom_login_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to your account or register to view this part of the site.')
            return redirect('user_login')  # Ensure this URL name matches your login view URL name
        return view_func(request, *args, **kwargs)
    return wrapped_view

def activateEmail(request, user, to_email):
    messages.success(request, f'You have successfully registered. \n Please check your email {to_email} to activate your account.')

# views.py



from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegisterForm
from .utils import activateEmail  # Ensure this import is correct

def user_register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username=username, password=password, email=email)
            user.is_active = False  # User is not active until they confirm their email
            user.save()
            
            activateEmail(request, user, email)
            messages.success(request, f'You have successfully registered. \n Your account activation link has been sent to  {email}. please check your email for account activation.')
            return redirect('shop')
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
            return redirect('shop')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html', {'form': form})

@custom_login_required
def user_logout(request):
    form = LogoutForm(request.POST)
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have logged out. Welcome back to cemi shop')
        return redirect('user_login')
    return render(request, 'logout.html', {'form': form})


@custom_login_required
def home(request):
    if 'q' in request.GET:
        q = request.GET['q']
        items_page = items.objects.filter(name__icontains=q)
    else:
        items_page = items.objects.all()
    user_page = Profile.objects.all()
    store_page = Store.objects.all()
    cart = Cart(request)
    total_quantity = sum(item['quantity'] for item in cart.cart.values())

    context = {
        'user_page': user_page,
        'store_page': store_page,
        'items_page': items_page,
        'total_quantity': total_quantity,
        'cart': cart,

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

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import items, Review
from .forms import ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def details(request, item_id):
    item = get_object_or_404(items, pk=item_id)
    user_page = Profile.objects.all()
    store_page = Store.objects.all()
    items_page = items.objects.all()
    cart = Cart(request)
    total_quantity = sum(item['quantity'] for item in cart.cart.values())

    # Fetch reviews for the specific item
    reviews = Review.objects.filter(item=item)

    # Handle review form submission
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully.')
            return redirect('details', item_id=item_id)
        else:
            messages.error(request, 'Failed to submit review. Please check the form data.')
    else:
        form = ReviewForm()

    context = {
        'user_page': user_page,
        'store_page': store_page,
        'items_page': items_page,
        'item': item,
        'reviews': reviews,  # Pass the reviews to the template
        'total_quantity': total_quantity,
        'cart': cart,
        'form': form,  # Pass the review form to the template
    }

    return render(request, 'details.html', context)



@custom_login_required
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


@custom_login_required
def reduce_item_quantity(request, item_id):
    cart = Cart(request)
    cart.reduce_quantity(item_id)
    return redirect('cart')

@custom_login_required
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

@custom_login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(items, id=item_id)
    cart = Cart(request)
    cart.add(item)
    total_price = Decimal(item.price) * cart.cart[str(item_id)]['quantity']
    return redirect('cart')

@custom_login_required
def user_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    latest_order = Order.objects.filter(user=request.user).order_by('-created_at').first()
    cart = Cart(request)
    total_quantity = sum(item['quantity'] for item in cart.cart.values())
    context = {
        'profile': profile,
        'latest_order': latest_order,
        'total_quantity': total_quantity,
        'cart': cart,


    }

    return render(request, 'profile.html', context)


def shop(request):
    if 'q' in request.GET:
        q = request.GET['q']
        items_page = items.objects.filter(name__icontains=q)
    else:
        items_page = items.objects.all()
    cart = Cart(request)
    user_page = Profile.objects.all()
    store_page = Store.objects.all()
    total_quantity = sum(item['quantity'] for item in cart.cart.values())
    context = {
        'user_page': user_page,
        'store_page': store_page,
        'items_page': items_page,
        'cart': cart,
        'total_quantity': total_quantity,


    }
    return render(request, 'shop.html', context)


@custom_login_required
def about(request):
    cart = Cart(request)
    context = {
        'cart': cart,
        }
    return render(request, 'about.html', context)

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


@custom_login_required
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

            return redirect('checkout')
    else:
        form = OrderForm()

    return render(request, 'order.html', {
        'form': form,
        'total_price': total_price,
    })

from .forms import ProfileForm


@custom_login_required
def user_profile(request):
    if request.method == 'POST':

        form = ProfileForm(request.POST)


        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile created successfully! You can now view your orders')
            return redirect('user_profile')
        else:
            messages.error(request, 'An error occurred while creating the profile.')
    else:
        form = ProfileForm()

    return render(request, 'user_profile.html', {'form': form})

@custom_login_required
def orders(request):
    profile = get_object_or_404(Profile, user=request.user)
    latest_order = Order.objects.filter(user=request.user).order_by('-created_at').first()
    cart = Cart(request)
    total_quantity = sum(item['quantity'] for item in cart.cart.values())


    context = {
        'profile': profile,
        'latest_order': latest_order,
        'cart': cart,
        'total_quantity': total_quantity,

    }

    return render(request, 'orders.html', context)


def handling_404(request, exception):
    return render(request, '404.html', status=404)




# views.py

from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib import messages

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been confirmed.')
        return redirect('user_login')
    else:
        messages.error(request, 'The confirmation link was invalid, possibly because it has already been used.')
        return redirect('user_register')


# views.py
def shop_category(request, category):
    items_by_category = items.objects.filter(category=category)
    cart = Cart(request)
    total_quantity = sum(item['quantity'] for item in cart.cart.values())

    context = {
        'items': items_by_category,
        'category': category,
        'cart': cart,
        'total_quantity': total_quantity,
    }
    return render(request, 'shop_category.html', context)

def landing_page(request):
    return render(request, 'landing_page.html')