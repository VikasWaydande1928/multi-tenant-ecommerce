from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=150)
    contact_email = models.EmailField()
    domain = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class User(AbstractUser):
    ROLE_CHOICES = (('owner','Owner'),('staff','Staff'),('customer','Customer'))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)

class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Customer(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='customers')
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='customer_profile')

class Order(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
