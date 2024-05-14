from django.contrib import admin
from .models import Store, items

admin.site.register(Store)
admin.site.register(items)
# This is the admin.py file where we register our models.
# Register your models here.
