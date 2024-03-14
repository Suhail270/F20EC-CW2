"""ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from sales.views import (CartListView,add_to_cart,load_cart_items,load_wishlist)
from users.views import (LandingPageView, 
                         SignupView, 
                         ServicesView, 
                         VisionView, 
                         OurTeamView, 
                         MembershipPlanView, 
                         PaymentView, 
                         PaymentSuccessView,
                         TrialSuccessView,
                         ItemListView,
                         SearchView)
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
import sales.views
# from sales.templates.sales.fonts import helvetiker.typeface.json

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('', OurTeamView.as_view(), name='landing-page'),
    path('', ItemListView.as_view(), name='landing-page'),
    path('search/', SearchView.as_view(), name='products-list'),
    path('add_to_cart/<int:id>/',sales.views.add_to_cart,name='add_to_cart'),
    path("our-services/", ServicesView.as_view(), name='services'),
    path("vision/", VisionView.as_view(), name='vision'),
    path("our-team/", OurTeamView.as_view(), name='team'),
    path('cart/', CartListView.as_view(), name='cart'),
    path('ajax/load_cart_list/', load_cart_items, name='ajax_load_cart_list'),
    path('ajax/load_wishlist/', load_wishlist, name='ajax_load_wishlist'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('membership-plans/', MembershipPlanView.as_view(), name='member-plan'),
    path('membership-plans/payment', PaymentView.as_view(), name='payment'),
    path('payment-success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('trial-success/', TrialSuccessView.as_view(), name='trial-success'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include('sales.urls')), # new
]
