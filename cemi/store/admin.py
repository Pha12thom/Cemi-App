from django.contrib import admin
from .models import Store, items, user

admin.site.register(Store)
admin.site.register(user)
admin.site.register(items)

# Register your models here.
