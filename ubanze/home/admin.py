from django.contrib import admin
from .models import City, Area, Services, ServiceCategory
# Register your models here.


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


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']
    list_filter = ['name']
