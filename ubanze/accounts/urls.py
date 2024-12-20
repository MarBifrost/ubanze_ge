from django.urls import path
from .views import RegisterView, LoginView, ServiceProviderProfileDetailView, CustomerProfileDetailView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('service-provider/<uuid:pk>', ServiceProviderProfileDetailView.as_view(), name='service-provider'),
    path('customer/<uuid:pk>', CustomerProfileDetailView.as_view(), name='customer'),
]