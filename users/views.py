from django.db.models.query import QuerySet
from django.views import generic
from django.http.response import JsonResponse
import string
import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from .forms import CustomUserCreationForm,SearchForm, UserModelForm,LogsisticsForm
from sales.models import Item
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

class ItemListView(generic.TemplateView):
    template_name = "products-display.html"
    context_object_name = "prods_list"

    # def get_queryset(self) :
    #     queryset = Item.objects.all().values()
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        user = self.request.user
        
        queryset = Item.objects.all().values()[:24]
        context.update({
                "prods_list": queryset
            })
        
        return context  

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
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
    template_name = 'products-display.html'
    context_object_name = 'prods_list'
    form_class = SearchForm

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return Item.objects.filter(name__icontains=query)[:24]
        return {}

class LogisticsView(generic.CreateView):
    template_name = "logistics.html"
    form_class = LogsisticsForm

    def get_success_url(self):
        return reverse("payment_success.html")
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['address'] = user.address
        return context
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        return super(LogisticsView,self).form_valid(form)