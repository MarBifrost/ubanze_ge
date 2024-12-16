from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import City, Area, ServiceProviderProfile, CustomerProfile, CustomUser


# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_service_provider', 'is_customer', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    search_fields = ['city_name']
    list_display = ['city_name']
    list_filter = ['city_name']

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    search_fields = ['area_name']
    list_display = ['area_name']
    list_filter = ['area_name']


@admin.register(ServiceProviderProfile)
class ServiceProviderProfileAdmin(admin.ModelAdmin):
    search_fields = ['service_title', 'user__username']
    list_display = ['get_user_name', 'service_title']

    def get_user_name(self, obj):
        return obj.user.username
    get_user_name.short_description = 'Username'

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    list_display = ['get_user_name']

    def get_user_name(self, obj):
        return obj.user.username
    get_user_name.short_description = 'Username'

