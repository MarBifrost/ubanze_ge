from django.urls import path
from .views import RegisterView, LoginView, ServiceProviderProfileCreateView, ServiceProviderProfileCompletedView,CustomerProfileDetailView, \
    get_subcategories, ServiceProviderProfileEditView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/create/', ServiceProviderProfileCreateView.as_view(), name='profile_create'),
    path('profile/completed/<int:pk>/', ServiceProviderProfileCompletedView.as_view(), name='profile_completed'),
    path('profile/edit/<int:pk>/', ServiceProviderProfileEditView.as_view(), name='profile_edit'),
    path('subcategories/<int:category_id>', get_subcategories, name='subcategories'),


]