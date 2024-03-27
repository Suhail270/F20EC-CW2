from django.db import models
from users.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self) :
        return f"{self.name}"

class Item(models.Model):
    name = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    retail_price = models.IntegerField()
    image = models.URLField()
    description = models.CharField(max_length=500)
    brand = models.CharField(max_length=100)
    
    def __str__(self) :
        return f"{self.name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) :
        return f"{self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) :
        return self.cart.user.username + " | " + self.item.name

class ModeOfPayment(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) :
        return f"{self.name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length=500)
    mode_of_payment = models.ForeignKey(ModeOfPayment, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) :
        return f"{self.user.username} - {self.ordered_date}: {self.total_amount}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) :
        return self.order.user.username + " - " + self.item.name + ": " + self.order.ordered_date.strftime("%Y-%m-%d %H:%M:%S")

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)