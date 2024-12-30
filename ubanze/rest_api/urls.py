from django.urls import path, include
from .views import ProvidersListing, CustomersListing, ServiceCategoryView, CityAreaView, ServiceCategoryDetailView, AreaViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'providers', ProvidersListing, basename='providers')
router.register(r'customers', CustomersListing, basename='customers')
router.register(r'categories', ServiceCategoryView, basename='categories')
router.register(r'city', CityAreaView, basename='city')
router.register(r'service-categories', ServiceCategoryDetailView, basename='service-categories')
router.register('area', AreaViewSet, basename='area')
router.register(r'areas', AreaViewSet, basename='areas')

urlpatterns = [
    path('', include(router.urls)),
]
