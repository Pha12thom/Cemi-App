from django.contrib import admin
from .models import Store, items, user, cart

admin.site.register(Store)
admin.site.register(user)
admin.site.register(items)
admin.site.register(cart)
# Register your models here.
