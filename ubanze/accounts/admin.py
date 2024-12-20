from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ServiceProviderProfile, CustomerProfile, CustomUser


# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # Fields to display when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone', 'is_active', 'is_staff',
            'is_superuser')}
         ),
    )


@admin.register(ServiceProviderProfile)
class ServiceProviderProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    list_display = ['get_user_name']

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

