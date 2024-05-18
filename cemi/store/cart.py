from decimal import Decimal


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, item, quantity=1):
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {'quantity': quantity, 'price': str(item.price)}
        else:
            self.cart[item_id]['quantity'] += quantity
        self.save()

    def reduce_quantity(self, item_id):
        item_id = str(item_id)
        if item_id in self.cart:
            if self.cart[item_id]['quantity'] > 1:
                self.cart[item_id]['quantity'] -= 1
            else:
                del self.cart[item_id]
            self.save()

    def save(self):
        self.session.modified = True
    
    def clear(self):
        self.cart = {}
        self.session.modified = True

    @property
    def get_total(self):
        total = 0
        for item_id, item_info in self.cart.items():
            total += item_info['quantity'] * Decimal(item_info['price'])
        return total
