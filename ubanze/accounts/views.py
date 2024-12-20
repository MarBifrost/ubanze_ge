from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, FormView, TemplateView, View, UpdateView
from mptt.templatetags.mptt_tags import cache_tree_children
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .forms import ServiceProviderProfileForm, RegisterForm, LoginForm
from .models import ServiceProviderProfile, CustomerProfile, CustomUser
from home.models import City, Area, ServiceCategory


# Create your views here.

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
                redirect_url = reverse('accounts:profile_create')
            else:
                redirect_url = reverse('accounts:customer', kwargs={'pk': user.pk})


            return render(request, 'accounts/loading.html', {'redirect_url': redirect_url})

        else:
            messages.error(request, "რეგისტრაციის დროს დაფიქსირდა შეცდომა")

        return render(request, 'accounts/register.html', {'form': form})


class ServiceProviderProfileCreateView(LoginRequiredMixin, CreateView):
    model = ServiceProviderProfile
    form_class = ServiceProviderProfileForm
    template_name = 'accounts/provider_profile.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ServiceCategory.objects.filter(parent__isnull=True)
        subcategories = ServiceCategory.objects.filter(parent__isnull=False)

        context['cities'] = City.objects.all()
        context['areas'] = Area.objects.all()
        context['service_categories'] = cache_tree_children(categories)
        context['subcategories'] = subcategories
        return context

    def get_success_url(self):
        return reverse('accounts:completed-profile', kwargs={'pk': self.object.pk})


class ServiceProviderProfileCompletedView(LoginRequiredMixin, DetailView):
    model = ServiceProviderProfile
    template_name = 'accounts/providers_completed_profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(ServiceProviderProfile, user=self.request.user)


class ServiceProviderProfileEditView(LoginRequiredMixin, UpdateView):
    model = ServiceProviderProfile
    fields = [
        'city', 'area', 'street',
        'service_category', 'sub_category',
        'service_description', 'phone_number', 'photo'
    ]

    template_name = 'accounts/provider_profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(ServiceProviderProfile, user=self.request.user)

    def get_success_url(self):
        return reverse('accounts:completed_profile', kwargs={'pk': self.request.user.pk})



class CustomerProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomerProfile
    template_name = './accounts/customer_profile.html'
    context_object_name = 'customer_profile'

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, pk=self.kwargs['pk'], is_service_provider=False)





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



def get_subcategories(request, category_id):
    subcategories = ServiceCategory.objects.filter(parent_id=category_id).values('id', 'name')
    return JsonResponse({'subcategories': list(subcategories)})


# class ServiceProviderProfileSaveView(LoginRequiredMixin, UpdateView):
#     model = ServiceProviderProfile
#     fields=[
#         'city', 'area', 'street',
#         'service_category', 'sub_category',
#         'service_description', 'phone_number', 'photo'
#     ]
#
#     template_name = 'accounts/provider_profile.html'
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(ServiceProviderProfile, user=self.request.user)
#
#     def get_success_url(self):
#         # Stay on the same page after saving
#         return reverse('accounts:edit-profile', kwargs={'pk': self.object.pk})


