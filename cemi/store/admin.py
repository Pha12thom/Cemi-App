from django.contrib import admin
from .models import Store, items, Profile, cart, Order, Review

admin.site.register(Store)
admin.site.register(Profile)
admin.site.register(items)
admin.site.register(Order)
admin.site.register(cart)
admin.site.register(Review)

# Register your models here.
