from django.urls import path
from .views import RegisterView, LoginView, ServiceProviderProfileCompletedView, \
    get_subcategories, ServiceProviderProfileEditView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/edit/', ServiceProviderProfileEditView.as_view(), name='profile_edit'),
    path('profile/completed/<int:pk>/', ServiceProviderProfileCompletedView.as_view(), name='completed_profile'),
    path('subcategories/<int:category_id>', get_subcategories, name='subcategories'),
]