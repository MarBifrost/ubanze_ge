from django.views.generic import ListView

from allauth.account.utils import user_email
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.lookups import IsNull
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

from .forms import ServiceProviderProfileForm, RegisterForm, LoginForm, CustomerProfileForm
from .models import ServiceProviderProfile, CustomerProfile, CustomUser
from home.models import City, Area, ServiceCategory

from ubanze import settings


# Create your views here.

class RegisterView(CreateView):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)

            if user.is_service_provider:
                redirect_url = reverse('accounts:profile_edit')
            else:
                redirect_url = reverse ('accounts:customer', kwargs={'pk':user.pk})

            return render(request, 'accounts/loading.html', {'redirect_url': redirect_url})

        messages.error(request, "An error occurred during registration.")
        return render(request, 'accounts/register.html', {'form': form})



# class ServiceProviderProfileCreateView(LoginRequiredMixin, CreateView):
#     model = ServiceProviderProfile
#     form_class = ServiceProviderProfileForm
#     template_name = 'accounts/provider_profile.html'
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         print("Cleaned Data:", form.cleaned_data)
#         messages.success(self.request, "Profile created successfully")
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         print("Form Errors:", form.errors)
#         messages.error(self.request, "Error creating profile")
#         return super().form_invalid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'cities': City.objects.all(),
#             'areas': Area.objects.all(),
#             'service_categories': cache_tree_children(ServiceCategory.objects.filter(parent__isnull=True)),
#             'subcategories': ServiceCategory.objects.filter(parent__isnull=False),
#             'provider_profile': None
#         })
#         return context


    # def dispatch(self, request, *args, **kwargs):
    #     if ServiceProviderProfile.objects.filter(user=request.user).exists():
    #         protile=ServiceProviderProfile.objects.get(user=request.user)
    #         return redirect('accounts:completed_profile', pk=protile.pk)
    #     return super().dispatch(request, *args, **kwargs)



class ServiceProviderProfileEditView(LoginRequiredMixin, UpdateView):
    model = ServiceProviderProfile
    form_class = ServiceProviderProfileForm
    template_name = 'accounts/provider_profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(ServiceProviderProfile, user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Profile updated successfully")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'profile': self.object,
            'cities':City.objects.all(),
            'areas':Area.objects.all(),
            'service_categories': cache_tree_children(ServiceCategory.objects.filter(parent__isnull=True)),
            'subcategories': ServiceCategory.objects.filter(parent__isnull=False),
        })
        return context

    def get_success_url(self):
        return reverse('accounts:completed_profile', kwargs={'pk': self.object.pk})

class ServiceProviderProfileCompletedView(LoginRequiredMixin, DetailView):
    model = ServiceProviderProfile
    template_name = 'accounts/providers_completed_profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        user = self.request.user
        return get_object_or_404(ServiceProviderProfile, user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('accounts:completed_profile', kwargs={'pk': self.object.pk})



class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'


    def get_success_url(self, form):
        user = self.request.user
        if user.is_authenticated:
            return reverse('home:authorized_home', kwargs={'pk': user.pk})
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
    


#subcategories API endpoint
def get_subcategories(request, category_id):
    subcategories = ServiceCategory.objects.filter(parent_id=category_id).values('id', 'name')
    return JsonResponse({'subcategories': list(subcategories)})




