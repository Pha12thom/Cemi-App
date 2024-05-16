from django.contrib import admin
from .models import Store, items, Profile, cart

admin.site.register(Store)
admin.site.register(Profile)
admin.site.register(items)
admin.site.register(cart)
# Register your models here.
