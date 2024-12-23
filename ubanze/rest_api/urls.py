from django.urls import path, include
from .views import ProvidersListing, CustomersListing, ServiceCategoryView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('providers', ProvidersListing, basename='providers')
router.register('customers', CustomersListing, basename='customers')
router.register('categories', ServiceCategoryView, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
]