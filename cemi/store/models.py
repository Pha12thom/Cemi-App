from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=20, null=True)
    address = models.TextField(null=True)

    # Add other fields as needed

    def __str__(self):
        return self.user.username 
    
    
# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
# models.py

class items(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('on_sale', 'On Sale'),
        ('sold', 'Sold'),
    ]

    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=100, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    percentage_discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    images = models.ImageField(null=True, upload_to='static/', default='fridge.jpg')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.name

    def sold(self):
        return self.status.capitalize()


class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(items, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{self.user} - {self.item} - {self.quantity}"
    
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    delivery_address = models.TextField()
    items = models.TextField()  # You can use JSONField if you want to store the items as structured data
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.user}'
