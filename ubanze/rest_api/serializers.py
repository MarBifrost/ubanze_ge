
from accounts.models import ServiceProviderProfile, CustomerProfile, CustomUser
from home.models import ServiceCategory
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
