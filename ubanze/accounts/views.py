from allauth.socialaccount.views import LoginErrorView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, FormView, TemplateView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import ServiceProviderProfileForm, RegisterForm, LoginForm
from .models import ServiceProviderProfile, CustomerProfile
from .serializers import RegisterSerializer


# Create your views here.

class ServiceProviderProfileCreateView(LoginRequiredMixin, CreateView):
    model = ServiceProviderProfile
    form_class = ServiceProviderProfileForm
    template_name = 'accounts/servie_provider_profile.html'
    success_url = reverse_lazy('accounts/profile/')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ServiceProviderProfileDetailView(LoginRequiredMixin, DetailView):
    model = ServiceProviderProfile
    template_name = 'accounts/servie_provider_profile.html'
    context_object_name = 'service_provider_profile'


class CustomerProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomerProfile
    template_name = './accounts/customer_profile.html'
    context_object_name = 'customer_profile'


class RegisterView(FormView):
    template_name = './accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class LoginView(FormView):
    template_name = './accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('accounts:home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = './accounts/home.html'
    login_url = reverse_lazy('accounts:home')
    redirect_field_name = 'next'





