from audioop import maxpp

from django import forms
from .models import CustomUser, ServiceProviderProfile, CustomerProfile

import re
from django import forms
from .models import ServiceProviderProfile
from home.models import City, Area, ServiceCategory

class ServiceProviderProfileForm(forms.ModelForm):
    class Meta:
        model = ServiceProviderProfile
        fields = [
            'city',
            'area',
            'street',
            'sub_category',
            'service_category',
            'service_description',
            'phone_number',
            'photo',
        ]


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = '__all__'


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'is_service_provider']




class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'password']