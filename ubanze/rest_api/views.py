from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import ServiceProviderProfile, CustomUser
from .serializers import ProviderSerializer, CustomerSerializer, ServiceCategorydSerializer
from home.models import ServiceCategory


# Create your views here.
class ProvidersListing(viewsets.ModelViewSet):
    queryset=ServiceProviderProfile.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = (IsAuthenticated,)
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CustomersListing(viewsets.ModelViewSet):
    queryset=CustomUser.objects.all().filter(is_service_provider=False)
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ServiceCategoryView(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        queryset = ServiceCategory.objects.all().filter(parent=None)
        serializer = ServiceCategorydSerializer(queryset, many=True)
        return Response(serializer.data)




