
from accounts.models import ServiceProviderProfile, CustomerProfile, CustomUser
from home.models import ServiceCategory, Area, City, Services
from rest_framework import serializers


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderProfile
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class ServiceCategorydSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'parent', 'children']

    def get_children(self, obj):
        if obj.get_children():
            return ServiceCategorydSerializer(
                obj.get_children(), many=True).data
        return []


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'area_name']


class CityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name', 'area']


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'area_name']


class ServiceSerializer(serializers.ModelSerializer):
    area = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Services
        fields = ['id', 'service_name', 'service_type', 'service_description', 'user', 'area']