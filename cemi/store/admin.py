from django.contrib import admin
from .models import Store, items, user

admin.site.register(Store)
admin.site.register(user)
admin.site.register(items)
# This is the admin.py file where we register our models.
# Register your models here.
