from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, FormView, TemplateView, View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .forms import ServiceProviderProfileForm, RegisterForm, LoginForm
from .models import ServiceProviderProfile, CustomerProfile, CustomUser
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
    template_name = 'accounts/provider_profile.html'
    context_object_name = 'provider_profile'

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, pk=self.kwargs['pk'], is_service_provider=True)

class CustomerProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomerProfile
    template_name = './accounts/customer_profile.html'
    context_object_name = 'customer_profile'

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, pk=self.kwargs['pk'], is_service_provider=False)


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            if user.is_service_provider:
                redirect_url = reverse('accounts:service-provider', kwargs={'pk': user.pk})
            else:
                redirect_url = reverse('accounts:customer', kwargs={'pk': user.pk})


            return render(request, 'accounts/loading.html', {'redirect_url': redirect_url})

        else:
            messages.error(request, "რეგისტრაციის დროს დაფიქსირდა შეცდომა")

        return render(request, 'accounts/register.html', {'form': form})



class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'


    def get_success_url(self, form):
        user = self.request.user
        if user.is_authenticated:
            return reverse('accounts:customer', kwargs={'pk': user.pk})
        return reverse('accounts:login')

    def form_valid(self, form):
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            backend = 'django.contrib.auth.backends.ModelBackend'
            login(self.request, user, backend=backend)
            return redirect(self.get_success_url(form=form))
        else:
            messages.error(self.request, form.errors)
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))






