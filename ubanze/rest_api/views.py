from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet
from django.shortcuts import get_object_or_404
from accounts.models import ServiceProviderProfile, CustomUser
from .serializers import ProviderSerializer, CustomerSerializer, ServiceCategorydSerializer, CitySerializer, \
    AreaSerializer, ServiceSerializer
from home.models import ServiceCategory, Area, City, Services


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

    def create(self, request):
        serializer = ServiceCategorydSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CityAreaView(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        cities = City.objects.prefetch_related('area').all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceCategoryDetailView(ReadOnlyModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorydSerializer

    def retrieve(self, request, *args, **kwargs):
        category = get_object_or_404(self.queryset, pk=self.kwargs['pk'])
        serializer = self.get_serializer(category)
        return Response(serializer.data)


class AreaViewSet(ReadOnlyModelViewSet):
    queryset = Area.objects.all()
    serializer_class=AreaSerializer

    def retrieve(self, request, *args, **kwargs):
        area = get_object_or_404(self.queryset, pk=self.kwargs['pk'])
        serializer = self.get_serializer(area)
        return Response(serializer.data)


class ServicesByAreaViewSet(ViewSet):
    def retrieve(self, request, pk=None):
        area = get_object_or_404(Area, id=pk)
        services = Services.objects.filter(area=area)
        serializer = ServiceSerializer(services, many=True)

        return Response({
            "area": str(area),
            "services": serializer.data
        })


