from django.db.models.query import QuerySet
from django.views import generic
from django.http.response import JsonResponse
import string
import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from .forms import CustomUserCreationForm,SearchForm, UserModelForm,LogsisticsForm
from sales.models import Item, Cart, CartItem, OrderItem, Order
# Create your views here.

class LandingPageView(generic.ListView):
    template_name = "landing.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("services")
        return super().dispatch(request, *args, **kwargs)

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        Cart.objects.create(user=self.object)
        return response

class ServicesView(generic.TemplateView):
    template_name = "services.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class VisionView(generic.TemplateView):
    template_name = "vision.html"
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class OurTeamView(generic.TemplateView):
    template_name = "team.html"
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class ItemListView(generic.ListView):
    template_name = "products-display.html"
    context_object_name = "prods_list"
    paginate_by = 24
    
    def get_queryset(self):
            sort_by = self.request.GET.get('sort_by')
            if sort_by == None:
                sort_by = "descending"
            if sort_by == "ascending":
                return Item.objects.all().order_by('retail_price')
            if sort_by == "descending":
                return Item.objects.all().order_by('-retail_price')
    
class MembershipPlanView(generic.TemplateView):
    template_name = "plan.html"
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class PaymentView(generic.TemplateView):
    template_name = "payment.html"
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
class PaymentSuccessView(generic.TemplateView):
    template_name = "payment_success.html"
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class TrialSuccessView(generic.TemplateView):
    template_name = "freeTrial.html"
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
class SearchView(generic.ListView):
    paginate_by = 24
    template_name = 'products-display.html'
    context_object_name = 'prods_list'
    form_class = SearchForm

    def get_queryset(self):
        query = self.request.GET.get('query')
        sort_by = self.request.GET.get('sort_by')
        if sort_by == None:
            sort_by = "descending"
        if sort_by == "ascending":
            return Item.objects.filter(name__icontains=query).order_by('retail_price')
        if sort_by == "descending":
            return Item.objects.filter(name__icontains=query).order_by('-retail_price')

class LogisticsView(generic.CreateView):
    template_name = "logistics.html"
    form_class = LogsisticsForm

    def get_success_url(self):
        return reverse("payment_success.html")
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        return form
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['address'] = self.request.user.address
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['address'] = user.address
        return context
    
    def form_valid(self, form):
        order = form.save(commit=False)

        user = self.request.user
        cart = Cart.objects.get(user=user)

        order.user  = self.request.user
        order.total_amount = cart.total_amount
        order.save()

        # THIS CODE IS FOR LATER
        # cart_items = CartItem.objects.filter(cart=cart)
        # for cart_item in cart_items:
        #     order_item = OrderItem()
        #     order_item.order = order
        #     order_item.quantity = cart_item.quantity
        #     order_item.item = cart_item.item
        #     order_item.save()
            
        return super(LogisticsView,self).form_valid(form)