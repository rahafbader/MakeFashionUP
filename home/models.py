# ecommerce/models.py 
from django.contrib.auth.models import User 
 
from django.db import models 
 
class Category(models.Model): 
    name = models.CharField(max_length=100) 
 
    def __str__(self): 
        return self.name 
 
class Product(models.Model): 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)  # Assuming 1 is a valid Category ID 
    name = models.CharField(max_length=200) 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    description = models.TextField() 
    image = models.ImageField(upload_to='images/') 
 
    def __str__(self): 
        return self.name 
 
class Order(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    products = models.ManyToManyField(Product, through='OrderItem') 
    total_price = models.DecimalField(max_digits=10, decimal_places=2) 
    ordered_date = models.DateTimeField(auto_now_add=True) 
    is_ordered = models.BooleanField(default=False) 
 
    def __str__(self): 
        return f"Order {self.id}" 
 
class OrderItem(models.Model): 
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1) 
 
    def __str__(self): 
        return f"{self.product.name} - {self.quantity}"