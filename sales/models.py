from django.db import models
from users.models import User
from django.utils import timezone

class Item(models.Model):
    name = models.CharField(max_length=500)
    category_tree = models.CharField(max_length=500)
    retail_price = models.IntegerField()
    image = models.URLField()
    description = models.CharField(max_length=500)
    brand = models.CharField(max_length=100)
    
    def __str__(self) :
        return f"{self.name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(null=True)
    edited_date = models.DateTimeField(default=timezone.now)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    edited_date = models.DateTimeField(default=timezone.now)

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)