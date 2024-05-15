from .cart import Cart
def cart(request):
    cart_obj = Cart(request)
    return {'cart': cart_obj}