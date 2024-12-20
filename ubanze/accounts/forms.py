from audioop import maxpp

from django import forms
from .models import CustomUser, ServiceProviderProfile, CustomerProfile

class ServiceProviderProfileForm(forms.ModelForm):
    class Meta:
        model = ServiceProviderProfile
        fields = '__all__'

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = '__all__'


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'is_service_provider']

    # def save(self, commit=True):
    #     user = super(RegisterForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data['password'])
    #     if commit:
    #         user.save()
    #         if user.is_service_provider:
    #             ServiceProviderProfile.objects.create(user=user)
    #     return user



class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'password']