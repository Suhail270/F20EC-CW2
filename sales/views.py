import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.forms import model_to_dict
from django.views import generic
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem, Item, Wishlist, WishlistItem, Cart, CartItem, Category
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, View
from django.utils import timezone

class CartListView(LoginRequiredMixin, generic.TemplateView):
    template_name = "cart.html"

class WishlistView(LoginRequiredMixin, generic.TemplateView):
    template_name = "wishlist.html"

def load_wishlist(request):
    user = request.user
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
    data = []
    for wishlist_item in wishlist_items:
        data.append({
            "id": wishlist_item.id,
            "quantity": wishlist_item.quantity,
            "item": model_to_dict(wishlist_item.item),
            "category": wishlist_item.item.category
        })
    return JsonResponse({"h": render_to_string(request=request, template_name="wishlist_content.html", context={"wishlist_items": data})})
    
def load_cart_items(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    cart_items = CartItem.objects.filter(cart=cart)
    data = []
    for cart_item in cart_items:
        data.append({
            "id": cart_item.id,
            "quantity": cart_item.quantity,
            "item": model_to_dict(cart_item.item),
            "category": cart_item.item.category
        })
    return JsonResponse({"h": render_to_string(request=request, template_name="cart_list.html", context={"cart_items": data})})

# class CategoryView(generic.TemplateView):
#     template_name = "category.html"  # Use navbar.html as the template

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         categories = Item.objects.values_list('category_tree', flat=True).distinct()[:10]
#         context['categories'] = categories
#         return context

class PaymentView(generic.TemplateView):
    template_name = 'stripe.html'

# @login_required
class CreateStripeCheckoutSessionView(View):

    stripe.api_key = settings.STRIPE_SECRET_KEY

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user).first()
        price = cart.total_amount

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "gbp",
                        "unit_amount": int(price),
                        "product_data": {
                            "name": "Secure transaction to WattMart™, Powered by Stripe",
                            "description": "Order placed",
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url='http://127.0.0.1:8000/success/',
            # cancel_url=,
        )
        return redirect(checkout_session.url)


class PaymentSuccessView(generic.TemplateView):
    template_name = "payment_success.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class CategoryView(generic.ListView):
    template_name = "category.html"
    context_object_name = "category"
 
    def get_queryset(self):
        print (Category.objects.all()[:10])
        return Category.objects.all()[:10]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = (Category.objects.all()[:10])
        context['categories'] = categories
        return context
    
class ItemDetailView(generic.DetailView):
    model = Item
    template_name = 'item_detail.html'
    context_object_name = 'item_detail'

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price': 'price_1Os1cYJDw3WYrLo5D2gQCvfP',
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    
    except ValueError as e:
        return HttpResponse(status=400)
    
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")

    return HttpResponse(status=200)

@csrf_exempt
@login_required
def add_to_cart(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'auth': False})

    item = get_object_or_404(Item, id=id)
    cart = Cart.objects.filter(user=request.user).first()
    
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        item=item,
        quantity=1
    )

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        
    else:
        cart.total_amount += item.retail_price
        cart.save()

    return JsonResponse({'auth': True, 'message': 'Item added to cart successfully'})


@csrf_exempt
def remove_from_cart(request, id):
    CartItem.objects.filter(id=id).delete()
    return JsonResponse({'message': 'Item deleted from cart'})

@csrf_exempt
def remove_from_wishlist(request, id):
    WishlistItem.objects.filter(id=id).delete()
    return JsonResponse({'message': 'Item deleted from wishlist'})

@csrf_exempt
def add_to_wishlist(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'auth': False})
    
    user = request.user
    item = get_object_or_404(Item, id=id)
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    
    wishlist_item, created = WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        item=item
    )

    if not created:
        wishlist_item.quantity += 1
        wishlist_item.save()

    return JsonResponse({'auth': True, 'message': 'Item added to wishlist successfully'})

@csrf_exempt
def change_quantity(request, id):
    diff = int(request.POST.get("diff"))
    list_type = request.POST.get("list_type")
    alt = request.POST.get("alt")
    if list_type == "cart":
        model = CartItem
    elif list_type == "wishlist":
        model = WishlistItem
    list_item = model.objects.get(id=id)
    if alt:
        list_item.quantity = diff
    else:
        list_item.quantity += diff
    list_item.save()
    return JsonResponse({"quantity": list_item.quantity})

@csrf_exempt
def move_to_cart(request, id):
    item = WishlistItem.objects.get(id=id).item
    remove_from_wishlist(request, id)
    add_to_cart(request, item.id)
    return JsonResponse({})

@csrf_exempt
def move_to_wishlist(request, id):
    item = CartItem.objects.get(id=id).item
    remove_from_cart(request, id)
    add_to_wishlist(request, item.id)
    return JsonResponse({})

class OrdersView(LoginRequiredMixin, generic.ListView):
    template_name = "orders.html"
    # template_name = "category.html"  # Use navbar.html as the template
    def get_queryset(self):
        return Order.objects.filter(user= self.request.user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(user= self.request.user)
        orders_items = OrderItem.objects.filter(order__in=orders)       
        
        context['orders'] = orders
        context['orders_items'] = orders_items
        return context
