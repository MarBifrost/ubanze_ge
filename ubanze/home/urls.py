from django.urls import path
from . import views
from .views import HomeView, ContactView, AuthorizedHome

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact', ContactView.as_view(), name='contact'),
    path('services/', AuthorizedHome.as_view(), name='services'),
]
