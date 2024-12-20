from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.

#model for the City
class City(models.Model):
    id = models.IntegerField(primary_key=True)
    city_name = models.CharField(max_length=50, unique=True, null=True)

    def __str__(self):
        return self.city_name


#Model for the Area
class Area(models.Model):
    id=models.AutoField(primary_key=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='area', default=1)
    area_name = models.CharField(max_length=50, unique=True, null=True)

    def __str__(self):
        return f"{self.area_name}, {self.city}"



#models for the services which is linked with customuser db

class ServiceCategory(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent=TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

class Services(models.Model):
    service_name = models.CharField(max_length=50, unique=True)
    service_type = models.CharField(max_length=50, unique=True)
    service_description = models.TextField(max_length=500, blank=True)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return f"{self.service_name}, {self.service_type}, {self.service_description}, {self.user}"

