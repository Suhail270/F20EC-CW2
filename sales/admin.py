from django.contrib import admin
from .models import (
                    Item,
                    Cart,
                    CartItem,
                    ModeOfPayment,
                    Order,
                    OrderItem,
                    Wishlist,
                    WishlistItem,
                    Category)

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ModeOfPayment)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)