from django.contrib import admin
from .models import Store, items, UserProfile, cart

admin.site.register(Store)
admin.site.register(UserProfile)
admin.site.register(items)
admin.site.register(cart)
# Register your models here.
