from typing import Any, Mapping
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import User
from sales.models import Order

User = get_user_model()


class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'address'
        )

    def clean_first_name(self):
        data = self.cleaned_data["first_name"]
        return data

    def clean(self):
        pass

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)

class CategoryForm(forms.Form):
    CategoryQuery = forms.CharField(max_length=500)

class LogsisticsForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'address',
            'mode_of_payment'
        )
        widgets = {
            "mode_of_payment": forms.RadioSelect(),
        }
    def __init__(self, *args, **kwargs):
        address = kwargs.pop('address', None)
        super().__init__(*args, **kwargs)
        if address is not None:
            self.fields['address'].initial = address
