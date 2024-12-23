from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from accounts.models import ServiceProviderProfile


# Create your views here.
class HomeView(TemplateView):
    template_name = './accounts/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ContactView(TemplateView):
    template_name = './home/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AuthorizedHome(LoginRequiredMixin, ListView):
    model = ServiceProviderProfile
    template_name = './home/authorized_home.html'
    context_object_name = 'profiles_list'
