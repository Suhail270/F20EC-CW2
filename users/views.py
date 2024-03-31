from django.db.models.query import QuerySet
from django.views import generic
from django.http.response import JsonResponse
import string
import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from .forms import CategoryForm, CustomUserCreationForm,SearchForm, UserModelForm,LogsisticsForm
from sales.models import Category, Item, Cart, CartItem, OrderItem, Order
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
    
def shorten_cat_name(name):
        words = name.split()
        if len(words) >= 2:
            return ' '.join(words[:2])
        else:
            return name
        
class ItemListView(generic.ListView):
    template_name = "products-display.html"
    context_object_name = "prods_list"
    paginate_by = 24
    
    def get_queryset(self):
        category = self.request.GET.get('CategoryQuery')
        sort_by = self.request.GET.get('sort_by')
        query = self.request.GET.get('query')
        filter_args = {}
        print("query is :", category)
        if query is not None:
            filter_args["name__icontains"] = query
        if category is not None and category != "none":
            categoryInstance = Category.objects.filter(name__startswith=category)
            filter_args["category__in"] = categoryInstance
        if sort_by == None or sort_by == "none":
            return Item.objects.filter(**filter_args)
        if sort_by == "ascending":
            return Item.objects.filter(**filter_args).order_by('retail_price')
        if sort_by == "descending":
            return Item.objects.filter(**filter_args).order_by('-retail_price')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = (Category.objects.all()[:10])
        categories_list = []
        for i in range(0,len(categories)): 
            categories_list.append(shorten_cat_name(categories[i].name))
        context['categories'] = categories_list
        return context
    
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
      
class LogisticsView(generic.CreateView):
    template_name = "logistics.html"
    form_class = LogsisticsForm

    def get_success_url(self):
        return reverse("payment_success")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['address'] = self.request.user.address
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address'] = self.request.user.address
        return context

    def form_valid(self, form):
        order = form.save(commit=False)

        user = self.request.user
        cart = Cart.objects.get(user=user)

        user.address = form.cleaned_data['address']
        user.save()

        order.user = self.request.user
        order.total_amount = cart.total_amount
        order.save()

        # YOUR CODE FOR LATER USE
        # cart_items = CartItem.objects.filter(cart=cart)
        # for cart_item in cart_items:
        #     order_item = OrderItem()
        #     order_item.order = order
        #     order_item.quantity = cart_item.quantity
        #     order_item.item = cart_item.item
        #     order_item.save()
            
        return super().form_valid(form)